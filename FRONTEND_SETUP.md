# Social Media Frontend Setup

## Overview
Building a modern React frontend for the social media backend with:
- GraphQL queries and mutations
- Real-time WebSocket support
- User authentication
- Post feed with interactions
- User profiles
- Responsive design

## Technology Stack
- **Framework:** React 18
- **State Management:** Apollo Client (GraphQL)
- **Styling:** Tailwind CSS + Shadcn/UI
- **Real-time:** WebSocket via Apollo
- **HTTP Client:** Apollo Client
- **Icons:** Lucide React
- **Forms:** React Hook Form

## Project Structure
```
social-media-frontend/
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── LoginForm.jsx
│   │   │   ├── RegisterForm.jsx
│   │   │   └── AuthContext.jsx
│   │   ├── Feed/
│   │   │   ├── PostFeed.jsx
│   │   │   ├── PostCard.jsx
│   │   │   └── CreatePost.jsx
│   │   ├── Profile/
│   │   │   ├── UserProfile.jsx
│   │   │   └── ProfileHeader.jsx
│   │   ├── Common/
│   │   │   ├── Navbar.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── Loading.jsx
│   │   └── Interactions/
│   │       ├── LikeButton.jsx
│   │       ├── CommentSection.jsx
│   │       └── ShareButton.jsx
│   ├── graphql/
│   │   ├── queries.js
│   │   ├── mutations.js
│   │   └── subscriptions.js
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── usePosts.js
│   │   └── useUser.js
│   ├── utils/
│   │   ├── apolloClient.js
│   │   ├── constants.js
│   │   └── helpers.js
│   ├── App.jsx
│   └── index.css
├── package.json
└── .env.example
```

## Installation Steps

### 1. Create React App
```bash
npx create-react-app social-media-frontend
cd social-media-frontend
```

### 2. Install Dependencies
```bash
npm install @apollo/client graphql
npm install @tanstack/react-query
npm install tailwindcss postcss autoprefixer
npm install -D shadcn-ui
npm install lucide-react
npm install react-hook-form
npm install axios
npm install react-router-dom
npm install zustand
```

### 3. Configure Tailwind CSS
```bash
npx tailwindcss init -p
```

### 4. Setup Environment Variables
Create `.env` file:
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GRAPHQL_URL=http://localhost:8000/graphql/
REACT_APP_WS_URL=ws://localhost:8001
```

## Key Features to Implement

### Authentication
- [ ] User registration
- [ ] User login
- [ ] JWT token storage
- [ ] Protected routes
- [ ] Logout functionality

### Feed
- [ ] Display posts from followed users
- [ ] Create new posts
- [ ] Like/unlike posts
- [ ] Comment on posts
- [ ] Share posts
- [ ] Infinite scroll/pagination

### User Profiles
- [ ] View user profile
- [ ] Edit profile
- [ ] Follow/unfollow users
- [ ] View follower/following lists
- [ ] User's posts

### Real-time Features
- [ ] Live notifications
- [ ] Real-time post updates
- [ ] Live comment updates
- [ ] Typing indicators

### UI/UX
- [ ] Responsive design
- [ ] Dark mode support
- [ ] Loading states
- [ ] Error handling
- [ ] Toast notifications

## API Integration

### GraphQL Queries
```graphql
query GetFeed {
  feed(limit: 20, offset: 0) {
    id
    content
    author {
      id
      username
      profilePicture
    }
    likesCount
    commentsCount
    isLiked
    createdAt
  }
}

query GetUser($id: ID!) {
  user(id: $id) {
    id
    username
    email
    bio
    profilePicture
    followersCount
    followingCount
    isFollowing
  }
}
```

### GraphQL Mutations
```graphql
mutation CreatePost($content: String!) {
  createPost(content: $content) {
    post {
      id
      content
      author {
        id
        username
      }
      createdAt
    }
    success
    message
  }
}

mutation LikePost($postId: ID!) {
  likePost(postId: $postId) {
    success
    message
  }
}
```

## Development Server

```bash
npm start
```

Server runs at: `http://localhost:3000`

## Build for Production

```bash
npm run build
```

## Deployment Options

### Netlify
```bash
npm run build
netlify deploy --prod --dir=build
```

### Vercel
```bash
vercel
```

### GitHub Pages
```bash
npm run build
npm run deploy
```

## Demo Video Script

### Scene 1: Authentication (0:00-0:30)
- Show login page
- Enter credentials
- Successful login
- Redirect to feed

### Scene 2: Feed & Posts (0:30-1:30)
- Display feed with multiple posts
- Show post interactions (like, comment)
- Create new post
- Real-time update

### Scene 3: User Profile (1:30-2:30)
- Navigate to user profile
- Show profile information
- Display user's posts
- Follow/unfollow functionality

### Scene 4: Interactions (2:30-3:30)
- Like a post
- Add comment
- Reply to comment
- Share post

### Scene 5: Best Practices (3:30-5:00)
- Show GraphQL query structure
- Explain error handling
- Demonstrate validation
- Show authentication flow
- Explain real-time updates

## Testing

### Unit Tests
```bash
npm test
```

### E2E Tests
```bash
npm run cypress
```

## Performance Optimization

- [ ] Code splitting
- [ ] Lazy loading
- [ ] Image optimization
- [ ] Caching strategies
- [ ] Bundle size optimization

## Security Considerations

- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Secure token storage
- [ ] Input validation
- [ ] Rate limiting

## Next Steps

1. Create React app
2. Install dependencies
3. Setup Tailwind CSS
4. Create authentication components
5. Implement GraphQL queries/mutations
6. Build feed components
7. Add real-time features
8. Record demo video
9. Deploy to production

---

**Status:** Ready to start building 🚀
