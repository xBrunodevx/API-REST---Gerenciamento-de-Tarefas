from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from tasks.models import Task


class TasksTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123',
            email='other@example.com'
        )

    def test_create_task_success(self):
        self.client.force_authenticate(user=self.user)
        url = '/tasks/'
        data = {
            'title': 'Nova Tarefa',
            'description': 'Descrição da tarefa',
            'status': 'pending'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.get()
        self.assertEqual(task.title, 'Nova Tarefa')
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.status, 'pending')

    def test_create_task_minimal_data(self):
        self.client.force_authenticate(user=self.user)
        url = '/tasks/'
        data = {
            'title': 'Tarefa Simples'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get()
        self.assertEqual(task.title, 'Tarefa Simples')
        self.assertEqual(task.status, 'pending')

    def test_create_task_invalid_status(self):
        self.client.force_authenticate(user=self.user)
        url = '/tasks/'
        data = {
            'title': 'Tarefa',
            'status': 'invalid_status'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)

    def test_list_tasks_returns_only_user_tasks(self):
        Task.objects.create(title='Tarefa 1', user=self.user)
        Task.objects.create(title='Tarefa 2', user=self.user)
        Task.objects.create(title='Tarefa do outro', user=self.other_user)
        
        self.client.force_authenticate(user=self.user)
        url = '/tasks/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        titles = [task['title'] for task in response.data['results']]
        self.assertIn('Tarefa 1', titles)
        self.assertIn('Tarefa 2', titles)
        self.assertNotIn('Tarefa do outro', titles)

    def test_list_tasks_empty(self):
        self.client.force_authenticate(user=self.user)
        url = '/tasks/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_get_task_detail_success(self):
        task = Task.objects.create(
            title='Tarefa para obter',
            description='Descrição detalhada',
            user=self.user
        )
        self.client.force_authenticate(user=self.user)
        url = f'/tasks/{task.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Tarefa para obter')
        self.assertEqual(response.data['description'], 'Descrição detalhada')
        self.assertEqual(response.data['user'], self.user.id)

    def test_get_task_other_user_returns_404(self):
        other_task = Task.objects.create(
            title='Tarefa do outro',
            user=self.other_user
        )
        self.client.force_authenticate(user=self.user)
        url = f'/tasks/{other_task.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task_success(self):
        task = Task.objects.create(
            title='Tarefa original',
            description='Descrição original',
            status='pending',
            user=self.user
        )
        self.client.force_authenticate(user=self.user)
        url = f'/tasks/{task.id}/'
        data = {
            'title': 'Tarefa atualizada',
            'description': 'Nova descrição',
            'status': 'in_progress'
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Tarefa atualizada')
        self.assertEqual(task.description, 'Nova descrição')
        self.assertEqual(task.status, 'in_progress')

    def test_partial_update_task(self):
        task = Task.objects.create(
            title='Tarefa original',
            status='pending',
            user=self.user
        )
        self.client.force_authenticate(user=self.user)
        url = f'/tasks/{task.id}/'
        data = {
            'title': 'Tarefa atualizada'
        }
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Tarefa atualizada')
        self.assertEqual(task.status, 'pending')

    def test_update_task_other_user_returns_404(self):
        other_task = Task.objects.create(
            title='Tarefa do outro',
            user=self.other_user
        )
        self.client.force_authenticate(user=self.user)
        url = f'/tasks/{other_task.id}/'
        data = {
            'title': 'Tentativa de atualizar'
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_task_success(self):
        task = Task.objects.create(
            title='Tarefa para deletar',
            user=self.user
        )
        self.client.force_authenticate(user=self.user)
        url = f'/tasks/{task.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_delete_task_other_user_returns_404(self):
        other_task = Task.objects.create(
            title='Tarefa do outro',
            user=self.other_user
        )
        self.client.force_authenticate(user=self.user)
        url = f'/tasks/{other_task.id}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Task.objects.count(), 1)

    def test_unauthenticated_access_denied(self):
        url = '/tasks/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_change_task_owner(self):
        task = Task.objects.create(
            title='Tarefa',
            user=self.user
        )
        self.client.force_authenticate(user=self.user)
        url = f'/tasks/{task.id}/'
        data = {
            'title': 'Tarefa',
            'user': self.other_user.id
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.user, self.user)

    def test_create_task_user_set_automatically(self):
        self.client.force_authenticate(user=self.user)
        url = '/tasks/'
        data = {
            'title': 'Tarefa',
            'user': self.other_user.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get()
        self.assertEqual(task.user, self.user)

