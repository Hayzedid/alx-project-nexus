# Frontend & Demo Video Plan

## Current Status

✅ Backend: Fully deployed to Render
✅ API: GraphQL endpoints ready
✅ Database: PostgreSQL configured
✅ Real-time: Django Channels ready

⏳ Frontend: React app creating (create-react-app in progress)

---

## Phase 1: Quick Demo (Today - Without Full Frontend)

### Option A: Postman + HTML Demo (15 minutes)

**What you can demo RIGHT NOW:**

1. **Postman GraphQL Requests:**
   - Login mutation
   - Get feed query
   - Create post mutation
   - Like post mutation
   - Follow user mutation

2. **Show in Browser:**
   - GraphQL Playground at `http://localhost:8000/graphql/`
   - Admin panel at `http://localhost:8000/admin/`
   - ERD diagram (already created)

3. **Explain Best Practices:**
   - GraphQL schema design
   - Authentication flow
   - Error handling
   - Real-time capabilities

**Time to record:** 5 minutes
**Tools needed:** Postman, browser, screen recorder

---

## Phase 2: Full Frontend Demo (After React Setup)

### Once create-react-app finishes:

1. **Install dependencies** (5 minutes)
2. **Create core components** (30 minutes)
3. **Connect to GraphQL API** (20 minutes)
4. **Test all features** (15 minutes)
5. **Record full demo** (10 minutes)

---

## Recommended Demo Video Structure

### Version 1: Quick Demo (5 minutes) - Record TODAY

**0:00-0:30** - Introduction
- Project overview
- Tech stack
- What we're building

**0:30-2:00** - API Demo (Postman)
- Login mutation
- Feed query
- Create post
- Like/comment interactions
- Show GraphQL advantages

**2:00-3:30** - GraphQL Playground
- Show schema
- Explain queries/mutations
- Show real-time capabilities
- Explain error handling

**3:30-4:00** - Best Practices
- Authentication (JWT)
- Validation
- Error handling
- Clean architecture

**4:00-5:00** - Architecture Overview
- Show ERD diagram
- Explain data model
- Show deployment setup

---

### Version 2: Full Demo (5 minutes) - Record AFTER Frontend Ready

**0:00-0:30** - Introduction
- Project overview
- Full-stack architecture

**0:30-1:30** - Frontend Demo
- Login page
- Feed display
- Create post
- Real-time updates

**1:30-2:30** - API Integration
- Show GraphQL queries
- Show mutations
- Show error handling

**2:30-3:30** - Interactions
- Like posts
- Comment on posts
- Follow users
- Real-time notifications

**3:30-4:30** - User Profile
- Profile page
- Edit profile
- View posts
- Follower/following lists

**4:30-5:00** - Best Practices
- Code organization
- Security measures
- Performance optimization

---

## Recording Setup

### Tools You'll Need

1. **Screen Recorder:**
   - OBS Studio (FREE - https://obsproject.com/)
   - ScreenFlow (Mac - $99)
   - Camtasia (Windows/Mac - $99)

2. **API Testing:**
   - Postman (FREE - https://www.postman.com/)
   - GraphQL Playground (Built-in)

3. **Backend Running:**
   ```bash
   cd social-media-backend
   python manage.py runserver
   ```

4. **Frontend Running (when ready):**
   ```bash
   cd social-media-frontend
   npm start
   ```

---

## Quick Demo Script (For Recording TODAY)

### Scene 1: Introduction (0:00-0:30)

**Show:**
- Project title on screen
- GitHub repository
- Tech stack logos

**Say:**
> "Hello! I'm demonstrating a full-stack social media application built with Django, GraphQL, and React. This project showcases modern backend architecture with real-time capabilities. Let me walk you through the key features and best practices I've implemented."

---

### Scene 2: API Overview (0:30-1:00)

**Show:**
- Open Postman
- Show GraphQL endpoint: `http://localhost:8000/graphql/`
- Show list of requests

**Say:**
> "The backend is built with Django and Graphene for GraphQL. I've created a type-safe schema with queries and mutations for all features. Let me show you some key endpoints."

---

### Scene 3: Authentication (1:00-1:30)

**Show:**
- Login mutation in Postman
- Execute request
- Show JWT token response

**Mutation:**
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
  }
}
```

**Say:**
> "First, authentication. I'm using JWT tokens for stateless authentication. The login mutation validates credentials and returns a token. This token is then used for all subsequent authenticated requests."

---

### Scene 4: Feed Query (1:30-2:00)

**Show:**
- Feed query in Postman
- Execute and show results
- Highlight nested data

**Query:**
```graphql
query GetFeed {
  feed(limit: 10) {
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

**Say:**
> "This is the feed query. Notice how GraphQL lets me request exactly the fields I need. I get posts from followed users with nested author information and interaction counts. This is much more efficient than REST endpoints."

---

### Scene 5: Create Post (2:00-2:30)

**Show:**
- Create post mutation
- Execute with sample content
- Show response

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
  }
}
```

**Say:**
> "Creating a post is straightforward. The mutation validates input, saves to the database, and triggers real-time notifications to followers. The response includes the new post with all necessary data."

---

### Scene 6: Interactions (2:30-3:30)

**Show:**
- Like post mutation
- Comment mutation
- Follow user mutation
- Show responses

**Say:**
> "The API supports various interactions: liking posts, commenting with nested replies, and following users. Each mutation includes proper validation and error handling. The backend maintains data consistency and triggers real-time updates."

---

### Scene 7: Best Practices (3:30-5:00)

**Show:**
- GraphQL schema in code editor
- Error handling examples
- Validation logic
- Authentication flow diagram

**Say:**
> "Let me highlight the best practices I've implemented:

> **1. GraphQL Best Practices:** Type-safe schema, efficient queries, proper error handling with meaningful messages.

> **2. Authentication:** JWT tokens for stateless auth, secure storage, automatic token refresh.

> **3. Validation:** Input validation on both frontend and backend, clear error messages for debugging.

> **4. Real-time:** WebSocket support via Django Channels for live notifications and updates.

> **5. Clean Architecture:** Separation of concerns with GraphQL types, resolvers, and mutations clearly organized.

> **6. Database Design:** Normalized schema with proper relationships, denormalized counts for performance.

> **7. Performance:** Pagination, lazy loading, optimized queries to reduce data transfer.

> **8. Security:** CORS configuration, CSRF protection, secure password hashing with bcrypt."

---

## Recording Instructions

### Step 1: Prepare Environment
```bash
# Terminal 1: Start backend
cd social-media-backend
python manage.py runserver

# Terminal 2: Open Postman
# Terminal 3: Open browser to http://localhost:8000/graphql/
```

### Step 2: Open OBS Studio
1. Download and install OBS Studio
2. Create new scene
3. Add display capture (select your monitor)
4. Set resolution to 1920x1080
5. Set frame rate to 60fps

### Step 3: Record
1. Click "Start Recording"
2. Follow the script above
3. Speak clearly and at moderate pace
4. Show each request/response clearly
5. Pause between scenes
6. Click "Stop Recording" when done

### Step 4: Edit (Optional)
- Trim intro/outro
- Add title slide
- Add captions for code
- Add background music (optional)
- Export at 1080p 60fps

### Step 5: Upload
- YouTube: youtube.com/upload
- Google Drive: drive.google.com
- Loom: loom.com (quick option)

---

## What to Have Ready

### Before Recording:

1. **Backend running:**
   ```bash
   python manage.py runserver
   ```

2. **Test data in database:**
   - Create test user
   - Create test posts
   - Create test interactions

3. **Postman configured:**
   - Login request ready
   - Feed query ready
   - Create post ready
   - Like post ready
   - Follow user ready

4. **Browser ready:**
   - GraphQL Playground open
   - Admin panel accessible
   - ERD diagram ready

5. **Screen setup:**
   - Resolution: 1920x1080
   - Zoom level: 100%
   - Dark theme for code
   - Microphone tested

---

## Timeline

### TODAY:
- [ ] Record quick demo (5 minutes) with Postman
- [ ] Upload to YouTube/Google Drive
- [ ] Share link

### THIS WEEK:
- [ ] Wait for React app to finish installing
- [ ] Install dependencies
- [ ] Create core components
- [ ] Connect to GraphQL API
- [ ] Record full frontend demo
- [ ] Upload full demo

---

## Video Submission Checklist

- [ ] Video is under 5 minutes
- [ ] Shows API endpoints and requests/responses
- [ ] Shows frontend integration (or Postman demo)
- [ ] Explains best practices
- [ ] Video is clear and audible
- [ ] Uploaded to YouTube/Google Drive
- [ ] Link is accessible
- [ ] Link added to README.md

---

## Next Steps

1. **Record quick demo TODAY** (Postman + API)
2. **Upload to YouTube/Google Drive**
3. **Share link with mentors**
4. **Continue with full frontend after React setup**
5. **Record full demo when frontend is ready**

---

**Ready to record!** 🎥
