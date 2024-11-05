from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APIClient

from habits.serializers import HabitSerializer
from users.models import User
from habits.models import Habit


class HabitModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            user=self.user,
            place='Gym',
            time='10:00:00',
            action='Exercise',
            is_pleasant=True,
            frequency='daily',
            completion_time=30,
            is_public=True
        )

    def test_habit_creation(self):
        self.assertIsInstance(self.habit, Habit)
        self.assertEqual(self.habit.action, 'Exercise')

    def test_habit_creation_with_reward_and_related_habit(self):
        habit1 = Habit.objects.create(
            user=self.user,
            place='Gym',
            time='10:00:00',
            action='Exercise',
            is_pleasant=False,
            frequency='daily',
            completion_time=30
        )
        habit2 = Habit.objects.create(
            user=self.user,
            place='Park',
            time='11:00:00',
            action='Walk',
            is_pleasant=True,
            related_habit=habit1,
            frequency='daily',
            completion_time=30
        )
        with self.assertRaises(ValidationError):
            habit2.reward = 'Chocolate'
            habit2.clean()  # Вызывает проверку

    def test_valid_habit_serializer(self):
        serializer = HabitSerializer(data=self.habit)
        self.assertFalse(serializer.is_valid())

    def test_create_habit(self):
        data = {
            'place': 'Park',
            'time': '11:00:00',
            'action': 'Walk',
            'is_pleasant': False,
            'frequency': 'weekly',
            'completion_time': 60,
            'is_public': False
        }
        response = self.client.post('/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)

    def test_create_habit_with_invalid_data(self):
        data = {
            'place': 'Park',
            'time': '11:00:00',
            'action': 'Walk',
            'is_pleasant': True,
            'reward': 'Chocolate',
            'related_habit': self.habit.id,
            'frequency': 'daily',
            'completion_time': 30
        }
        response = self.client.post('/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_public_habits(self):
        response = self.client.get('/habits/public_habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_get_my_habits(self):
        response = self.client.get('/habits/my_habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
