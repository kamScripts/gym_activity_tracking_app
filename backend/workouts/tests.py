from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from exercises.models import MuscleGroup, EquipmentType, Exercise
from plans.models import WorkoutPlan, WorkoutUnit, PlanExercise
from .models import Workout, Set


class WorkoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='john', email='john@test.com', password='secret123'
        )
        self.other_user = User.objects.create_user(
            username='jane', email='jane@test.com', password='secret123'
        )
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # set up reference data and a plan
        self.chest = MuscleGroup.objects.create(name='Chest')
        self.barbell = EquipmentType.objects.create(name='Barbell')
        self.bench = Exercise.objects.create(
            name='Bench press', muscle_group=self.chest,
            equipment_type=self.barbell, is_compound=True
        )
        self.plan = WorkoutPlan.objects.create(
            user=self.user, name='Test plan', length_weeks=3
        )
        self.unit = WorkoutUnit.objects.create(
            plan=self.plan, weekly_order=1, name='Push'
        )
        self.plan_exercise = PlanExercise.objects.create(
            unit=self.unit, exercise=self.bench,
            order_index=1, default_sets=4,
            rep_range_min=6, rep_range_max=12, rest_seconds=120
        )

    def test_start_workout(self):
        response = self.client.post('/api/workouts/', {
            'plan': str(self.plan.id),
            'workout_unit': str(self.unit.id),
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 1)
        self.assertEqual(Workout.objects.get().user, self.user)

    def test_log_set(self):
        workout = Workout.objects.create(
            user=self.user, plan=self.plan, workout_unit=self.unit
        )
        response = self.client.post(f'/api/workouts/{workout.id}/sets/', {
            'exercise': str(self.bench.id),
            'set_number': 1,
            'reps': 10,
            'weight_kg': '80.00',
            'rest_after_seconds': 90,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(workout.sets.count(), 1)

    def test_get_workout_with_sets(self):
        workout = Workout.objects.create(
            user=self.user, plan=self.plan, workout_unit=self.unit
        )
        Set.objects.create(
            workout=workout, exercise=self.bench,
            set_number=1, reps=10, weight_kg=80
        )
        Set.objects.create(
            workout=workout, exercise=self.bench,
            set_number=2, reps=8, weight_kg=82.5
        )

        response = self.client.get(f'/api/workouts/{workout.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['sets']), 2)

    def test_prefill_returns_plan_defaults(self):
        response = self.client.get(
            f'/api/plans/{self.plan.id}/units/{self.unit.id}/prefill/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['default_sets'], 4)
        self.assertEqual(response.data[0]['rep_range_min'], 6)
        self.assertEqual(response.data[0]['rest_seconds'], 120)

    def test_prefill_other_users_unit_returns_404(self):
        other_plan = WorkoutPlan.objects.create(
            user=self.other_user, name='Theirs', length_weeks=3
        )
        other_unit = WorkoutUnit.objects.create(
            plan=other_plan, weekly_order=1
        )
        response = self.client.get(
            f'/api/plans/{other_plan.id}/units/{other_unit.id}/prefill/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_start_workout_for_other_users_plan(self):
        other_plan = WorkoutPlan.objects.create(
            user=self.other_user, name='Theirs', length_weeks=3
        )
        other_unit = WorkoutUnit.objects.create(
            plan=other_plan, weekly_order=1
        )
        response = self.client.post('/api/workouts/', {
            'plan': str(other_plan.id),
            'workout_unit': str(other_unit.id),
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_history_only_shows_own_workouts(self):
        Workout.objects.create(
            user=self.user, plan=self.plan, workout_unit=self.unit
        )
        other_plan = WorkoutPlan.objects.create(
            user=self.other_user, name='Theirs', length_weeks=3
        )
        other_unit = WorkoutUnit.objects.create(
            plan=other_plan, weekly_order=1
        )
        Workout.objects.create(
            user=self.other_user, plan=other_plan, workout_unit=other_unit
        )

        response = self.client.get('/api/workouts/')
        self.assertEqual(len(response.data), 1)

    def test_mark_workout_complete(self):
        workout = Workout.objects.create(
            user=self.user, plan=self.plan, workout_unit=self.unit
        )
        response = self.client.patch(f'/api/workouts/{workout.id}/', {
            'notes': 'felt strong',
            'completed_at': '2026-04-25T15:30:00Z',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        workout.refresh_from_db()
        self.assertEqual(workout.notes, 'felt strong')
        self.assertIsNotNone(workout.completed_at)
