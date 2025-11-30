import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_feed_api.settings')
django.setup()

from users.models import User

# Register a new user
try:
    user = User.objects.create_user(
        username='newuser',
        email='newuser@example.com',
        password='pass123'
    )
    print(f'✓ User created successfully: {user.username} ({user.email})')
except Exception as e:
    print(f'✗ Error creating user: {e}')
