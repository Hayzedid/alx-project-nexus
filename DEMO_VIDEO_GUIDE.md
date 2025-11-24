# Demo Video Guide (5 Minutes Max)

## Video Structure & Script

### Total Duration: 5 minutes
- Introduction: 30 seconds
- API Demo: 2 minutes
- Frontend Demo: 2 minutes
- Best Practices: 30 seconds

---

## Scene 1: Introduction (0:00-0:30)

**What to show:**
- Project title: "Social Media Backend API"
- Brief overview of what the app does
- Technologies used (Django, GraphQL, React)

**Script:**
> "Hello! I'm demonstrating a full-stack social media application built with Django, GraphQL, and React. This project showcases modern backend architecture with real-time capabilities and a responsive frontend. Let me walk you through the key features and best practices I've implemented."

**Visual:**
- Show project repository
- Display architecture diagram (from ERD_DIAGRAM.html)
- Show tech stack logos

---

## Scene 2: API Demo with Postman (0:30-2:30)

### 2.1: GraphQL Endpoint Overview (0:30-0:50)

**What to show:**
- Open Postman
- Navigate to GraphQL endpoint: `http://localhost:8000/graphql/`
- Show GraphQL interface

**Script:**
> "First, let me show you the GraphQL API. I'm using Graphene-Django to create a type-safe GraphQL schema. All queries and mutations are defined in a single schema file, making it easy to understand the API contract."

### 2.2: Authentication Query (0:50-1:10)

**What to show:**
- Show login mutation in Postman
- Execute login request
- Show JWT token response

**Query:**
```graphql
mutation LoginUser($email: String!, $password: String!) {
  loginUser(email: $email, password: $password) {
    user {
      id
      username
      email
    }
    token
    success
    message
  }
}
```

**Variables:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Script:**
> "Here's the login mutation. I'm using JWT tokens for stateless authentication. The mutation validates credentials and returns a token that the frontend stores for subsequent requests."

### 2.3: Feed Query (1:10-1:40)

**What to show:**
- Show feed query
- Execute and display results
- Show nested data structure

**Query:**
```graphql
query GetFeed {
  feed(limit: 10, offset: 0) {
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
```

**Script:**
> "This is the feed query. Notice how GraphQL lets me request exactly the fields I need. The API returns posts from users I follow, with nested author information and interaction counts. This is much more efficient than REST endpoints that return fixed data structures."

### 2.4: Create Post Mutation (1:40-2:10)

**What to show:**
- Show create post mutation
- Execute with sample content
- Show response with new post ID

**Mutation:**
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
```

**Variables:**
```json
{
  "content": "This is my first post! #GraphQL #Django"
}
```

**Script:**
> "Creating a post is straightforward. The mutation validates the input, saves to the database, and triggers real-time notifications to followers. The response includes the new post with all necessary data."

### 2.5: Interactions (2:10-2:30)

**What to show:**
- Show like post mutation
- Show comment mutation
- Show follow user mutation

**Script:**
> "The API supports various interactions: liking posts, commenting with nested replies, and following users. Each mutation includes proper validation and error handling."

---

## Scene 3: Frontend Demo (2:30-4:30)

### 3.1: Authentication Flow (2:30-2:50)

**What to show:**
- Open React app at `http://localhost:3000`
- Show login page
- Enter credentials
- Successful login redirect to feed

**Script:**
> "Now let's see the frontend in action. The React app uses Apollo Client to communicate with the GraphQL API. When I log in, the app stores the JWT token and uses it for authenticated requests."

### 3.2: Feed Display (2:50-3:20)

**What to show:**
- Display feed with multiple posts
- Show post cards with author info
- Show like/comment buttons
- Scroll through feed

**Script:**
> "The feed displays posts from followed users in real-time. Each post shows the author's profile picture, content, and interaction counts. The UI is responsive and uses Tailwind CSS for styling."

### 3.3: Creating a Post (3:20-3:40)

**What to show:**
- Click "Create Post" button
- Type new post content
- Submit
- See new post appear in feed

**Script:**
> "Creating a post is simple. I type content and submit. The app sends a GraphQL mutation to the backend, which validates the input, saves to the database, and returns the new post. The feed updates immediately."

### 3.4: Interactions (3:40-4:10)

**What to show:**
- Like a post (show like count increase)
- Add a comment
- Reply to comment
- Show real-time updates

**Script:**
> "The app supports full interaction capabilities. I can like posts, add comments with nested replies, and see real-time updates. The backend handles all validation and maintains data consistency."

### 3.5: User Profile (4:10-4:30)

**What to show:**
- Navigate to user profile
- Show profile information
- Show user's posts
- Show follow button
- Show follower/following counts

**Script:**
> "Each user has a profile page showing their information, posts, and follower counts. I can follow/unfollow users directly from the profile."

---

## Scene 4: Best Practices (4:30-5:00)

**What to show:**
- Open browser DevTools
- Show network requests
- Show GraphQL query structure
- Show error handling

**Script:**
> "Let me highlight some best practices I've implemented:

> **1. GraphQL Best Practices:** Type-safe schema, efficient queries, proper error handling.

> **2. Authentication:** JWT tokens, secure storage, automatic token refresh.

> **3. Validation:** Input validation on both frontend and backend, clear error messages.

> **4. Real-time:** WebSocket support via Django Channels for live notifications and updates.

> **5. Clean Architecture:** Separation of concerns with GraphQL types, resolvers, and mutations clearly organized.

> **6. Error Handling:** Comprehensive error responses with meaningful messages for debugging.

> **7. Performance:** Pagination, lazy loading, optimized queries to reduce data transfer."

---

## Recording Tips

### Tools Needed
- **Screen Recorder:** OBS Studio (free) or ScreenFlow (Mac)
- **API Testing:** Postman or GraphQL Playground
- **Frontend:** React dev server running locally
- **Backend:** Django dev server running locally

### Setup Before Recording
1. Start Django backend: `python manage.py runserver`
2. Start React frontend: `npm start`
3. Open Postman with pre-configured requests
4. Test all endpoints before recording
5. Clear browser cache and cookies
6. Set screen resolution to 1920x1080 for clarity

### Recording Best Practices
- Speak clearly and at a moderate pace
- Pause briefly between scenes
- Show code snippets on screen
- Highlight important parts with cursor
- Use keyboard shortcuts to speed up navigation
- Keep terminal/console visible for logs
- Zoom in on code for readability

### Audio
- Use a quiet environment
- Speak into microphone clearly
- Add background music (optional)
- Use royalty-free music from YouTube Audio Library

### Editing
- Add title slide at beginning
- Add transitions between scenes
- Add captions for code snippets
- Add background music
- Keep video under 5 minutes
- Export at 1080p 60fps

---

## Upload Instructions

### YouTube
1. Go to youtube.com
2. Click "Create" → "Upload video"
3. Upload your video file
4. Add title: "Social Media Backend API - Full Demo"
5. Add description with links to GitHub and documentation
6. Add tags: GraphQL, Django, React, API, Backend
7. Set visibility to "Unlisted" or "Public"
8. Copy video link

### Google Drive
1. Go to drive.google.com
2. Click "New" → "File upload"
3. Select your video file
4. Right-click → "Share"
5. Set permissions to "Viewer"
6. Copy sharing link

### Alternative Platforms
- Vimeo (vimeo.com)
- Loom (loom.com) - Great for quick demos
- Wistia (wistia.com)

---

## Demo Script Summary

| Time | Scene | Duration |
|------|-------|----------|
| 0:00-0:30 | Introduction | 30s |
| 0:30-1:10 | GraphQL Overview & Login | 40s |
| 1:10-1:40 | Feed Query | 30s |
| 1:40-2:10 | Create Post | 30s |
| 2:10-2:30 | Interactions | 20s |
| 2:30-2:50 | Frontend Login | 20s |
| 2:50-3:20 | Feed Display | 30s |
| 3:20-3:40 | Create Post | 20s |
| 3:40-4:10 | Interactions | 30s |
| 4:10-4:30 | User Profile | 20s |
| 4:30-5:00 | Best Practices | 30s |

---

## Checklist Before Recording

- [ ] Backend running and tested
- [ ] Frontend running and tested
- [ ] Postman requests configured
- [ ] Test data created in database
- [ ] Screen resolution set to 1920x1080
- [ ] Microphone tested
- [ ] Recording software ready
- [ ] All endpoints working
- [ ] No errors in console
- [ ] Network tab clear
- [ ] Browser zoomed for readability

---

## Post-Recording

1. Edit video (add intro, transitions, captions)
2. Export at 1080p 60fps
3. Upload to YouTube/Google Drive
4. Share link with mentors
5. Add link to README.md
6. Update portfolio with video

---

**Ready to record!** 🎥
