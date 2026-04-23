from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from .models import MuscleGroup, EquipmentType, Exercise


class ExerciseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='john', email='john@test.com', password='secret123'
        )
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.chest = MuscleGroup.objects.create(name='Chest')
        self.back = MuscleGroup.objects.create(name='Back')
        self.barbell = EquipmentType.objects.create(name='Barbell')
        self.cable = EquipmentType.objects.create(name='Cable')

        self.bench = Exercise.objects.create(
            name='Bench press',
            muscle_group=self.chest,
            equipment_type=self.barbell,
            is_compound=True,
        )
        self.fly = Exercise.objects.create(
            name='Cable fly',
            muscle_group=self.chest,
            equipment_type=self.cable,
            is_compound=False,
        )
        self.deadlift = Exercise.objects.create(
            name='Deadlift',
            muscle_group=self.back,
            equipment_type=self.barbell,
            is_compound=True,
        )

    def test_list_muscle_groups(self):
        response = self.client.get('/api/muscle-groups/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_equipment_types(self):
        response = self.client.get('/api/equipment-types/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_exercises(self):
        response = self.client.get('/api/exercises/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_muscle_group(self):
        response = self.client.get(f'/api/exercises/?muscle_group={self.chest.id}')
        self.assertEqual(len(response.data), 2)

    def test_filter_by_equipment_type(self):
        response = self.client.get(f'/api/exercises/?equipment_type={self.barbell.id}')
        self.assertEqual(len(response.data), 2)

    def test_filter_by_compound(self):
        response = self.client.get('/api/exercises/?is_compound=true')
        self.assertEqual(len(response.data), 2)

        response = self.client.get('/api/exercises/?is_compound=false')
        self.assertEqual(len(response.data), 1)

    def test_retrieve_single_exercise(self):
        response = self.client.get(f'/api/exercises/{self.bench.id}/')
        self.assertEqual(response.data['name'], 'Bench press')
        self.assertEqual(response.data['muscle_group_name'], 'Chest')
        self.assertEqual(response.data['equipment_type_name'], 'Barbell')
        self.assertTrue(response.data['is_compound'])

    def test_unauthenticated_returns_401(self):
        self.client.credentials()
        response = self.client.get('/api/exercises/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
