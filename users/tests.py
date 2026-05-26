from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User


class UserRegistrationTest(APITestCase):
    def test_register_user(self):
        data = {
            "username": "newuser",
            "password": "testpass123",
            "email": "test@test.com",
        }
        response = self.client.post(reverse("user-register"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_obtain_token(self):
        User.objects.create_user(username="testuser", password="testpass123")
        data = {
            "username": "testuser",
            "password": "testpass123",
        }
        response = self.client.post(reverse("token_obtain_pair"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)