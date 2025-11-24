# Demo Recording Checklist & Quick Start

## 🎯 Your Task: Record 5-Minute Demo Video

### What to Show:
1. ✅ API endpoints and requests/responses (Postman)
2. ✅ Frontend integration (React - when ready)
3. ✅ Best practices explanation
4. ✅ Industry standards applied

### Where to Upload:
- YouTube (youtube.com)
- Google Drive (drive.google.com)
- Loom (loom.com) - Easiest option

---

## 🚀 Quick Start: Record Demo TODAY (Without Frontend)

### Step 1: Ensure Backend is Running
```bash
cd social-media-backend
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 2: Download OBS Studio (FREE)
- Go to https://obsproject.com/
- Download for your OS
- Install and open

### Step 3: Setup OBS for Recording
1. Click "+" under "Scenes" → Name it "Demo"
2. Click "+" under "Sources" → Select "Display Capture"
3. Select your monitor
4. Set output resolution to 1920x1080
5. Set frame rate to 60fps

### Step 4: Prepare Postman
1. Open Postman (https://www.postman.com/)
2. Create new request to: `http://localhost:8000/graphql/`
3. Set method to POST
4. Add these pre-configured requests:

**Request 1: Login**
```json
{
  "query": "mutation LoginUser($email: String!, $password: String!) { loginUser(email: $email, password: $password) { user { id username email } token success } }",
  "variables": {
    "email": "user@example.com",
    "password": "password123"
  }
}
```

**Request 2: Get Feed**
```json
{
  "query": "query GetFeed { feed(limit: 10) { id content author { id username profilePicture } likesCount commentsCount isLiked createdAt } }"
}
```

**Request 3: Create Post**
```json
{
  "query": "mutation CreatePost($content: String!) { createPost(content: $content) { post { id content author { id username } createdAt } success } }",
  "variables": {
    "content": "This is my first post! #GraphQL #Django"
  }
}
```

**Request 4: Like Post**
```json
{
  "query": "mutation LikePost($postId: ID!) { likePost(postId: $postId) { success message } }",
  "variables": {
    "postId": "1"
  }
}
```

### Step 5: Open GraphQL Playground
- Open browser to: `http://localhost:8000/graphql/`
- This shows the interactive GraphQL interface

### Step 6: Start Recording
1. In OBS, click "Start Recording"
2. Follow the script below
3. Click "Stop Recording" when done

---

## 📝 Recording Script (5 Minutes)

### [0:00-0:30] Introduction
**What to show on screen:**
- Your project name
- GitHub repository link
- Tech stack (Django, GraphQL, React)

**What to say:**
> "Hello! I'm demonstrating a full-stack social media application. The backend is built with Django and GraphQL, providing a modern, type-safe API. The frontend is built with React for a responsive user experience. Let me show you how it all works together."

---

### [0:30-1:30] API Demo - Postman

**What to show:**
1. Open Postman
2. Show GraphQL endpoint
3. Execute Login request
4. Show JWT token response

**What to say:**
> "First, let's look at the API. I'm using GraphQL with Graphene-Django. This provides a type-safe schema and efficient queries. Here's the login mutation - I send credentials and get back a JWT token. This token is used for all authenticated requests.

> The key advantage of GraphQL is that I request exactly the fields I need. No over-fetching or under-fetching like with REST APIs."

---

### [1:30-2:30] Feed Query

**What to show:**
1. Execute Feed query in Postman
2. Show nested data structure
3. Highlight author information
4. Show interaction counts

**What to say:**
> "This is the feed query. Notice the nested structure - I get posts with author information, like counts, comment counts, and whether I've liked each post. All in a single query. The API returns exactly what the frontend needs.

> This is much more efficient than REST endpoints that return fixed data structures. With GraphQL, I can optimize each query for the specific use case."

---

### [2:30-3:30] Mutations & Interactions

**What to show:**
1. Execute Create Post mutation
2. Show response with new post
3. Execute Like Post mutation
4. Show success response

**What to say:**
> "Creating a post is straightforward. The mutation validates the input, saves to the database, and returns the new post. The response includes all necessary data for the frontend to display it immediately.

> Liking a post is just as simple. The mutation validates that the user hasn't already liked the post, saves the interaction, and returns success. The backend maintains data consistency and triggers real-time notifications to followers."

---

### [3:30-4:30] Best Practices

**What to show:**
1. Open GraphQL Playground
2. Show schema
3. Show error handling
4. Explain validation

**What to say:**
> "Let me highlight the best practices I've implemented:

> **1. GraphQL Schema:** Type-safe, self-documenting, and efficient. Every field has a clear type and purpose.

> **2. Authentication:** JWT tokens for stateless authentication. Secure, scalable, and industry-standard.

> **3. Validation:** Input validation on both frontend and backend. Clear error messages for debugging.

> **4. Error Handling:** Comprehensive error responses with meaningful messages. No generic '500 errors'.

> **5. Real-time:** Django Channels provides WebSocket support for live notifications and updates.

> **6. Database Design:** Normalized schema with proper relationships. Denormalized counts for performance.

> **7. Clean Architecture:** Separation of concerns with GraphQL types, resolvers, and mutations clearly organized.

> **8. Security:** CORS configuration, CSRF protection, secure password hashing with bcrypt."

---

### [4:30-5:00] Deployment & Summary

**What to show:**
1. Show Render deployment configuration
2. Show Docker setup
3. Show environment variables

**What to say:**
> "The application is deployed to Render with PostgreSQL and Redis. The Docker setup allows for consistent development and production environments. Environment variables are properly configured for security.

> This project demonstrates a complete, production-ready backend with modern best practices. The GraphQL API is efficient, type-safe, and easy to integrate with any frontend framework."

---

## 📹 Recording Tips

### Before You Start:
- [ ] Backend is running (`python manage.py runserver`)
- [ ] Postman is open with requests ready
- [ ] GraphQL Playground is open in browser
- [ ] OBS is configured and ready
- [ ] Microphone is tested
- [ ] Screen is at 1920x1080 resolution
- [ ] No notifications will pop up
- [ ] You have 5-10 minutes of uninterrupted time

### During Recording:
- [ ] Speak clearly and at moderate pace
- [ ] Pause briefly between sections
- [ ] Move mouse slowly for clarity
- [ ] Zoom in on code for readability
- [ ] Show each request/response clearly
- [ ] Don't rush through the content

### After Recording:
- [ ] Review the video
- [ ] Trim any long pauses
- [ ] Add title slide (optional)
- [ ] Add captions for code (optional)
- [ ] Export at 1080p 60fps

---

## 📤 Upload to YouTube (Easiest)

### Step 1: Go to YouTube
- Visit https://www.youtube.com
- Click your profile icon (top right)
- Click "Create a video"

### Step 2: Upload Video
- Click "SELECT FILES"
- Choose your recorded video
- Wait for upload to complete

### Step 3: Add Details
- **Title:** "Social Media Backend API - Full Demo"
- **Description:**
  ```
  Full-stack social media application built with Django, GraphQL, and React.
  
  GitHub: https://github.com/Hayzedid/alx-project-nexus
  
  Features:
  - GraphQL API with type-safe schema
  - JWT authentication
  - Real-time WebSocket support
  - PostgreSQL database
  - Docker deployment
  
  Best Practices Demonstrated:
  - Clean architecture
  - Input validation
  - Error handling
  - Security measures
  - Performance optimization
  ```
- **Tags:** GraphQL, Django, React, API, Backend, Python
- **Visibility:** "Unlisted" or "Public"

### Step 4: Share Link
- Copy the video URL
- Share with mentors
- Add to README.md

---

## 🎬 Alternative: Use Loom (Easiest Option)

Loom is perfect for quick demos:

1. Go to https://www.loom.com
2. Sign up (free)
3. Click "Start recording"
4. Select screen to record
5. Record your demo
6. Click "Done"
7. Copy sharing link
8. Share with mentors

**Advantage:** No editing needed, instant sharing!

---

## 📋 Final Checklist

### Before Recording:
- [ ] Backend running
- [ ] Postman configured
- [ ] OBS installed and configured
- [ ] Microphone tested
- [ ] Screen resolution 1920x1080
- [ ] No notifications enabled

### During Recording:
- [ ] Introduction (0:00-0:30)
- [ ] API Demo (0:30-1:30)
- [ ] Feed Query (1:30-2:30)
- [ ] Mutations (2:30-3:30)
- [ ] Best Practices (3:30-4:30)
- [ ] Deployment (4:30-5:00)

### After Recording:
- [ ] Review video
- [ ] Trim if needed
- [ ] Upload to YouTube/Loom
- [ ] Share link
- [ ] Add to README.md
- [ ] Submit to mentors

---

## 🆘 Troubleshooting

### Backend won't start?
```bash
# Make sure you're in the right directory
cd social-media-backend

# Check if port 8000 is available
# If not, use: python manage.py runserver 8001

# Check for errors
python manage.py check
```

### Postman requests failing?
- Verify backend is running
- Check that GraphQL endpoint is correct
- Verify request format is valid JSON
- Check for typos in query

### OBS not recording?
- Check that display capture is selected
- Verify output directory is writable
- Check disk space is available
- Try restarting OBS

### Video quality issues?
- Set resolution to 1920x1080
- Set frame rate to 60fps
- Use H.264 codec
- Export at high bitrate

---

## 📚 Resources

- **OBS Studio:** https://obsproject.com/
- **Postman:** https://www.postman.com/
- **Loom:** https://www.loom.com/
- **YouTube Upload:** https://www.youtube.com/upload
- **GraphQL Docs:** https://graphql.org/
- **Django Docs:** https://docs.djangoproject.com/

---

## ✅ You're Ready!

Everything is set up. Now:
1. Start your backend
2. Open OBS
3. Follow the script
4. Record your demo
5. Upload to YouTube/Loom
6. Share the link

**Good luck! 🚀**
