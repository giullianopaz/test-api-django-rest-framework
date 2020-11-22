import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer
from apps.users.models import User


class CompanyTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.numbers_of_companies = 5

        self.valid_company_data = {
            'name': 'Company Hero LTDA',
            'trading_name': 'Company Hero',
            'registered_number': '20240272000176',
            'email': 'contato@companyhero.com.br',
            'phone': '9999999999'
        }
        self.invalid_company_data = {
            'name': '',
            'trading_name': '',
            'registered_number': '',
            'email': 'contatocompanyhero',
        }

        self.company_list = [
            Company.objects.create(
                name=f'Company {i} LTDA',
                trading_name=f'Company {i}',
                registered_number=f'2024027200017{i}',
                email=f'contato@company{i}.com',
                phone=f'999999999{i}',
            ).pk for i in range(1, self.numbers_of_companies + 1)
        ]

    def test_list_companies(self):
        response = self.client.get(reverse('company-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        companies = Company.objects.all()
        self.assertEqual(companies.count(), self.numbers_of_companies)

        serializer = CompanySerializer(companies, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_company(self):
        for company_pk in self.company_list:
            response = self.client.get(reverse('company-detail', kwargs={'pk': company_pk}))

            company = Company.objects.get(pk=company_pk)
            serializer = CompanySerializer(company)
            self.assertEqual(response.data, serializer.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_retrieve_company(self):
        company_not_exists_pk = Company.objects.last().pk + 10
        response = self.client.get(reverse('company-detail', kwargs={'pk': company_not_exists_pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_company(self):
        response = self.client.post(reverse('company-list'), data=json.dumps(self.valid_company_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        company_exists = Company.objects.filter(
            registered_number=self.valid_company_data.get('registered_number')).exists()
        self.assertTrue(company_exists)

    def test_invalid_create_company(self):
        response = self.client.post(reverse('company-list'), data=json.dumps(self.invalid_company_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.json().get('name'))
        self.assertIn('This field may not be blank.', response.json().get('registered_number'))
        self.assertIn('Enter a valid email address.', response.json().get('email'))

    def test_update_company(self):
        to_update_pk = self.company_list[0]
        response = self.client.put(reverse('company-detail', kwargs={'pk': to_update_pk}),
                                   data=json.dumps(self.valid_company_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('registered_number'), self.valid_company_data.get('registered_number'))

    def test_invalid_update_company(self):
        to_update_pk = self.company_list[0]
        response = self.client.put(reverse('company-detail', kwargs={'pk': to_update_pk}),
                                   data=json.dumps(self.invalid_company_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.json().get('name'))
        self.assertIn('This field may not be blank.', response.json().get('registered_number'))
        self.assertIn('Enter a valid email address.', response.json().get('email'))

    def test_partial_update_company(self):
        partial_updated_name = 'Partial Updated Company Hero'
        partial_updated_email = 'partial_updated_contato@companyhero.com.br'
        valid_company_data = self.valid_company_data.copy()
        valid_company_data['name'] = partial_updated_name
        valid_company_data['email'] = partial_updated_email

        to_update_pk = self.company_list[0]
        response = self.client.patch(reverse('company-detail', kwargs={'pk': to_update_pk}),
                                     data=json.dumps(valid_company_data),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('name'), partial_updated_name)
        self.assertEqual(response.json().get('email'), partial_updated_email)

    def test_invalid_partial_update_company(self):
        partial_invalid_company_data = {
            'name': '',
            'registered_number': '',
            'email': 'companyhero.com.br',
        }
        to_update_pk = self.company_list[0]
        response = self.client.patch(reverse('company-detail', kwargs={'pk': to_update_pk}),
                                     data=json.dumps(partial_invalid_company_data),
                                     content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank.', response.json().get('name'))
        self.assertIn('This field may not be blank.', response.json().get('registered_number'))
        self.assertIn('Enter a valid email address.', response.json().get('email'))

    def test_add_employees_to_company(self):
        numbers_of_employees = 3
        employee_list = []
        for i in range(1, numbers_of_employees + 1):
            user = User.objects.create_user(
                username=f'usertest{i}',
                first_name='User',
                last_name=f'Test {i}',
                email=f'test{i}@test.com',
            )
            employee_list.append(user.pk)

        test_company_pk = self.company_list[0]
        response = self.client.post(reverse('company-add-employees', kwargs={'pk': test_company_pk}),
                                     data=json.dumps({
                                         'employees': employee_list
                                     }),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.get(pk=test_company_pk).employees.count(), numbers_of_employees)

    def test_update_employees_to_company(self):
        numbers_of_employees = 3
        employee_list = []
        for i in range(1, numbers_of_employees + 1):
            user = User.objects.create_user(
                username=f'usertest{i}',
                first_name='User',
                last_name=f'Test {i}',
                email=f'test{i}@test.com',
            )
            employee_list.append(user.pk)

        test_company_pk = self.company_list[0]
        response = self.client.put(reverse('company-update-employees', kwargs={'pk': test_company_pk}),
                                     data=json.dumps({
                                         'employees': employee_list
                                     }),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.get(pk=test_company_pk).employees.count(), numbers_of_employees)

    def test_delete_employees_to_company(self):
        numbers_of_employees = 3
        employee_list = []
        for i in range(1, numbers_of_employees + 1):
            user = User.objects.create_user(
                username=f'usertest{i}',
                first_name='User',
                last_name=f'Test {i}',
                email=f'test{i}@test.com',
            )
            employee_list.append(user.pk)

        test_company = Company.objects.get(pk=self.company_list[0])
        test_company.add_employees(User.get_existing_by_pk(employee_list))

        response = self.client.delete(reverse('company-delete-employees', kwargs={'pk': test_company.pk}),
                                     data=json.dumps({
                                         'employees': employee_list[:-1]
                                     }),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(test_company.get_employees().count(), 1)

    def test_clean_employees_to_company(self):
        numbers_of_employees = 3
        employee_list = []
        for i in range(1, numbers_of_employees + 1):
            user = User.objects.create_user(
                username=f'usertest{i}',
                first_name='User',
                last_name=f'Test {i}',
                email=f'test{i}@test.com',
            )
            employee_list.append(user.pk)

        test_company = Company.objects.get(pk=self.company_list[0])
        test_company.add_employees(User.get_existing_by_pk(employee_list))

        response = self.client.delete(reverse('company-clean-employees', kwargs={'pk': test_company.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(test_company.get_employees().count(), 0)

    def test_delete_company(self):
        company_pk = self.company_list[0]
        response = self.client.delete(reverse('company-detail', kwargs={'pk': company_pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        company_exists = Company.objects.filter(pk=company_pk).exists()
        self.assertFalse(company_exists)

    def test_invalid_delete_company(self):
        company_not_exists_pk = Company.objects.last().pk + 10
        response = self.client.delete(reverse('company-detail', kwargs={'pk': company_not_exists_pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
