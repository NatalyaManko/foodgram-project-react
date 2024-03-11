from http import HTTPStatus

from django.test import TestCase
from rest_framework.test import APIClient

from recipes import models
from users import models


class FoodgramAPITestCase(TestCase):

    def setUp(self):
        User = models.User
        self.user = User.objects.create_user(username='auth_user')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_exists(self):
        """Проверка доступности списка задач."""
        
        response = self.client.get('/api/recipes/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_task_creation(self):
        """Проверка создания задачи."""
        
        data = {'name': 'Test', 'text': 'Test'}
        response = self.guest_client.post('/api/recipes/', data=data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertTrue(models.Recipe.objects.filter(name='Test').exists())
