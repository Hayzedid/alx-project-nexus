# Social Media Feed Backend - ProDev BE

A scalable social media feed backend built with Django and GraphQL, designed to handle high-volume user interactions efficiently.

## 🚀 Project Overview

This project implements a complete social media backend with GraphQL API for managing posts, user interactions, and real-time engagement features. It demonstrates best practices for building scalable social platforms.

## 🎯 Project Goals

- **Post Management**: Design APIs for creating, fetching, and managing posts
- **Flexible Querying**: Implement GraphQL for advanced querying capabilities  
- **Scalability**: Optimize database schema for high-volume user interactions
- **Real-time Interactions**: Support likes, comments, shares, and follows

## Real-time Features

The Social Media Feed Backend now supports real-time updates using Django Channels and WebSockets. This enables live notifications, feed updates, and post interactions without needing to refresh the page.

### WebSocket Endpoints

- **Feed Updates**: `ws://localhost:8000/ws/feed/`
  - Receives real-time updates when new posts are created
  
- **User Notifications**: `ws://localhost:8000/ws/notifications/<user_id>/`
  - Receives personalized notifications for likes, comments, and follows
  
- **Post Updates**: `ws://localhost:8000/ws/post/<post_id>/`
  - Receives real-time updates for specific post interactions (likes, comments, shares)

### Real-time Features

1. **Like Notifications**: Users receive instant notifications when someone likes their posts
2. **Comment Notifications**: Real-time alerts when someone comments on posts
3. **Follow Notifications**: Instant updates when someone starts following a user
4. **Feed Updates**: New posts appear in real-time in the feed
5. **Post Interaction Updates**: Like and comment counts update in real-time for posts being viewed

### Testing Real-time Features

1. Open the WebSocket examples page in your browser:
   ```bash
   Open: websocket_examples.html
   ```

2. In another browser window or tab, use the GraphQL Playground to:
   - Create posts (they'll appear in the feed in real-time)
   - Like posts (notifications will be sent to post authors)
   - Comment on posts (real-time comment updates)
   - Follow users (follow notifications will be sent)

### WebSocket Message Formats

#### New Post Notification
```json
{
  "type": "new_post",
  "data": {
    "id": "post_id",
    "content": "Post content",
    "author": {
      "id": "user_id",
      "username": "username",
      "full_name": "Full Name"
    },
    "created_at": "2025-01-01T12:00:00Z",
    "likes_count": 0,
    "comments_count": 0,
    "shares_count": 0
  }
}
```

#### Like Notification
```json
{
  "type": "like",
  "data": {
    "post_id": "post_id",
    "user_id": "user_id",
    "username": "username",
    "full_name": "Full Name",
    "message": "username liked your post"
  }
}
```

#### Comment Notification
```json
{
  "type": "comment",
  "data": {
    "post_id": "post_id",
    "user_id": "user_id",
    "username": "username",
    "full_name": "Full Name",
    "message": "username commented on your post",
    "comment_content": "Comment content..."
  }
}
```

#### Follow Notification
```json
{
  "type": "follow",
  "data": {
    "user_id": "user_id",
    "username": "username",
    "full_name": "Full Name",
    "message": "username started following you",
    "followers_count": 42
  }
}
```

## 🛠 Technologies Used

- **Django 5.2.6**: Backend framework
- **Django Channels**: WebSocket support for real-time features
- **GraphQL (Graphene-Django)**: Flexible data queries
- **SQLite/PostgreSQL**: Database (SQLite for development, PostgreSQL for production)
- **Django REST Framework**: REST API support
- **CORS Headers**: Cross-origin resource sharing
- **Pillow**: Image processing for profile pictures and media

## 🌟 Key Features

### 1. GraphQL APIs
- Flexible querying of posts and interactions
- Resolvers for creating, fetching, and managing posts and interactions
- Optimized queries with proper indexing
- Authentication-aware resolvers

### 2. User Management
- Custom user model with extended profile fields
- User authentication and authorization
- Follow/unfollow functionality
- User search and discovery

### 3. Post Management
- Create posts with text, images, videos, or mixed content
- Privacy levels (public, followers, private)
- Media attachments with thumbnails
- Engagement tracking (likes, comments, shares)

### 4. Interaction System
- Like/unlike posts and comments
- Threaded comments with replies
- Share posts with captions
- Post view tracking for analytics

### 5. Database Optimization
- Proper indexing for high-volume queries
- Optimized GraphQL resolvers
- Efficient relationship handling
- Scalable schema design

## 📁 Project Structure

```
social-media-backend/
├── social_feed_api/          # Main Django project
│   ├── __init__.py
│   ├── settings.py          # Django settings with GraphQL config
│   ├── urls.py              # URL routing with GraphQL endpoint
│   ├── schema.py            # GraphQL schema with queries and mutations
│   └── wsgi.py              # WSGI configuration
├── users/                   # User management app
│   ├── models.py            # Custom User model
│   └── admin.py             # Admin interface configuration
├── posts/                   # Post management app
│   ├── models.py            # Post and PostMedia models
│   └── admin.py             # Admin interface configuration
├── interactions/           # User interactions app
│   ├── models.py            # Like, Comment, Share, Follow models
│   └── admin.py             # Admin interface configuration
├── manage.py                # Django management script
└── requirements.txt         # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd alx-project-nexus/social-media-backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

### Access Points

- **GraphQL Playground**: http://localhost:8000/graphql/
- **Admin Interface**: http://localhost:8000/admin/
- **API Endpoint**: http://localhost:8000/graphql/

## 📊 GraphQL API

### Queries

#### User Queries
```graphql
# Get current user
query {
  me {
    id
    username
    email
    full_name
    bio
    followersCount
    followingCount
    postsCount
    isVerified
  }
}

# Get user by ID
query GetUser($id: ID!) {
  user(id: $id) {
    id
    username
    full_name
    bio
    followersCount
    followingCount
    isFollowing
  }
}

# Search users
query SearchUsers($search: String!) {
  users(search: $search) {
    id
    username
    full_name
    bio
    isVerified
  }
}
```

#### Post Queries
```graphql
# Get feed posts
query GetFeed($limit: Int, $offset: Int) {
  feed(limit: $limit, offset: $offset) {
    id
    content
    contentType
    privacyLevel
    likesCount
    commentsCount
    sharesCount
    isLiked
    isShared
    createdAt
    author {
      id
      username
      full_name
      profilePicture
    }
    mediaFiles {
      id
      mediaType
      file
      thumbnail
      order
    }
  }
}

# Get user posts
query GetUserPosts($userId: ID!) {
  userPosts(userId: $userId) {
    id
    content
    contentType
    privacyLevel
    likesCount
    commentsCount
    createdAt
    author {
      username
      full_name
    }
  }
}
```

#### Interaction Queries
```graphql
# Get post likes
query GetPostLikes($postId: ID!) {
  postLikes(postId: $postId) {
    id
    user {
      username
      full_name
    }
    createdAt
  }
}

# Get post comments
query GetPostComments($postId: ID!) {
  postComments(postId: $postId) {
    id
    content
    likesCount
    isLiked
    isEdited
    createdAt
    author {
      username
      full_name
    }
    replies {
      id
      content
      author {
        username
      }
      createdAt
    }
  }
}
```

### Mutations

#### Post Mutations
```graphql
# Create a post
mutation CreatePost($input: PostInput!) {
  createPost(input: $input) {
    success
    message
    post {
      id
      content
      contentType
      privacyLevel
      createdAt
      author {
        username
      }
    }
  }
}
```

#### Interaction Mutations
```graphql
# Like/unlike a post
mutation LikePost($postId: ID!) {
  likePost(postId: $postId) {
    success
    message
    isLiked
  }
}

# Create a comment
mutation CreateComment($input: CommentInput!) {
  createComment(input: $input) {
    success
    message
    comment {
      id
      content
      createdAt
      author {
        username
      }
    }
  }
}

# Follow/unfollow a user
mutation FollowUser($userId: ID!) {
  followUser(userId: $userId) {
    success
    message
    isFollowing
  }
}
```

## 🗄 Database Schema

### User Model
- Custom user model extending AbstractUser
- Email as unique identifier
- Profile fields (bio, profile picture)
- Social stats (followers, following, posts counts)
- Verification status

### Post Model
- Content with different types (text, image, video, mixed)
- Privacy levels (public, followers, private)
- Engagement counters
- Media attachments
- Timestamps with editing tracking

### Interaction Models
- **Like**: User-post like relationships
- **Comment**: Threaded comments with replies
- **CommentLike**: Likes on comments
- **Share**: Post sharing with captions
- **Follow**: User following relationships
- **PostView**: View tracking for analytics

## 🔧 Configuration

### Database Settings

**Development (SQLite)**: Already configured for easy setup

**Production (PostgreSQL)**:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'social_feed_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### CORS Settings
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
]
```

## 📈 Performance Optimizations

### Database Indexing
- Composite indexes on frequently queried fields
- Optimized for feed generation and interaction queries
- Proper foreign key indexing

### GraphQL Optimizations
- Efficient resolvers with select_related/prefetch_related
- Pagination support for large datasets
- Authentication-aware query optimization

### Caching Strategy
- Model-level caching for user stats
- Query result caching for expensive operations
- Session-based caching for user sessions

## 🧪 Testing

### Running Tests
```bash
python manage.py test
```

### GraphQL Testing
Use the built-in GraphQL Playground at http://localhost:8000/graphql/

### Admin Interface
Access the Django admin at http://localhost:8000/admin/ to:
- Manage users and posts
- Monitor interactions
- View analytics data

## 🚀 Deployment

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### Production Setup
1. Set DEBUG=False
2. Configure PostgreSQL database
3. Set up proper CORS origins
4. Configure static file serving
5. Set up SSL certificate

## 📝 Git Commit Workflow

```
feat: set up Django project with PostgreSQL
feat: create models for posts, comments, and interactions  
feat: implement GraphQL API for querying posts and interactions
feat: integrate and publish GraphQL Playground
perf: optimize database queries for interactions
docs: update README with API usage
```

## 🏆 Evaluation Criteria

### Functionality
- ✅ Fully functional GraphQL APIs for posts and interactions
- ✅ High-performing queries for large datasets
- ✅ Complete CRUD operations for all entities

### Code Quality
- ✅ Clean and modular code structure
- ✅ Efficient database schema design
- ✅ Proper error handling and validation

### User Experience
- ✅ Intuitive GraphQL Playground interface
- ✅ Comprehensive API documentation
- ✅ Easy-to-use admin interface

### Version Control
- ✅ Frequent and clear commits
- ✅ Organized project repository
- ✅ Proper branching strategy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of the ProDev Backend Engineering program.

---

**Built with ❤️ for ProDev Backend Engineering**
