from django.test import TestCase
from django.contrib.auth import authenticate

from apps.users.models import User


class UserTest(TestCase):

    def setUp(self):
        user1 = User.objects.create_user(
            username='usertest1',
            first_name='User',
            last_name='Test 1',
            email='test1@test.com',
        )
        user1.set_password('passuser1')
        user1.save()

        user2 = User.objects.create_user(
            username='usertest2',
            first_name='User',
            last_name='Test 2',
            email='test2@test.com',
        )
        user2.set_password('passuser2')
        user2.save()

    def test_user_creation(self):
        user1 = User.objects.get(username='usertest1')
        user2 = User.objects.get(username='usertest2')

        self.assertEqual(user1.username, 'usertest1')
        self.assertEqual(user1.get_full_name(), 'User Test 1')
        self.assertEqual(user1.email, 'test1@test.com')

        self.assertEqual(user2.username, 'usertest2')
        self.assertEqual(user2.get_full_name(), 'User Test 2')
        self.assertEqual(user2.email, 'test2@test.com')

    def test_user_authentication(self):
        self.assertIsNotNone(authenticate(username='usertest1', password='passuser1'))
        self.assertIsNotNone(authenticate(username='usertest2', password='passuser2'))
