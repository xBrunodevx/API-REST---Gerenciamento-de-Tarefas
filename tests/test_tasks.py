from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from tasks.models import Task


class TaskFlowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="owner",
            password="testpass123",
            email="owner@example.com",
        )
        self.other = User.objects.create_user(
            username="other",
            password="testpass123",
            email="other@example.com",
        )
        self.token = self._login_and_get_token("owner", "testpass123")

    def _login_and_get_token(self, username, password):
        resp = self.client.post(
            "/auth/login/", {"username": username, "password": password}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        return resp.data["access"]

    def _auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_task_success(self):
        self._auth()
        data = {"title": "Tarefa", "description": "desc", "status": "pending"}
        resp = self.client.post("/tasks/", data, format="json")

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.get()
        self.assertEqual(task.user, self.user)

    def test_list_tasks_returns_only_owner(self):
        Task.objects.create(title="A", user=self.user)
        Task.objects.create(title="B", user=self.user)
        Task.objects.create(title="Other", user=self.other)

        self._auth()
        resp = self.client.get("/tasks/")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = {item["title"] for item in resp.data}
        self.assertEqual(titles, {"A", "B"})

    def test_detail_other_user_returns_404(self):
        task_other = Task.objects.create(title="Other", user=self.other)
        self._auth()
        resp = self.client.get(f"/tasks/{task_other.id}/")

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_status_validation_rejects_invalid_value(self):
        self._auth()
        resp = self.client.post(
            "/tasks/", {"title": "Tarefa", "status": "invalid"}, format="json"
        )

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", resp.data)

    def test_cannot_change_owner(self):
        task = Task.objects.create(title="Mine", user=self.user)
        self._auth()
        resp = self.client.put(
            f"/tasks/{task.id}/",
            {"title": "Mine", "user": self.other.id, "status": "pending"},
            format="json",
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.user, self.user)
