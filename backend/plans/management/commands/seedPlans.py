from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from exercises.models import Exercise
from plans.models import PlanExercise, WorkoutPlan, WorkoutUnit


class Command(BaseCommand):
    help = 'Seed workout plans, units and plan exercises for a given user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            required=True,
            help='Username of the user to attach the seeded plans to',
        )

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')

        # Structure:
        # plans -> list of (plan_attrs, units)
        # units -> list of (unit_attrs, plan_exercises)
        # plan_exercises -> list of dicts keyed by exercise name
        plans = [
            {
                'name': 'Push Pull Legs',
                'description': 'Classic 6-day PPL split for hypertrophy',
                'goal': 'Hypertrophy',
                'length_weeks': 8,
                'is_active': True,
                'units': [
                    {
                        'weekly_order': 1,
                        'name': 'Push A',
                        'warmup_notes': '5 min bike, shoulder dislocates, empty bar bench x10',
                        'exercises': [
                            ('Barbell bench press', 4, 5, 8, 180),
                            ('Incline dumbbell press', 3, 8, 12, 120),
                            ('Overhead press', 3, 6, 10, 150),
                            ('Lateral raise', 3, 12, 15, 60),
                            ('Tricep pushdown', 3, 10, 15, 60),
                        ],
                    },
                    {
                        'weekly_order': 2,
                        'name': 'Pull A',
                        'warmup_notes': 'Band pull-aparts, light lat pulldown x15',
                        'exercises': [
                            ('Deadlift', 3, 3, 5, 240),
                            ('Pull-up', 4, 6, 10, 120),
                            ('Barbell row', 3, 8, 10, 120),
                            ('Face pull', 3, 12, 15, 60),
                            ('Barbell curl', 3, 8, 12, 90),
                        ],
                    },
                    {
                        'weekly_order': 3,
                        'name': 'Legs A',
                        'warmup_notes': '5 min bike, bodyweight squats x15, leg swings',
                        'exercises': [
                            ('Back squat', 4, 5, 8, 180),
                            ('Romanian deadlift', 3, 8, 10, 150),
                            ('Leg press', 3, 10, 12, 120),
                            ('Leg curl', 3, 10, 15, 90),
                        ],
                    },
                    {
                        'weekly_order': 4,
                        'name': 'Push B',
                        'warmup_notes': 'Light dumbbell press x15, band external rotations',
                        'exercises': [
                            ('Incline dumbbell press', 4, 6, 10, 150),
                            ('Push-up', 3, 10, 15, 90),
                            ('Cable fly', 3, 12, 15, 60),
                            ('Lateral raise', 4, 12, 15, 60),
                            ('Tricep pushdown', 3, 10, 12, 60),
                        ],
                    },
                    {
                        'weekly_order': 5,
                        'name': 'Pull B',
                        'warmup_notes': 'Scap pulls, light row x15',
                        'exercises': [
                            ('Barbell row', 4, 6, 10, 150),
                            ('Lat pulldown', 3, 10, 12, 90),
                            ('Pull-up', 3, 6, 10, 120),
                            ('Hammer curl', 3, 10, 12, 60),
                            ('Face pull', 3, 12, 15, 60),
                        ],
                    },
                    {
                        'weekly_order': 6,
                        'name': 'Legs B',
                        'warmup_notes': 'Goblet squats x10, glute bridges x15',
                        'exercises': [
                            ('Romanian deadlift', 4, 6, 8, 180),
                            ('Leg press', 4, 10, 12, 120),
                            ('Back squat', 3, 8, 10, 150),
                            ('Leg curl', 3, 12, 15, 60),
                        ],
                    },
                ],
            },
            {
                'name': 'Upper Lower',
                'description': '4-day upper/lower split for strength and size',
                'goal': 'Strength',
                'length_weeks': 12,
                'is_active': False,
                'units': [
                    {
                        'weekly_order': 1,
                        'name': 'Upper A',
                        'warmup_notes': 'Band pull-aparts, empty bar bench x10',
                        'exercises': [
                            ('Barbell bench press', 4, 4, 6, 210),
                            ('Barbell row', 4, 5, 8, 180),
                            ('Overhead press', 3, 6, 8, 150),
                            ('Pull-up', 3, 6, 10, 120),
                            ('Barbell curl', 3, 8, 12, 90),
                        ],
                    },
                    {
                        'weekly_order': 2,
                        'name': 'Lower A',
                        'warmup_notes': 'Bodyweight squats x15, hip circles',
                        'exercises': [
                            ('Back squat', 4, 4, 6, 210),
                            ('Romanian deadlift', 3, 6, 8, 180),
                            ('Leg press', 3, 8, 12, 120),
                            ('Leg curl', 3, 10, 12, 90),
                        ],
                    },
                    {
                        'weekly_order': 3,
                        'name': 'Upper B',
                        'warmup_notes': 'Light dumbbell press, scap pulls',
                        'exercises': [
                            ('Incline dumbbell press', 4, 6, 10, 150),
                            ('Lat pulldown', 4, 8, 12, 120),
                            ('Lateral raise', 3, 12, 15, 60),
                            ('Cable fly', 3, 10, 15, 60),
                            ('Tricep pushdown', 3, 10, 15, 60),
                            ('Hammer curl', 3, 10, 12, 60),
                        ],
                    },
                    {
                        'weekly_order': 4,
                        'name': 'Lower B',
                        'warmup_notes': '5 min bike, leg swings',
                        'exercises': [
                            ('Deadlift', 3, 3, 5, 240),
                            ('Back squat', 3, 8, 10, 150),
                            ('Leg press', 4, 10, 12, 120),
                            ('Leg curl', 3, 12, 15, 60),
                        ],
                    },
                ],
            },
            {
                'name': 'Full Body Beginner',
                'description': '3-day full body routine for beginners',
                'goal': 'General fitness',
                'length_weeks': 6,
                'is_active': False,
                'units': [
                    {
                        'weekly_order': 1,
                        'name': 'Full Body A',
                        'warmup_notes': '5 min walk, bodyweight squats x10, arm circles',
                        'exercises': [
                            ('Back squat', 3, 8, 10, 120),
                            ('Barbell bench press', 3, 8, 10, 120),
                            ('Barbell row', 3, 8, 10, 120),
                            ('Overhead press', 2, 8, 12, 90),
                        ],
                    },
                    {
                        'weekly_order': 2,
                        'name': 'Full Body B',
                        'warmup_notes': '5 min bike, glute bridges x15',
                        'exercises': [
                            ('Romanian deadlift', 3, 8, 10, 120),
                            ('Push-up', 3, 8, 12, 90),
                            ('Lat pulldown', 3, 10, 12, 90),
                            ('Leg press', 3, 10, 12, 90),
                        ],
                    },
                    {
                        'weekly_order': 3,
                        'name': 'Full Body C',
                        'warmup_notes': 'Band pull-aparts, bodyweight lunges x10',
                        'exercises': [
                            ('Deadlift', 3, 5, 8, 180),
                            ('Incline dumbbell press', 3, 8, 12, 90),
                            ('Pull-up', 3, 5, 8, 120),
                            ('Lateral raise', 2, 12, 15, 60),
                        ],
                    },
                ],
            },
        ]

        exercise_cache = {}

        with transaction.atomic():
            for plan_data in plans:
                units_data = plan_data.pop('units')

                plan, created = WorkoutPlan.objects.get_or_create(
                    user=user,
                    name=plan_data['name'],
                    defaults=plan_data,
                )

                for unit_data in units_data:
                    exercises_data = unit_data.pop('exercises')

                    unit, _ = WorkoutUnit.objects.get_or_create(
                        plan=plan,
                        weekly_order=unit_data['weekly_order'],
                        defaults=unit_data,
                    )

                    for order_index, ex_tuple in enumerate(exercises_data, start=1):
                        ex_name, sets, rep_min, rep_max, rest = ex_tuple

                        if ex_name not in exercise_cache:
                            try:
                                exercise_cache[ex_name] = Exercise.objects.get(name=ex_name)
                            except Exercise.DoesNotExist:
                                raise CommandError(
                                    f'Exercise "{ex_name}" not found. '
                                    f'Run seed_exercises first.'
                                )

                        PlanExercise.objects.get_or_create(
                            unit=unit,
                            exercise=exercise_cache[ex_name],
                            defaults={
                                'order_index': order_index,
                                'default_sets': sets,
                                'rep_range_min': rep_min,
                                'rep_range_max': rep_max,
                                'rest_seconds': rest,
                            },
                        )

        self.stdout.write(self.style.SUCCESS(f'Seeded plans for user "{username}"'))