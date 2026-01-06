from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class AuthFlowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="tester",
            password="testpass123",
            email="tester@example.com",
        )

    def test_register_creates_user_and_tokens(self):
        data = {
            "username": "newuser",
            "password": "newpass123",
            "password2": "newpass123",
            "email": "new@example.com",
        }
        resp = self.client.post("/auth/register/", data, format="json")

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_password_mismatch(self):
        data = {
            "username": "newuser",
            "password": "onepass",
            "password2": "otherpass",
            "email": "new@example.com",
        }
        resp = self.client.post("/auth/register/", data, format="json")

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", resp.data)

    def test_login_success(self):
        data = {"username": "tester", "password": "testpass123"}
        resp = self.client.post("/auth/login/", data, format="json")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)

    def test_login_invalid_credentials(self):
        data = {"username": "tester", "password": "wrong"}
        resp = self.client.post("/auth/login/", data, format="json")

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", resp.data)

    def test_protected_endpoint_requires_token(self):
        resp = self.client.get("/tasks/")

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", resp.data)
