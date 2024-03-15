from http import HTTPStatus

from django.test import TestCase
from rest_framework.test import APIClient

from users import models


class FoodgramAPITestCase(TestCase):

    def setUp(self):
        User = models.User
        self.user = User.objects.create_user(username='auth_user')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_exists(self):
        """Проверка доступности списка рецептов."""

        response = self.client.get('/api/recipes/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
