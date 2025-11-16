# GraphQL API Examples

This file contains example queries and mutations for testing the Social Media Feed Backend API.

## 🚀 Getting Started

Access the GraphQL Playground at: http://localhost:8000/graphql/

## 🔐 Authentication

### Register a New User
```graphql
mutation RegisterUser {
  registerUser(input: {
    username: "newuser"
    email: "newuser@example.com"
    password: "password123"
    firstName: "John"
    lastName: "Doe"
    bio: "I love social media!"
  }) {
    success
    message
    user {
      id
      username
      email
      fullName
      bio
    }
  }
}
```

### Login
```graphql
mutation LoginUser {
  loginUser(input: {
    username: "user_1"
    password: "password123"
  }) {
    success
    message
    user {
      id
      username
      email
      fullName
      followersCount
      followingCount
    }
  }
}
```

### Logout
```graphql
mutation LogoutUser {
  logoutUser {
    success
    message
  }
}
```

## 👤 User Queries

### Get Current User
```graphql
query GetCurrentUser {
  me {
    id
    username
    email
    fullName
    bio
    profilePicture
    followersCount
    followingCount
    postsCount
    isVerified
    createdAt
  }
}
```

### Get User by ID
```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    username
    fullName
    bio
    profilePicture
    followersCount
    followingCount
    postsCount
    isVerified
    isFollowing
    mutualFollowers {
      username
      fullName
    }
  }
}
```

*Variables:*
```json
{
  "id": "1"
}
```

### Search Users
```graphql
query SearchUsers($search: String!) {
  users(search: $search) {
    id
    username
    fullName
    bio
    profilePicture
    isVerified
    followersCount
  }
}
```

*Variables:*
```json
{
  "search": "user"
}
```

## 📝 Post Queries

### Get Feed Posts
```graphql
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
    isPinned
    isEdited
    createdAt
    updatedAt
    author {
      id
      username
      fullName
      profilePicture
      isVerified
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
```

*Variables:*
```json
{
  "limit": 10,
  "offset": 0
}
```

### Get Public Posts
```graphql
query GetPosts($limit: Int, $offset: Int) {
  posts(limit: $limit, offset: $offset) {
    id
    content
    contentType
    privacyLevel
    likesCount
    commentsCount
    sharesCount
    createdAt
    author {
      username
      fullName
      profilePicture
    }
  }
}
```

### Get User Posts
```graphql
query GetUserPosts($userId: ID!) {
  userPosts(userId: $userId) {
    id
    content
    contentType
    privacyLevel
    likesCount
    commentsCount
    sharesCount
    createdAt
    author {
      username
      fullName
    }
  }
}
```

*Variables:*
```json
{
  "userId": "1"
}
```

### Get Single Post
```graphql
query GetPost($id: ID!) {
  post(id: $id) {
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
      username
      fullName
      profilePicture
    }
    comments {
      id
      content
      likesCount
      isLiked
      isEdited
      createdAt
      author {
        username
        fullName
      }
      replies {
        id
        content
        createdAt
        author {
          username
        }
      }
    }
  }
}
```

*Variables:*
```json
{
  "id": "1"
}
```

## 💬 Interaction Queries

### Get Post Likes
```graphql
query GetPostLikes($postId: ID!) {
  postLikes(postId: $postId) {
    id
    user {
      username
      fullName
      profilePicture
    }
    createdAt
  }
}
```

*Variables:*
```json
{
  "postId": "1"
}
```

### Get Post Comments
```graphql
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
      fullName
      profilePicture
    }
    replies {
      id
      content
      likesCount
      isLiked
      createdAt
      author {
        username
      }
    }
  }
}
```

### Get User Followers
```graphql
query GetUserFollowers($userId: ID!) {
  userFollowers(userId: $userId) {
    id
    username
    fullName
    profilePicture
    isVerified
  }
}
```

### Get User Following
```graphql
query GetUserFollowing($userId: ID!) {
  userFollowing(userId: $userId) {
    id
    username
    fullName
    profilePicture
    isVerified
  }
}
```

## ✏️ Post Mutations

### Create a Post
```graphql
mutation CreatePost {
  createPost(input: {
    content: "Hello world! This is my first post on this amazing platform. 🚀"
    contentType: "text"
    privacyLevel: "public"
  }) {
    success
    message
    post {
      id
      content
      contentType
      privacyLevel
      likesCount
      commentsCount
      sharesCount
      createdAt
      author {
        username
        fullName
      }
    }
  }
}
```

### Create a Post with Media
```graphql
mutation CreatePostWithMedia {
  createPost(input: {
    content: "Check out this amazing photo! 📸"
    contentType: "image"
    privacyLevel: "public"
    mediaUrl: "https://example.com/image.jpg"
  }) {
    success
    message
    post {
      id
      content
      contentType
      mediaUrl
      createdAt
    }
  }
}
```

## ❤️ Interaction Mutations

### Like/Unlike a Post
```graphql
mutation LikePost($postId: ID!) {
  likePost(postId: $postId) {
    success
    message
    isLiked
  }
}
```

*Variables:*
```json
{
  "postId": "1"
}
```

### Create a Comment
```graphql
mutation CreateComment {
  createComment(input: {
    postId: "1"
    content: "Great post! I really enjoyed reading this. 👍"
  }) {
    success
    message
    comment {
      id
      content
      likesCount
      isLiked
      createdAt
      author {
        username
        fullName
      }
    }
  }
}
```

### Reply to a Comment
```graphql
mutation CreateReply {
  createComment(input: {
    postId: "1"
    content: "Thanks! I appreciate your response."
    parentId: "1"
  }) {
    success
    message
    comment {
      id
      content
      createdAt
      author {
        username
      }
      parent {
        id
        content
        author {
          username
        }
      }
    }
  }
}
```

### Follow/Unfollow a User
```graphql
mutation FollowUser($userId: ID!) {
  followUser(userId: $userId) {
    success
    message
    isFollowing
  }
}
```

*Variables:*
```json
{
  "userId": "2"
}
```

## 🔄 Complex Queries

### Get Feed with Full Details
```graphql
query GetDetailedFeed {
  feed(limit: 5) {
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
      fullName
      profilePicture
      isVerified
      followersCount
      followingCount
      isFollowing
    }
    comments(limit: 3) {
      id
      content
      likesCount
      isLiked
      createdAt
      author {
        username
        fullName
      }
    }
  }
}
```

### Get User Profile with Posts
```graphql
query GetUserProfile($username: String!) {
  users(search: $username) {
    id
    username
    fullName
    bio
    profilePicture
    followersCount
    followingCount
    postsCount
    isVerified
    isFollowing
  }
}
```

*Variables:*
```json
{
  "username": "user_1"
}
```

## 🧪 Testing Workflow

1. **Register/Login**: First authenticate yourself
2. **Create Posts**: Add some content to the platform
3. **Interact**: Like, comment, and follow other users
4. **Explore**: Check your feed and discover new content

## 📝 Sample Test Data

The database is pre-populated with:
- **11 users** (user_1 through user_10 + admin)
- **38 posts** with various content types
- **175 likes** across posts
- **293 comments** including replies
- **56 shares** with different types
- **48 follow relationships**

**Test Login**: username: `user_1`, password: `password123`

## 🚀 Advanced Features

### Pagination
Use `limit` and `offset` parameters for large datasets:
```graphql
query GetPaginatedFeed($limit: Int!, $offset: Int!) {
  feed(limit: $limit, offset: $offset) {
    id
    content
    createdAt
    author {
      username
    }
  }
}
```

### Search and Filter
Combine search with pagination:
```graphql
query SearchAndPaginate($search: String!, $limit: Int!, $offset: Int!) {
  users(search: $search) {
    id
    username
    fullName
    followersCount
  }
  posts(limit: $limit, offset: $offset) {
    id
    content
    author {
      username
    }
  }
}
```

---

**Happy coding! 🎉**
