from django.core.urlresolvers import reverse
from common.tests.test_views import LoginMixin
from rest_framework.test import APITestCase

from ..models import MflUser


class TestLogin(APITestCase):
    def setUp(self):
        self.user = MflUser.objects.create(
            'user@test.com', 'pass', 'pass', 'pass'
        )
        self.login_url = reverse("api:rest_auth:rest_login")
        self.logout_url = reverse("api:rest_auth:rest_logout")
        super(TestLogin, self).setUp()

    def test_login(self):
        data = {
            "username": 'user@test.com',
            "password": 'pass'
        }
        response = self.client.post(self.login_url, data)
        self.assertTrue(self.user.is_authenticated())
        self.assertEquals(200, response.status_code)

    def test_inactive_user_login(self):
        user = MflUser.objects.create(
            'user2@test.com', 'test first name', 'test user name', 'pass'
        )
        user.is_active = False
        user.save()
        response = self.client.post(
            self.login_url,
            {
                "username": user.email,
                "password": 'pass'
            }
        )
        self.assertEquals(400, response.status_code)
        self.assertEquals(
            {'non_field_errors': ['User account is disabled.']},
            response.data
        )

    def test_login_user_does_not_exist(self):
        data = {
            "username": "non_existent@email.com",
            "password": 'pass'
        }
        response = self.client.post(self.login_url, data)
        self.assertEquals(400, response.status_code)
        self.assertEquals(
            {
                'non_field_errors': [
                    'Unable to log in with provided credentials.']
            },
            response.data
        )


class TestGroupViews(LoginMixin, APITestCase):
    def setUp(self):
        super(TestGroupViews, self).setUp()
        self.url = reverse('api:users:groups_list')

    def test_create_and_update_group(self):
        data = {
            "name": "Documentation Example Group",
            "permissions": [
                {
                    "id": 61,
                    "name": "Can add email address",
                    "codename": "add_emailaddress"
                },
                {
                    "id": 62,
                    "name": "Can change email address",
                    "codename": "change_emailaddress"
                }
            ]
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(response.data['name'], 'Documentation Example Group')
        self.assertEqual(len(response.data['permissions']), 2)

        new_group_id = response.data['id']
        update_url = reverse(
            'api:users:group_detail', kwargs={'pk': new_group_id})
        update_response = self.client.put(
            update_url,
            {
                "name": "Documentation Example Group Updated",
                "permissions": [
                    {
                        "id": 61,
                        "name": "Can add email address",
                        "codename": "add_emailaddress"
                    }
                ]
            }
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(len(update_response.data['permissions']), 1)

    def test_failed_create(self):
        data = {
            "name": "Documentation Example Group",
            "permissions": [
                {
                    "id": 67897,
                    "name": "does not exist",
                    "codename": "query should raise an exception"
                }
            ]
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)
