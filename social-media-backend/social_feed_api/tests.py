from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Post
from interactions.models import Like, Comment, Follow
import json

User = get_user_model()


class GraphQLAPITests(TestCase):
    """Test cases for GraphQL API"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User1'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User2'
        )
        self.post1 = Post.objects.create(
            author=self.user1,
            content='Test post 1',
            privacy_level='public'
        )
        self.post2 = Post.objects.create(
            author=self.user2,
            content='Test post 2',
            privacy_level='public'
        )

    def execute_query(self, query, variables=None):
        """Helper method to execute GraphQL queries"""
        response = self.client.post(
            '/graphql/',
            data=json.dumps({'query': query, 'variables': variables or {}}),
            content_type='application/json'
        )
        return json.loads(response.content)

    def test_query_all_posts(self):
        """Test querying all posts"""
        query = '''
            query {
                posts(limit: 10, offset: 0) {
                    id
                    content
                    author {
                        username
                    }
                    likesCount
                    commentsCount
                }
            }
        '''
        result = self.execute_query(query)
        self.assertIn('data', result)
        self.assertIn('posts', result['data'])
        self.assertEqual(len(result['data']['posts']), 2)

    def test_query_single_post(self):
        """Test querying a single post by ID"""
        query = '''
            query GetPost($id: ID!) {
                post(id: $id) {
                    id
                    content
                    author {
                        username
                    }
                }
            }
        '''
        result = self.execute_query(query, {'id': str(self.post1.id)})
        self.assertIn('data', result)
        self.assertEqual(result['data']['post']['content'], 'Test post 1')
        self.assertEqual(result['data']['post']['author']['username'], 'testuser1')

    def test_query_user_by_id(self):
        """Test querying a user by ID"""
        query = '''
            query GetUser($id: ID!) {
                user(id: $id) {
                    id
                    username
                    email
                    fullName
                    followersCount
                    followingCount
                }
            }
        '''
        result = self.execute_query(query, {'id': str(self.user1.id)})
        self.assertIn('data', result)
        self.assertEqual(result['data']['user']['username'], 'testuser1')
        self.assertEqual(result['data']['user']['email'], 'test1@example.com')
        self.assertEqual(result['data']['user']['fullName'], 'Test User1')

    def test_query_users_search(self):
        """Test searching users"""
        query = '''
            query SearchUsers($search: String) {
                users(search: $search) {
                    username
                    email
                }
            }
        '''
        result = self.execute_query(query, {'search': 'testuser1'})
        self.assertIn('data', result)
        self.assertTrue(len(result['data']['users']) > 0)
        self.assertEqual(result['data']['users'][0]['username'], 'testuser1')

    def test_query_user_posts(self):
        """Test querying posts by user"""
        query = '''
            query GetUserPosts($userId: ID!) {
                userPosts(userId: $userId) {
                    id
                    content
                    author {
                        username
                    }
                }
            }
        '''
        result = self.execute_query(query, {'userId': str(self.user1.id)})
        self.assertIn('data', result)
        self.assertEqual(len(result['data']['userPosts']), 1)
        self.assertEqual(result['data']['userPosts'][0]['content'], 'Test post 1')

    def test_mutation_register_user(self):
        """Test user registration mutation"""
        mutation = '''
            mutation RegisterUser($input: RegisterInput!) {
                registerUser(input: $input) {
                    success
                    message
                    user {
                        username
                        email
                    }
                }
            }
        '''
        variables = {
            'input': {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'newpass123',
                'firstName': 'New',
                'lastName': 'User'
            }
        }
        result = self.execute_query(mutation, variables)
        self.assertIn('data', result)
        self.assertTrue(result['data']['registerUser']['success'])
        self.assertEqual(result['data']['registerUser']['user']['username'], 'newuser')

    def test_mutation_create_post_without_auth(self):
        """Test creating a post without authentication"""
        mutation = '''
            mutation CreatePost($input: PostInput!) {
                createPost(input: $input) {
                    success
                    message
                }
            }
        '''
        variables = {
            'input': {
                'content': 'New post content',
                'contentType': 'text',
                'privacyLevel': 'public'
            }
        }
        result = self.execute_query(mutation, variables)
        self.assertIn('data', result)
        self.assertFalse(result['data']['createPost']['success'])
        self.assertIn('Authentication required', result['data']['createPost']['message'])

    def test_mutation_create_post_with_auth(self):
        """Test creating a post with authentication"""
        self.client.force_login(self.user1)
        mutation = '''
            mutation CreatePost($input: PostInput!) {
                createPost(input: $input) {
                    success
                    message
                    post {
                        id
                        content
                        author {
                            username
                        }
                    }
                }
            }
        '''
        variables = {
            'input': {
                'content': 'New authenticated post',
                'contentType': 'text',
                'privacyLevel': 'public'
            }
        }
        result = self.execute_query(mutation, variables)
        self.assertIn('data', result)
        self.assertTrue(result['data']['createPost']['success'])
        self.assertEqual(result['data']['createPost']['post']['content'], 'New authenticated post')

    def test_mutation_like_post(self):
        """Test liking a post"""
        self.client.force_login(self.user2)
        mutation = '''
            mutation LikePost($postId: ID!) {
                likePost(postId: $postId) {
                    success
                    message
                    isLiked
                }
            }
        '''
        result = self.execute_query(mutation, {'postId': str(self.post1.id)})
        self.assertIn('data', result)
        self.assertTrue(result['data']['likePost']['success'])
        self.assertTrue(result['data']['likePost']['isLiked'])

    def test_mutation_unlike_post(self):
        """Test unliking a post"""
        self.client.force_login(self.user2)
        # First like the post
        Like.objects.create(user=self.user2, post=self.post1)
        
        mutation = '''
            mutation LikePost($postId: ID!) {
                likePost(postId: $postId) {
                    success
                    message
                    isLiked
                }
            }
        '''
        result = self.execute_query(mutation, {'postId': str(self.post1.id)})
        self.assertIn('data', result)
        self.assertTrue(result['data']['likePost']['success'])
        self.assertFalse(result['data']['likePost']['isLiked'])

    def test_mutation_create_comment(self):
        """Test creating a comment"""
        self.client.force_login(self.user2)
        mutation = '''
            mutation CreateComment($input: CommentInput!) {
                createComment(input: $input) {
                    success
                    message
                    comment {
                        id
                        content
                        author {
                            username
                        }
                    }
                }
            }
        '''
        variables = {
            'input': {
                'postId': str(self.post1.id),
                'content': 'Test comment on post'
            }
        }
        result = self.execute_query(mutation, variables)
        self.assertIn('data', result)
        self.assertTrue(result['data']['createComment']['success'])
        self.assertEqual(result['data']['createComment']['comment']['content'], 'Test comment on post')

    def test_mutation_follow_user(self):
        """Test following a user"""
        self.client.force_login(self.user1)
        mutation = '''
            mutation FollowUser($userId: ID!) {
                followUser(userId: $userId) {
                    success
                    message
                    isFollowing
                }
            }
        '''
        result = self.execute_query(mutation, {'userId': str(self.user2.id)})
        self.assertIn('data', result)
        self.assertTrue(result['data']['followUser']['success'])
        self.assertTrue(result['data']['followUser']['isFollowing'])

    def test_mutation_unfollow_user(self):
        """Test unfollowing a user"""
        self.client.force_login(self.user1)
        # First follow the user
        Follow.objects.create(follower=self.user1, following=self.user2)
        
        mutation = '''
            mutation FollowUser($userId: ID!) {
                followUser(userId: $userId) {
                    success
                    message
                    isFollowing
                }
            }
        '''
        result = self.execute_query(mutation, {'userId': str(self.user2.id)})
        self.assertIn('data', result)
        self.assertTrue(result['data']['followUser']['success'])
        self.assertFalse(result['data']['followUser']['isFollowing'])

    def test_query_post_likes(self):
        """Test querying likes for a post"""
        Like.objects.create(user=self.user2, post=self.post1)
        
        query = '''
            query GetPostLikes($postId: ID!) {
                postLikes(postId: $postId) {
                    user {
                        username
                    }
                    createdAt
                }
            }
        '''
        result = self.execute_query(query, {'postId': str(self.post1.id)})
        self.assertIn('data', result)
        self.assertEqual(len(result['data']['postLikes']), 1)
        self.assertEqual(result['data']['postLikes'][0]['user']['username'], 'testuser2')

    def test_query_post_comments(self):
        """Test querying comments for a post"""
        Comment.objects.create(
            user=self.user2,
            post=self.post1,
            content='Test comment'
        )
        
        query = '''
            query GetPostComments($postId: ID!) {
                postComments(postId: $postId) {
                    content
                    author {
                        username
                    }
                }
            }
        '''
        result = self.execute_query(query, {'postId': str(self.post1.id)})
        self.assertIn('data', result)
        self.assertEqual(len(result['data']['postComments']), 1)
        self.assertEqual(result['data']['postComments'][0]['content'], 'Test comment')

    def test_query_user_followers(self):
        """Test querying user followers"""
        Follow.objects.create(follower=self.user2, following=self.user1)
        
        query = '''
            query GetUserFollowers($userId: ID!) {
                userFollowers(userId: $userId) {
                    username
                }
            }
        '''
        result = self.execute_query(query, {'userId': str(self.user1.id)})
        self.assertIn('data', result)
        self.assertEqual(len(result['data']['userFollowers']), 1)
        self.assertEqual(result['data']['userFollowers'][0]['username'], 'testuser2')

    def test_query_user_following(self):
        """Test querying users that a user is following"""
        Follow.objects.create(follower=self.user1, following=self.user2)
        
        query = '''
            query GetUserFollowing($userId: ID!) {
                userFollowing(userId: $userId) {
                    username
                }
            }
        '''
        result = self.execute_query(query, {'userId': str(self.user1.id)})
        self.assertIn('data', result)
        self.assertEqual(len(result['data']['userFollowing']), 1)
        self.assertEqual(result['data']['userFollowing'][0]['username'], 'testuser2')

    def test_query_feed_without_auth(self):
        """Test querying feed without authentication"""
        query = '''
            query GetFeed {
                feed(limit: 10, offset: 0) {
                    id
                    content
                }
            }
        '''
        result = self.execute_query(query)
        self.assertIn('data', result)
        self.assertEqual(result['data']['feed'], [])

    def test_query_feed_with_auth(self):
        """Test querying feed with authentication"""
        self.client.force_login(self.user1)
        Follow.objects.create(follower=self.user1, following=self.user2)
        
        query = '''
            query GetFeed {
                feed(limit: 10, offset: 0) {
                    id
                    content
                    author {
                        username
                    }
                }
            }
        '''
        result = self.execute_query(query)
        self.assertIn('data', result)
        self.assertTrue(len(result['data']['feed']) > 0)
