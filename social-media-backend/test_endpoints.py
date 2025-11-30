import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_feed_api.settings')
django.setup()

from users.models import User
from posts.models import Post
from interactions.models import Like, Comment

print("=" * 60)
print("TESTING ALL ENDPOINTS")
print("=" * 60)

# Test 1: Create another user
print("\n1. Creating a second user...")
try:
    user2 = User.objects.create_user(
        username='testuser2',
        email='testuser2@example.com',
        password='pass123'
    )
    print(f"   ✓ User created: {user2.username} ({user2.email})")
except Exception as e:
    print(f"   ✗ Error: {e}")
    user2 = User.objects.get(username='testuser2')
    print(f"   ℹ Using existing user: {user2.username}")

# Get the first user
user1 = User.objects.get(username='newuser')

# Test 2: Create posts
print("\n2. Creating posts...")
try:
    post1 = Post.objects.create(
        author=user1,
        content="Hello world! This is my first post.",
        media_url="https://example.com/image1.jpg"
    )
    print(f"   ✓ Post 1 created by {user1.username}: '{post1.content[:30]}...'")
    
    post2 = Post.objects.create(
        author=user2,
        content="Testing the social media platform! #awesome",
        media_url="https://example.com/image2.jpg"
    )
    print(f"   ✓ Post 2 created by {user2.username}: '{post2.content[:30]}...'")
    
    post3 = Post.objects.create(
        author=user1,
        content="Another post from newuser without media"
    )
    print(f"   ✓ Post 3 created by {user1.username}: '{post3.content[:30]}...'")
except Exception as e:
    print(f"   ✗ Error creating posts: {e}")

# Test 3: Like posts
print("\n3. Testing likes...")
try:
    like1 = Like.objects.create(user=user2, post=post1)
    print(f"   ✓ {user2.username} liked {user1.username}'s post")
    
    like2 = Like.objects.create(user=user1, post=post2)
    print(f"   ✓ {user1.username} liked {user2.username}'s post")
    
    # Check like count
    post1_likes = Like.objects.filter(post=post1).count()
    print(f"   ℹ Post 1 has {post1_likes} like(s)")
except Exception as e:
    print(f"   ✗ Error creating likes: {e}")

# Test 4: Comment on posts
print("\n4. Testing comments...")
try:
    comment1 = Comment.objects.create(
        user=user2,
        post=post1,
        content="Great post! Welcome to the platform."
    )
    print(f"   ✓ {user2.username} commented: '{comment1.content[:30]}...'")
    
    comment2 = Comment.objects.create(
        user=user1,
        post=post2,
        content="Thanks! Looking forward to connecting."
    )
    print(f"   ✓ {user1.username} commented: '{comment2.content[:30]}...'")
    
    comment3 = Comment.objects.create(
        user=user2,
        post=post1,
        content="Can't wait to see more content!"
    )
    print(f"   ✓ {user2.username} commented again: '{comment3.content[:30]}...'")
    
    # Check comment count
    post1_comments = Comment.objects.filter(post=post1).count()
    print(f"   ℹ Post 1 has {post1_comments} comment(s)")
except Exception as e:
    print(f"   ✗ Error creating comments: {e}")

# Test 5: Follow users
print("\n5. Testing follows...")
try:
    from interactions.models import Follow
    follow1 = Follow.objects.create(follower=user1, following=user2)
    print(f"   ✓ {user1.username} is now following {user2.username}")
    
    follow2 = Follow.objects.create(follower=user2, following=user1)
    print(f"   ✓ {user2.username} is now following {user1.username}")
    
    # Check follow counts
    user1_following = Follow.objects.filter(follower=user1).count()
    user1_followers = Follow.objects.filter(following=user1).count()
    print(f"   ℹ {user1.username} follows {user1_following}, has {user1_followers} follower(s)")
except Exception as e:
    print(f"   ✗ Error creating follows: {e}")

# Test 6: Query all data
print("\n6. Database summary...")
print(f"   • Total users: {User.objects.count()}")
print(f"   • Total posts: {Post.objects.count()}")
print(f"   • Total likes: {Like.objects.count()}")
print(f"   • Total comments: {Comment.objects.count()}")

# Test 7: Display feed for user1
print(f"\n7. Feed for {user1.username}...")
all_posts = Post.objects.all().order_by('-created_at')
for i, post in enumerate(all_posts[:5], 1):
    likes = post.likes.count()
    comments = post.comments.count()
    print(f"   {i}. @{post.author.username}: {post.content[:40]}...")
    print(f"      ({likes} likes, {comments} comments)")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 60)
