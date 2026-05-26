from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from habits.models import Habit


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )

    def test_habit_creation(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Зарядка",
            duration=60,
        )
        self.assertEqual(habit.action, "Зарядка")
        self.assertEqual(habit.periodicity, 1)
        self.assertFalse(habit.is_pleasant)
        self.assertFalse(habit.is_public)

    def test_habit_str(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Зарядка",
            duration=60,
        )
        self.assertIn("Зарядка", str(habit))


class HabitValidatorTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_duration_more_than_120(self):
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "action": "Зарядка",
            "duration": 150,
            "periodicity": 1,
        }
        response = self.client.post(reverse("habit-create"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reward_and_related_habit_together(self):
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="09:00:00",
            action="Ванна с пеной",
            duration=60,
            is_pleasant=True,
        )
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "action": "Прогулка",
            "duration": 60,
            "periodicity": 1,
            "reward": "Мороженое",
            "related_habit": pleasant_habit.id,
        }
        response = self.client.post(reverse("habit-create"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_related_habit_must_be_pleasant(self):
        not_pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="09:00:00",
            action="Бег",
            duration=60,
            is_pleasant=False,
        )
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "action": "Прогулка",
            "duration": 60,
            "periodicity": 1,
            "related_habit": not_pleasant_habit.id,
        }
        response = self.client.post(reverse("habit-create"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pleasant_habit_no_reward(self):
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "action": "Ванна",
            "duration": 60,
            "periodicity": 1,
            "is_pleasant": True,
            "reward": "Мороженое",
        }
        response = self.client.post(reverse("habit-create"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_periodicity_more_than_7(self):
        data = {
            "place": "Дом",
            "time": "08:00:00",
            "action": "Зарядка",
            "duration": 60,
            "periodicity": 8,
        }
        response = self.client.post(reverse("habit-create"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            password="testpass123",
        )
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Зарядка",
            duration=60,
        )

    def test_create_habit(self):
        data = {
            "place": "Парк",
            "time": "07:00:00",
            "action": "Бег",
            "duration": 30,
            "periodicity": 1,
        }
        response = self.client.post(reverse("habit-create"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_habits(self):
        response = self.client.get(reverse("habit-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_public_habits(self):
        Habit.objects.create(
            user=self.other_user,
            place="Парк",
            time="07:00:00",
            action="Бег",
            duration=30,
            is_public=True,
        )
        response = self.client.get(reverse("habit-public-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_sees_only_own_habits(self):
        Habit.objects.create(
            user=self.other_user,
            place="Парк",
            time="07:00:00",
            action="Бег",
            duration=30,
        )
        response = self.client.get(reverse("habit-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for habit in response.data["results"]:
            self.assertEqual(habit["user"], self.user.id)

    def test_delete_habit(self):
        response = self.client.delete(
            reverse("habit-detail", kwargs={"pk": self.habit.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_other_user_cannot_delete_habit(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(
            reverse("habit-detail", kwargs={"pk": self.habit.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)