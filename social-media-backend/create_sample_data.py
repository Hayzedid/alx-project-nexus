import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_feed_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post, PostMedia
from interactions.models import Like, Comment, Share, Follow
from random import choice, randint
from faker import Faker

User = get_user_model()
fake = Faker()

def create_sample_users():
    """Create sample users"""
    users = []
    print("Creating sample users...")
    
    # Create 10 sample users
    for i in range(10):
        username = f"user_{i+1}"
        email = f"user_{i+1}@example.com"
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'bio': fake.sentence(nb_words=10),
                'is_verified': choice([True, False])
            }
        )
        
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created user: {username}")
        
        users.append(user)
    
    return users

def create_sample_posts(users):
    """Create sample posts"""
    posts = []
    print("Creating sample posts...")
    
    content_types = ['text', 'image', 'video', 'mixed']
    privacy_levels = ['public', 'followers', 'private']
    
    for user in users:
        # Create 3-5 posts per user
        for _ in range(randint(3, 5)):
            post = Post.objects.create(
                author=user,
                content=fake.paragraph(nb_sentences=randint(1, 3)),
                content_type=choice(content_types),
                privacy_level=choice(privacy_levels),
                likes_count=randint(0, 50),
                comments_count=randint(0, 20),
                shares_count=randint(0, 10),
                is_pinned=choice([True, False]) if randint(1, 10) == 1 else False
            )
            posts.append(post)
            print(f"Created post by {user.username}")
    
    return posts

def create_sample_interactions(users, posts):
    """Create sample interactions"""
    print("Creating sample interactions...")
    
    # Create follows
    for user in users:
        # Follow 3-7 other users
        follow_count = randint(3, min(7, len(users)-1))
        following_users = [u for u in users if u != user]
        selected_follows = fake.random_elements(elements=following_users, length=follow_count, unique=True)
        
        for follow_user in selected_follows:
            Follow.objects.get_or_create(
                follower=user,
                following=follow_user
            )
            print(f"{user.username} follows {follow_user.username}")
    
    # Update follower/following counts
    for user in users:
        user.followers_count = Follow.objects.filter(following=user).count()
        user.following_count = Follow.objects.filter(follower=user).count()
        user.posts_count = Post.objects.filter(author=user).count()
        user.save()
    
    # Create likes
    for post in posts:
        # 30-70% of users like each post
        like_count = int(len(users) * randint(30, 70) / 100)
        liking_users = fake.random_elements(elements=users, length=like_count, unique=True)
        
        for user in liking_users:
            Like.objects.get_or_create(
                user=user,
                post=post
            )
    
    # Update post like counts
    for post in posts:
        post.likes_count = Like.objects.filter(post=post).count()
        post.save()
    
    # Create comments
    for post in posts:
        # 0-10 comments per post
        comment_count = randint(0, 10)
        
        for _ in range(comment_count):
            commenter = choice(users)
            comment = Comment.objects.create(
                user=commenter,
                post=post,
                content=fake.sentence(nb_words=randint(5, 15)),
                likes_count=randint(0, 10)
            )
            
            # Sometimes add replies
            if randint(1, 3) == 1:
                reply_count = randint(1, 3)
                for _ in range(reply_count):
                    Comment.objects.create(
                        user=choice(users),
                        post=post,
                        parent=comment,
                        content=fake.sentence(nb_words=randint(3, 10)),
                        likes_count=randint(0, 5)
                    )
    
    # Update post comment counts
    for post in posts:
        post.comments_count = Comment.objects.filter(post=post).count()
        post.save()
    
    # Create shares
    for post in posts:
        # 10-30% of users share each post
        share_count = int(len(users) * randint(10, 30) / 100)
        sharing_users = fake.random_elements(elements=users, length=share_count, unique=True)
        
        for user in sharing_users:
            Share.objects.get_or_create(
                user=user,
                post=post,
                defaults={
                    'share_type': choice(['timeline', 'direct', 'external']),
                    'caption': fake.sentence(nb_words=randint(3, 8)) if randint(1, 2) == 1 else ''
                }
            )
    
    # Update post share counts
    for post in posts:
        post.shares_count = Share.objects.filter(post=post).count()
        post.save()
    
    print("Sample interactions created successfully!")

def main():
    """Main function to create all sample data"""
    print("Starting sample data creation...")
    
    # Create users
    users = create_sample_users()
    
    # Create posts
    posts = create_sample_posts(users)
    
    # Create interactions
    create_sample_interactions(users, posts)
    
    print(f"\nSample data creation complete!")
    print(f"Users created: {User.objects.count()}")
    print(f"Posts created: {Post.objects.count()}")
    print(f"Likes created: {Like.objects.count()}")
    print(f"Comments created: {Comment.objects.count()}")
    print(f"Shares created: {Share.objects.count()}")
    print(f"Follows created: {Follow.objects.count()}")
    
    print("\nYou can now test the API with:")
    print("GraphQL Playground: http://localhost:8000/graphql/")
    print("Admin Interface: http://localhost:8000/admin/")
    print("Login credentials: username=user_1, password=password123")

if __name__ == '__main__':
    main()
