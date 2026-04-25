from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from exercises.models import MuscleGroup, EquipmentType, Exercise
from .models import WorkoutPlan, WorkoutUnit, PlanExercise


class WorkoutPlanTests(TestCase):
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

        self.chest = MuscleGroup.objects.create(name='Chest')
        self.barbell = EquipmentType.objects.create(name='Barbell')
        self.bench = Exercise.objects.create(
            name='Bench press',
            muscle_group=self.chest,
            equipment_type=self.barbell,
            is_compound=True
        )

    def test_create_plan(self):
        response = self.client.post('/api/plans/', {
            'name': '3 week hypertrophy',
            'goal': 'muscle gain',
            'length_weeks': 3
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkoutPlan.objects.count(), 1)
        self.assertEqual(WorkoutPlan.objects.get().user, self.user)

    def test_list_only_own_plans(self):
        WorkoutPlan.objects.create(user=self.user, name='Mine', length_weeks=3)
        WorkoutPlan.objects.create(user=self.other_user, name='Theirs', length_weeks=3)

        response = self.client.get('/api/plans/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Mine')

    def test_cannot_access_other_users_plan(self):
        other_plan = WorkoutPlan.objects.create(
            user=self.other_user, name='Theirs', length_weeks=3
        )
        response = self.client.get(f'/api/plans/{other_plan.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_unit_to_plan(self):
        plan = WorkoutPlan.objects.create(
            user=self.user, name='Test', length_weeks=3
        )
        response = self.client.post(f'/api/plans/{plan.id}/units/', {
            'weekly_order': 1,
            'name': 'Push day'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(plan.units.count(), 1)

    def test_cannot_add_unit_to_other_users_plan(self):
        other_plan = WorkoutPlan.objects.create(
            user=self.other_user, name='Theirs', length_weeks=3
        )
        response = self.client.post(f'/api/plans/{other_plan.id}/units/', {
            'weekly_order': 1,
            'name': 'Push day'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_exercise_to_unit(self):
        plan = WorkoutPlan.objects.create(
            user=self.user, name='Test', length_weeks=3
        )
        unit = WorkoutUnit.objects.create(plan=plan, weekly_order=1, name='Push')

        response = self.client.post(
            f'/api/plans/{plan.id}/units/{unit.id}/exercises/', {
                'exercise': str(self.bench.id),
                'order_index': 1,
                'default_sets': 4,
                'rep_range_min': 6,
                'rep_range_max': 12,
                'rest_seconds': 120,
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(unit.plan_exercises.count(), 1)

    def test_get_full_plan_tree(self):
        plan = WorkoutPlan.objects.create(
            user=self.user, name='Test', length_weeks=3
        )
        unit = WorkoutUnit.objects.create(plan=plan, weekly_order=1, name='Push')
        PlanExercise.objects.create(
            unit=unit, exercise=self.bench,
            order_index=1, default_sets=4,
            rep_range_min=6, rep_range_max=12, rest_seconds=120
        )

        response = self.client.get(f'/api/plans/{plan.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['units']), 1)
        self.assertEqual(len(response.data['units'][0]['plan_exercises']), 1)
        self.assertEqual(
            response.data['units'][0]['plan_exercises'][0]['exercise_name'],
            'Bench press'
        )
