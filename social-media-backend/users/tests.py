from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserModelTests(TestCase):
    """Test cases for the User model"""

    def setUp(self):
        """Set up test data"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'bio': 'Test bio'
        }

    def test_create_user(self):
        """Test creating a user with valid data"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.bio, 'Test bio')

    def test_user_str_representation(self):
        """Test the string representation of user"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), '@testuser')

    def test_user_full_name_property(self):
        """Test the full_name property"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.full_name, 'Test User')

    def test_user_full_name_without_names(self):
        """Test full_name when first and last names are not provided"""
        data = self.user_data.copy()
        data['first_name'] = ''
        data['last_name'] = ''
        user = User.objects.create_user(**data)
        self.assertEqual(user.full_name, '')

    def test_unique_email_constraint(self):
        """Test that email must be unique"""
        User.objects.create_user(**self.user_data)
        
        duplicate_data = self.user_data.copy()
        duplicate_data['username'] = 'differentuser'
        
        with self.assertRaises(Exception):
            User.objects.create_user(**duplicate_data)

    def test_unique_username_constraint(self):
        """Test that username must be unique"""
        User.objects.create_user(**self.user_data)
        
        duplicate_data = self.user_data.copy()
        duplicate_data['email'] = 'different@example.com'
        
        with self.assertRaises(Exception):
            User.objects.create_user(**duplicate_data)

    def test_default_field_values(self):
        """Test default values for model fields"""
        user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='pass123'
        )
        self.assertEqual(user.followers_count, 0)
        self.assertEqual(user.following_count, 0)
        self.assertEqual(user.posts_count, 0)
        self.assertFalse(user.is_verified)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_username_field_is_email(self):
        """Test that USERNAME_FIELD is set to email"""
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_user_authentication(self):
        """Test user authentication"""
        user = User.objects.create_user(**self.user_data)
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.check_password('wrongpassword'))

    def test_create_superuser(self):
        """Test creating a superuser"""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
