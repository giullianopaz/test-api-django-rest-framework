import json

from django.test import TestCase, Client
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status

from apps.companies.models import Company
from apps.users.models import User
from apps.users.serializers import UserSerializer


class UserTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.numbers_of_users = 5
        self.user_list = []

        self.valid_user_data = {
            'password': 'passuser',
            'username': 'usertest',
            'email': 'teste@test.com',
            'first_name': 'Test',
            'last_name': 'Test'
        }
        self.invalid_user_data = {
            'password': '',
            'username': '',
            'email': 'teste',
            'first_name': 'Test',
            'last_name': 'Test'
        }

        for i in range(1, self.numbers_of_users + 1):
            user = User.objects.create_user(
                username=f'usertest{i}',
                first_name='User',
                last_name=f'Test {i}',
                email=f'test{i}@test.com',
            )
            user.set_password(f'passuser{i}')
            user.save()
            self.user_list.append(user.username)

    def test_list_users(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        users = User.objects.all()
        self.assertEqual(users.count(), self.numbers_of_users)

        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_user(self):
        for username in self.user_list:
            response = self.client.get(reverse('user-detail', kwargs={'username': username}))

            user = User.objects.get(username=username)
            serializer = UserSerializer(user)
            self.assertEqual(response.data, serializer.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_retrieve_user(self):
        user_not_exists = 'username_not_exists_on_db'
        response = self.client.get(reverse('user-detail', kwargs={'username': user_not_exists}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_and_authenticate_user(self):
        response = self.client.post(reverse('user-list'), data=json.dumps(self.valid_user_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_exists = User.objects.filter(username=self.valid_user_data.get('username')).exists()
        self.assertTrue(user_exists)

        self.assertIsNotNone(authenticate(username=self.valid_user_data.get('username'),
                                          password=self.valid_user_data.get('password')))

    def test_invalid_create_user(self):
        response = self.client.post(reverse('user-list'), data=json.dumps(self.invalid_user_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        updated_username = 'updated_usertest'
        updated_password = 'updated_passuser'
        valid_user_data = self.valid_user_data.copy()
        valid_user_data['username'] = updated_username
        valid_user_data['password'] = updated_password

        to_update = self.user_list[0]
        response = self.client.put(reverse('user-detail', kwargs={'username': to_update}),
                                   data=json.dumps(valid_user_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('username'), updated_username)
        self.assertIsNotNone(authenticate(username=updated_username,
                                          password=updated_password))

    def test_invalid_update_user(self):
        to_update = self.user_list[0]
        response = self.client.put(reverse('user-detail', kwargs={'username': to_update}),
                                   data=json.dumps(self.invalid_user_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.json().get('username'))
        self.assertIn('This field may not be blank.', response.json().get('password'))
        self.assertIn('Enter a valid email address.', response.json().get('email'))

    def test_partial_update_user(self):
        partial_updated_username = 'partial_updated_usertest'
        valid_user_data = self.valid_user_data.copy()
        valid_user_data['username'] = partial_updated_username

        to_update = self.user_list[0]
        response = self.client.patch(reverse('user-detail', kwargs={'username': to_update}),
                                     data=json.dumps(valid_user_data),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('username'), partial_updated_username)
        self.assertIsNotNone(authenticate(username=partial_updated_username,
                                          password=self.valid_user_data.get('password')))

    def test_invalid_partial_update_user(self):
        partial_invalid_user_data = {
            'username': '',
            'password': '',
        }
        to_update = self.user_list[0]
        response = self.client.patch(reverse('user-detail', kwargs={'username': to_update}),
                                     data=json.dumps(partial_invalid_user_data),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.json().get('username'))
        self.assertIn('This field may not be blank.', response.json().get('password'))

    def test_add_companies_to_user(self):
        numbers_of_companies = 3
        company_list = [
            Company.objects.create(
                name=f'Company {i} LTDA',
                trading_name=f'Company {i}',
                registered_number=f'2024027200017{i}',
                email=f'contato@company{i}.com',
                phone=f'999999999{i}',
            ).pk for i in range(1, numbers_of_companies + 1)
        ]

        username = self.user_list[0]
        response = self.client.post(reverse('user-add-companies', kwargs={'username': username}),
                                     data=json.dumps({
                                         'companies': company_list
                                     }),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(username=username).companies.count(), numbers_of_companies)

    def test_update_companies_to_user(self):
        numbers_of_companies = 3
        company_list = [
            Company.objects.create(
                name=f'Company {i} LTDA',
                trading_name=f'Company {i}',
                registered_number=f'2024027200017{i}',
                email=f'contato@company{i}.com',
                phone=f'999999999{i}',
            ).pk for i in range(1, numbers_of_companies + 1)
        ]

        username = self.user_list[0]
        response = self.client.put(reverse('user-update-companies', kwargs={'username': username}),
                                     data=json.dumps({
                                         'companies': company_list
                                     }),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(username=username).companies.count(), numbers_of_companies)

    def test_delete_companies_from_user(self):
        numbers_of_companies = 3
        company_list = [
            Company.objects.create(
                name=f'Company {i} LTDA',
                trading_name=f'Company {i}',
                registered_number=f'2024027200017{i}',
                email=f'contato@company{i}.com',
                phone=f'999999999{i}',
            ).pk for i in range(1, numbers_of_companies + 1)
        ]

        user = User.objects.get(username=self.user_list[0])
        user.add_companies(company_list)

        response = self.client.delete(reverse('user-delete-companies', kwargs={'username': user.username}),
                                     data=json.dumps({
                                         'companies': company_list[:-1]
                                     }),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.get_companies().count(), 1)

    def test_clean_companies_from_user(self):
        numbers_of_companies = 3
        company_list = [
            Company.objects.create(
                name=f'Company {i} LTDA',
                trading_name=f'Company {i}',
                registered_number=f'2024027200017{i}',
                email=f'contato@company{i}.com',
                phone=f'999999999{i}',
            ).pk for i in range(1, numbers_of_companies + 1)
        ]

        user = User.objects.get(username=self.user_list[0])
        user.add_companies(company_list)

        response = self.client.delete(reverse('user-clean-companies', kwargs={'username': user.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.get_companies().count(), 0)

    def test_delete_user(self):
        to_delete = self.user_list[0]
        response = self.client.delete(reverse('user-detail', kwargs={'username': to_delete}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        user_exists = User.objects.filter(username=to_delete).exists()
        self.assertFalse(user_exists)

    def test_invalid_delete_user(self):
        user_not_exists = 'username_not_exists_on_db'
        response = self.client.delete(reverse('user-detail', kwargs={'username': user_not_exists}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
