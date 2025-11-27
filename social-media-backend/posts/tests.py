from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Post, PostMedia

User = get_user_model()


class PostModelTests(TestCase):
    """Test cases for the Post model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post_data = {
            'author': self.user,
            'content': 'Test post content',
            'content_type': 'text',
            'privacy_level': 'public'
        }

    def test_create_post(self):
        """Test creating a post with valid data"""
        post = Post.objects.create(**self.post_data)
        self.assertEqual(post.content, 'Test post content')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.content_type, 'text')
        self.assertEqual(post.privacy_level, 'public')

    def test_post_str_representation(self):
        """Test the string representation of post"""
        post = Post.objects.create(**self.post_data)
        self.assertIn('testuser', str(post))

    def test_default_post_values(self):
        """Test default values for post fields"""
        post = Post.objects.create(
            author=self.user,
            content='Test'
        )
        self.assertEqual(post.content_type, 'text')
        self.assertEqual(post.privacy_level, 'public')
        self.assertEqual(post.likes_count, 0)
        self.assertEqual(post.comments_count, 0)
        self.assertEqual(post.shares_count, 0)
        self.assertFalse(post.is_pinned)
        self.assertFalse(post.is_edited)

    def test_post_ordering(self):
        """Test that posts are ordered by created_at descending"""
        post1 = Post.objects.create(author=self.user, content='First post')
        post2 = Post.objects.create(author=self.user, content='Second post')
        posts = Post.objects.all()
        self.assertEqual(posts[0], post2)
        self.assertEqual(posts[1], post1)

    def test_post_with_media_url(self):
        """Test creating a post with media URL"""
        data = self.post_data.copy()
        data['media_url'] = 'https://example.com/image.jpg'
        data['content_type'] = 'image'
        post = Post.objects.create(**data)
        self.assertEqual(post.media_url, 'https://example.com/image.jpg')
        self.assertEqual(post.content_type, 'image')

    def test_post_privacy_levels(self):
        """Test different privacy levels"""
        for privacy in ['public', 'followers', 'private']:
            data = self.post_data.copy()
            data['privacy_level'] = privacy
            post = Post.objects.create(**data)
            self.assertEqual(post.privacy_level, privacy)

    def test_post_content_types(self):
        """Test different content types"""
        for content_type in ['text', 'image', 'video', 'mixed']:
            data = self.post_data.copy()
            data['content_type'] = content_type
            post = Post.objects.create(**data)
            self.assertEqual(post.content_type, content_type)

    def test_post_cascade_delete_with_user(self):
        """Test that posts are deleted when user is deleted"""
        post = Post.objects.create(**self.post_data)
        post_id = post.id
        self.user.delete()
        self.assertFalse(Post.objects.filter(id=post_id).exists())


class PostMediaModelTests(TestCase):
    """Test cases for the PostMedia model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            content='Test post'
        )

    def test_post_media_ordering(self):
        """Test that media files are ordered by order field"""
        media1 = PostMedia.objects.create(
            post=self.post,
            media_type='image',
            order=2
        )
        media2 = PostMedia.objects.create(
            post=self.post,
            media_type='image',
            order=1
        )
        media_files = self.post.media_files.all()
        self.assertEqual(media_files[0], media2)
        self.assertEqual(media_files[1], media1)

    def test_post_media_str_representation(self):
        """Test the string representation of post media"""
        media = PostMedia.objects.create(
            post=self.post,
            media_type='image',
            order=1
        )
        self.assertIn('image', str(media))
        self.assertIn(str(self.post.id), str(media))
