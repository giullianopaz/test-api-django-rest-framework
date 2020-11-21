from django.test import TestCase

from apps.users.models import User
from apps.companies.models import Company


class CompanyTest(TestCase):

    def setUp(self):
        user1 = User.objects.create_user(
            username='usertest1',
            first_name='User',
            last_name='Test 1',
            email='test1@test.com',
        )

        user2 = User.objects.create_user(
            username='usertest2',
            first_name='User',
            last_name='Test 2',
            email='test2@test.com',
        )

        company = Company.objects.create(
            name='Company Hero LTDA',
            trading_name='Company Hero',
            registered_number='20240272000176',
            email='contato@companyhero.com',
            phone='9999999999',
        )

        company.employees.add(user1, user2)

    def test_company_creation(self):
        company = Company.objects.get(registered_number='20240272000176')

        self.assertEqual(company.name, 'Company Hero LTDA')
        self.assertEqual(company.trading_name, 'Company Hero')
        self.assertEqual(company.email, 'contato@companyhero.com')
        self.assertEqual(company.phone, '9999999999')


    def test_company_employees(self):
        company = Company.objects.get(registered_number='20240272000176')

        self.assertEqual(company.employees.count(), 2)
