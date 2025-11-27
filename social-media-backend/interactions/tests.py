from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Post
from interactions.models import Like, Comment, CommentLike, Share, Follow, PostView

User = get_user_model()


class LikeModelTests(TestCase):
    """Test cases for the Like model"""

    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
        self.post = Post.objects.create(
            author=self.user1,
            content='Test post'
        )

    def test_create_like(self):
        """Test creating a like"""
        like = Like.objects.create(user=self.user2, post=self.post)
        self.assertEqual(like.user, self.user2)
        self.assertEqual(like.post, self.post)
        self.assertIsNotNone(like.created_at)

    def test_like_str_representation(self):
        """Test the string representation of like"""
        like = Like.objects.create(user=self.user2, post=self.post)
        self.assertIn('user2', str(like))
        self.assertIn(str(self.post.id), str(like))

    def test_unique_user_post_constraint(self):
        """Test that a user can only like a post once"""
        Like.objects.create(user=self.user2, post=self.post)
        with self.assertRaises(Exception):
            Like.objects.create(user=self.user2, post=self.post)


class CommentModelTests(TestCase):
    """Test cases for the Comment model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            content='Test post'
        )

    def test_create_comment(self):
        """Test creating a comment"""
        comment = Comment.objects.create(
            user=self.user,
            post=self.post,
            content='Test comment'
        )
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.content, 'Test comment')
        self.assertIsNone(comment.parent)

    def test_comment_str_representation(self):
        """Test the string representation of comment"""
        comment = Comment.objects.create(
            user=self.user,
            post=self.post,
            content='Test comment'
        )
        self.assertIn('user1', str(comment))

    def test_comment_default_values(self):
        """Test default values for comment"""
        comment = Comment.objects.create(
            user=self.user,
            post=self.post,
            content='Test'
        )
        self.assertEqual(comment.likes_count, 0)
        self.assertFalse(comment.is_edited)

    def test_nested_comment_reply(self):
        """Test creating a reply to a comment"""
        parent_comment = Comment.objects.create(
            user=self.user,
            post=self.post,
            content='Parent comment'
        )
        reply = Comment.objects.create(
            user=self.user,
            post=self.post,
            content='Reply comment',
            parent=parent_comment
        )
        self.assertEqual(reply.parent, parent_comment)
        self.assertIn(reply, parent_comment.replies.all())


class CommentLikeModelTests(TestCase):
    """Test cases for the CommentLike model"""

    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
        self.post = Post.objects.create(
            author=self.user1,
            content='Test post'
        )
        self.comment = Comment.objects.create(
            user=self.user1,
            post=self.post,
            content='Test comment'
        )

    def test_create_comment_like(self):
        """Test creating a comment like"""
        like = CommentLike.objects.create(
            user=self.user2,
            comment=self.comment
        )
        self.assertEqual(like.user, self.user2)
        self.assertEqual(like.comment, self.comment)

    def test_unique_user_comment_constraint(self):
        """Test that a user can only like a comment once"""
        CommentLike.objects.create(user=self.user2, comment=self.comment)
        with self.assertRaises(Exception):
            CommentLike.objects.create(user=self.user2, comment=self.comment)


class ShareModelTests(TestCase):
    """Test cases for the Share model"""

    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
        self.post = Post.objects.create(
            author=self.user1,
            content='Test post'
        )

    def test_create_share(self):
        """Test creating a share"""
        share = Share.objects.create(
            user=self.user2,
            post=self.post,
            share_type='timeline',
            caption='Sharing this post'
        )
        self.assertEqual(share.user, self.user2)
        self.assertEqual(share.post, self.post)
        self.assertEqual(share.share_type, 'timeline')
        self.assertEqual(share.caption, 'Sharing this post')

    def test_share_types(self):
        """Test different share types"""
        for share_type in ['timeline', 'direct', 'external']:
            share = Share.objects.create(
                user=self.user2,
                post=self.post,
                share_type=share_type
            )
            self.assertEqual(share.share_type, share_type)


class FollowModelTests(TestCase):
    """Test cases for the Follow model"""

    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )

    def test_create_follow(self):
        """Test creating a follow relationship"""
        follow = Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )
        self.assertEqual(follow.follower, self.user1)
        self.assertEqual(follow.following, self.user2)

    def test_follow_str_representation(self):
        """Test the string representation of follow"""
        follow = Follow.objects.create(
            follower=self.user1,
            following=self.user2
        )
        self.assertIn('user1', str(follow))
        self.assertIn('user2', str(follow))
        self.assertIn('follows', str(follow))

    def test_unique_follower_following_constraint(self):
        """Test that a user can only follow another user once"""
        Follow.objects.create(follower=self.user1, following=self.user2)
        with self.assertRaises(Exception):
            Follow.objects.create(follower=self.user1, following=self.user2)


class PostViewModelTests(TestCase):
    """Test cases for the PostView model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            content='Test post'
        )

    def test_create_post_view_with_user(self):
        """Test creating a post view with authenticated user"""
        view = PostView.objects.create(
            user=self.user,
            post=self.post,
            ip_address='192.168.1.1'
        )
        self.assertEqual(view.user, self.user)
        self.assertEqual(view.post, self.post)
        self.assertEqual(view.ip_address, '192.168.1.1')

    def test_create_post_view_anonymous(self):
        """Test creating a post view for anonymous user"""
        view = PostView.objects.create(
            post=self.post,
            ip_address='192.168.1.1'
        )
        self.assertIsNone(view.user)
        self.assertEqual(view.post, self.post)
