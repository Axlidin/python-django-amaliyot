from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegisterTestCase(TestCase):

    def test_CustomUser_is_created(self):
        self.client.post(
            reverse('users:register'),
            data={
                 'username': 'axlidin',
                 'first_name': 'Test',
                 'last_name': 'CustomUser',
                 'email': 'testCustomUser@example.com',
                 'password': 'test123'
             }
        )

        user = CustomUser.objects.get(username='axlidin')

        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'CustomUser')
        self.assertEqual(user.email, 'testCustomUser@example.com')
        # self.assertEqual(user.password, 'test123')
        self.assertNotEquals(user.password, 'test123')
        self.assertTrue(user.check_password, 'test123')

    def test_invalid_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'first_name': 'Test',
                'email': 'testCustomUser',
            }
        )
        CustomUser_count = CustomUser.objects.count()
        self.assertEqual(CustomUser_count, 0)
        form = response.context.get('form')
        self.assertTrue(form)
        self.assertFormError(form, 'username', 'This field is required.')
        self.assertFormError(form, 'password', 'This field is required.')
        self.assertFormError(form, 'email', 'Enter a valid email address.')

    def test_CustomUsername_is_exist(self):
        user = CustomUser.objects.create_user(username='axlidin',
                                        first_name='Test')
        user.set_password('pasword')
        user.save()

        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'axlidin',
                'first_name': 'Test',
                'last_name': 'CustomUser',
                'email': 'testCustomUser@example.com',
                'password': 'test123'
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count,1)
        # CustomUser_exists = CustomUser.objects.filter(username='axlidin').exists()
        # self.assertTrue(CustomUser_exists)
        # self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')

class LoginFormTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create_user(username='testCustomUser',
                                      first_name='name')
        self.db_user.set_password('test123')
        self.db_user.save()

    def test_login_successfull_CustomUser(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'testCustomUser',
                'password': 'test123'
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wronw_states(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'wrong_CustomUser',
                'password': 'test123'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'testCustomUser',
                'password': 'wrong_password'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username='testCustomUser', password='test123')
        self.client.get(reverse('users:logout'))
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.url, reverse('users:login') + '?next=/users/profile/')
        self.assertEqual(response.status_code, 302)

    def test_profile_details(self):
        user = CustomUser.objects.create_user(
            username='testCustomUser',
            first_name='Test',
            last_name='CustomUser',
            email='testCustomUser@example.com',
        )
        user.set_password('test123')
        user.save()
        self.client.login(username='testCustomUser', password='test123')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create_user(
            username='testCustomUser',
            first_name='Test',
            last_name='CustomUser',
            email='testCustomUser@example.com',
        )
        user.set_password('test123')
        user.save()

        self.client.login(username='testCustomUser', password='test123')

        response = self.client.post(reverse('users:profile-edit'),
                    data={
                        'username': 'new_testCustomUser',
                        'first_name': 'New',
                        'last_name': 'Test',
                        'email': 'new_testCustomUser@example.com'
                    }
                                    )
        # user = user.objects.get(pk=CustomUser.pk)
        user.refresh_from_db()
        self.assertEqual(user.username, 'new_testCustomUser')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(response.url, reverse('users:profile'))