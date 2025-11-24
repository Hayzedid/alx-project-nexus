# Social Media Backend - ERD Submission Guide

## 📊 Database Schema Overview

Your social media backend contains **9 entities** with well-designed relationships:

### Entities:
1. **USER** - User accounts with profile information
2. **POST** - User-created posts with content and metadata
3. **POST_MEDIA** - Media files attached to posts (1:N with POST)
4. **LIKE** - Post likes (tracks user-post interactions)
5. **COMMENT** - Comments on posts (supports nested replies)
6. **COMMENT_LIKE** - Likes on comments
7. **SHARE** - Post shares with share types
8. **FOLLOW** - User follow relationships (self-referential N:M)
9. **POST_VIEW** - Analytics tracking for post views

---

## 🔗 Key Relationships

| Relationship | Type | Constraint |
|---|---|---|
| USER → POST | 1:N | CASCADE delete |
| POST → POST_MEDIA | 1:N | CASCADE delete |
| USER → LIKE | 1:N | CASCADE delete |
| POST → LIKE | 1:N | CASCADE delete |
| USER → COMMENT | 1:N | CASCADE delete |
| POST → COMMENT | 1:N | CASCADE delete |
| COMMENT → COMMENT | 1:N | Self-referential (nested replies) |
| USER ↔ USER (FOLLOW) | N:M | Self-referential |
| USER → POST_VIEW | 1:N | CASCADE delete (nullable for anonymous) |

---

## 📋 Entity Attributes Summary

### USER
- **PK:** id
- **UK:** email, username
- **Fields:** bio, profile_picture, followers_count, following_count, posts_count, is_verified
- **Timestamps:** created_at, updated_at

### POST
- **PK:** id
- **FK:** author_id (USER)
- **Fields:** content, content_type (text/image/video/mixed), privacy_level (public/followers/private)
- **Denormalized:** likes_count, comments_count, shares_count
- **Flags:** is_pinned, is_edited
- **Timestamps:** created_at, updated_at

### POST_MEDIA
- **PK:** id
- **FK:** post_id (POST)
- **Fields:** media_type (image/video/gif), file, thumbnail, order
- **Timestamps:** created_at

### LIKE
- **PK:** id
- **FK:** user_id (USER), post_id (POST)
- **Unique Constraint:** (user_id, post_id)
- **Timestamps:** created_at

### COMMENT
- **PK:** id
- **FK:** user_id (USER), post_id (POST), parent_id (COMMENT - nullable)
- **Fields:** content, likes_count, is_edited
- **Timestamps:** created_at, updated_at

### COMMENT_LIKE
- **PK:** id
- **FK:** user_id (USER), comment_id (COMMENT)
- **Unique Constraint:** (user_id, comment_id)
- **Timestamps:** created_at

### SHARE
- **PK:** id
- **FK:** user_id (USER), post_id (POST)
- **Fields:** share_type (timeline/direct/external), caption
- **Timestamps:** created_at

### FOLLOW
- **PK:** id
- **FK:** follower_id (USER), following_id (USER)
- **Unique Constraint:** (follower_id, following_id)
- **Timestamps:** created_at

### POST_VIEW
- **PK:** id
- **FK:** user_id (USER - nullable), post_id (POST)
- **Fields:** ip_address (for anonymous tracking)
- **Timestamps:** viewed_at

---

## 🎯 Design Highlights

✅ **Normalized Structure:** Separate tables for interactions (Like, Comment, Share, Follow)
✅ **Denormalization Strategy:** Count fields on POST and COMMENT for performance
✅ **Cascading Deletes:** Maintains referential integrity
✅ **Unique Constraints:** Prevents duplicate likes, follows, comments
✅ **Self-Referential:** COMMENT (nested replies) and FOLLOW (user relationships)
✅ **Flexible Privacy:** Privacy levels on posts (public/followers/private)
✅ **Analytics Ready:** POST_VIEW table with IP tracking for anonymous users
✅ **Indexed Queries:** Optimized for common queries (author, created_at, privacy_level)

---

## 📤 Steps to Submit

### Option 1: Using the HTML ERD File
1. Open `ERD_DIAGRAM.html` in your browser
2. Right-click the diagram → "Save image as" → Save as PNG
3. Create a new Google Doc at [docs.google.com](https://docs.google.com)
4. Insert → Image → Upload the saved PNG
5. Share the Google Doc with your mentor

### Option 2: Using Draw.io
1. Go to [draw.io](https://draw.io)
2. Create → New Diagram
3. Recreate the ERD using the entity details above
4. File → Export → PNG
5. Upload to Google Doc and share

### Option 3: Using Lucidchart
1. Go to [lucidchart.com](https://lucidchart.com)
2. Create new ERD diagram
3. Add entities and relationships from the schema above
4. Export as image
5. Upload to Google Doc and share

---

## 🔐 Google Doc Sharing Settings

When sharing your Google Doc:
- Click **Share** button
- Set to **"Viewer"** access for mentors (they can view but not edit)
- Copy the shareable link
- Provide the link in your submission

---

## 📝 Example Google Doc Structure

Your Google Doc should include:
1. **Title:** "Social Media Backend - Entity Relationship Diagram"
2. **ERD Image:** The diagram showing all entities and relationships
3. **Brief Description:** 2-3 sentences about your database design
4. **Key Features:** Bullet points highlighting design decisions
5. **Entity Count:** "9 entities with X relationships"

---

## ✨ Design Strengths to Highlight

- **Scalable Architecture:** Separate interaction tables allow independent scaling
- **Data Integrity:** Foreign key constraints with CASCADE deletes
- **Performance:** Denormalized counts reduce query complexity
- **Flexibility:** Privacy levels and share types support multiple use cases
- **Analytics:** POST_VIEW table enables engagement tracking
- **Nested Comments:** Self-referential design supports threaded discussions
- **Social Graph:** FOLLOW table enables friend/follower features

---

Generated from: `/social-media-backend/users/models.py`, `/social-media-backend/posts/models.py`, `/social-media-backend/interactions/models.py`
