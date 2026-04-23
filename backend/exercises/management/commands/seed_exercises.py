from django.core.management.base import BaseCommand
from exercises.models import MuscleGroup, EquipmentType, Exercise


class Command(BaseCommand):
    help = 'Seed muscle groups, equipment types and exercises'

    def handle(self, *args, **options):
        # (exercise name, equipment, is_compound)
        data = {
            'Chest': [
                ('Barbell bench press', 'Barbell', True),
                ('Incline dumbbell press', 'Dumbbell', True),
                ('Cable fly', 'Cable', False),
                ('Push-up', 'Bodyweight', True),
            ],
            'Back': [
                ('Deadlift', 'Barbell', True),
                ('Pull-up', 'Bodyweight', True),
                ('Barbell row', 'Barbell', True),
                ('Lat pulldown', 'Cable', False),
            ],
            'Legs': [
                ('Back squat', 'Barbell', True),
                ('Romanian deadlift', 'Barbell', True),
                ('Leg press', 'Machine', True),
                ('Leg curl', 'Machine', False),
            ],
            'Shoulders': [
                ('Overhead press', 'Barbell', True),
                ('Lateral raise', 'Dumbbell', False),
                ('Face pull', 'Cable', False),
            ],
            'Arms': [
                ('Barbell curl', 'Barbell', False),
                ('Tricep pushdown', 'Cable', False),
                ('Hammer curl', 'Dumbbell', False),
            ],
        }

        equipment_cache = {}

        for group_name, exercises in data.items():
            group, _ = MuscleGroup.objects.get_or_create(name=group_name)

            for ex_name, equipment_name, is_compound in exercises:
                if equipment_name not in equipment_cache:
                    equipment_cache[equipment_name], _ = (
                        EquipmentType.objects.get_or_create(name=equipment_name)
                    )

                Exercise.objects.get_or_create(
                    name=ex_name,
                    defaults={
                        'muscle_group': group,
                        'equipment_type': equipment_cache[equipment_name],
                        'is_compound': is_compound,
                    }
                )

        self.stdout.write(self.style.SUCCESS('Seeded successfully'))