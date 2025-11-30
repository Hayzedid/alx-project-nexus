# 🚀 Social Media Platform - Full Stack Application

A modern, production-ready social media platform built with Django GraphQL backend and React TypeScript frontend.

[![React](https://img.shields.io/badge/React-18.2-blue)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-blue)](https://www.typescriptlang.org/)
[![Django](https://img.shields.io/badge/Django-5.2-green)](https://www.djangoproject.com/)
[![GraphQL](https://img.shields.io/badge/GraphQL-16.8-E10098)](https://graphql.org/)

## 📋 Overview

Complete social media application with modern features including real-time interactions, infinite scrolling, and responsive design. Built as part of the ALX ProDev Frontend Engineering Program.

## ✨ Features

- 🔐 **Authentication** - Secure login/register with session management
- 📝 **Posts** - Create, like, comment, and share
- 💬 **Comments** - Nested replies and real-time updates
- ♾️ **Infinite Scroll** - Seamless content loading
- 📱 **Responsive Design** - Works on all devices
- ⚡ **Real-time Updates** - Optimistic UI with instant feedback
- 🎨 **Modern UI** - Smooth animations with Framer Motion
- 🔒 **Type Safety** - Full TypeScript implementation

## 🏗️ Project Structure

```
alx-project-nexus/
├── social-media-backend/      # Django + GraphQL API
│   ├── users/                 # User authentication
│   ├── posts/                 # Post management
│   ├── interactions/          # Likes & comments
│   └── social_feed_api/       # GraphQL schema
│
├── social-media-frontend/     # React + TypeScript
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/            # Route pages
│   │   ├── context/          # Global state
│   │   ├── graphql/          # Apollo Client setup
│   │   └── types/            # TypeScript interfaces
│   └── package.json
│
└── Documentation files
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ with pip
- Node.js 18+ with npm
- Git

### Installation & Running

#### Option 1: Automated Start (Windows)

```bash
start_servers.bat
```

#### Option 2: Manual Start

**Terminal 1 - Backend:**

```bash
cd social-media-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Terminal 2 - Frontend:**

```bash
cd social-media-frontend
npm install
npm run dev
```

**Access the application:** http://localhost:3000

## 🛠️ Technology Stack

### Backend

| Technology  | Purpose                |
| ----------- | ---------------------- |
| Django 5.2  | Web framework          |
| Graphene    | GraphQL implementation |
| SQLite      | Database               |
| Django CORS | Cross-origin requests  |

### Frontend

| Technology          | Purpose        |
| ------------------- | -------------- |
| React 18.2          | UI framework   |
| TypeScript 5.2      | Type safety    |
| Apollo Client 3.8   | GraphQL client |
| Framer Motion 10.16 | Animations     |
| React Router 6.20   | Navigation     |
| Vite 5.0            | Build tool     |

## 📚 Documentation

- **START_HERE.md** - Complete setup and getting started guide
- **PROJECT_COMPLETE_SUMMARY.md** - Full project overview and achievements
- **BACKEND_CONNECTION_GUIDE.txt** - API documentation and GraphQL schema
- **social-media-backend/README.md** - Backend-specific documentation
- **ERD_DIAGRAM.html** - Database schema visualization

## 🎯 Key Features Implementation

### Dynamic Data Loading

GraphQL with Apollo Client for efficient data fetching with automatic caching and optimistic updates.

### User Interactions

- Like/unlike posts with instant UI feedback
- Nested comment threads
- Share functionality
- Real-time like/comment counts

### Infinite Scrolling

Intersection Observer API for seamless content loading as user scrolls.

### Authentication Flow

- Session-based authentication with HTTP-only cookies
- Protected routes
- Automatic session persistence
- Secure logout

### Responsive Design

- Mobile-first approach
- Breakpoints for all screen sizes
- Touch-friendly interactions
- Optimized layouts

## 🧪 Testing

The application has been thoroughly tested with:

- ✅ User authentication flow
- ✅ Post creation and display
- ✅ Like functionality
- ✅ Comment system
- ✅ Infinite scrolling
- ✅ Responsive design
- ✅ Error handling
- ✅ Loading states

## 🚢 Deployment

### Backend (Render/Railway)

```bash
cd social-media-backend
# Follow DEPLOYMENT.md or RENDER_DEPLOYMENT.md
```

### Frontend (Vercel/Netlify)

```bash
cd social-media-frontend
npm run build
# Deploy dist folder
```

## 📖 API Documentation

GraphQL endpoint: `http://localhost:8000/graphql/`

### Key Mutations

- `registerUser` - Create new account
- `loginUser` - Authenticate user
- `createPost` - Create new post
- `likePost` - Like/unlike post
- `createComment` - Add comment

### Key Queries

- `posts` - Get all posts
- `feed` - Get personalized feed
- `me` - Get current user
- `postComments` - Get post comments

Full API documentation available in `BACKEND_CONNECTION_GUIDE.txt`

## 🎓 Project Context

Built as the capstone project for the ALX ProDev Frontend Engineering Program, demonstrating:

- Modern web development practices
- Full-stack application architecture
- GraphQL API integration
- Type-safe development with TypeScript
- Professional code quality and documentation

## 🏆 Achievements

- ✅ 100% requirement completion
- ✅ Production-ready code
- ✅ Comprehensive documentation
- ✅ Best practices implementation
- ✅ Responsive design
- ✅ Type safety throughout

## 📞 Support

For issues, questions, or contributions:

1. Check documentation files
2. Review START_HERE.md
3. Check backend/frontend READMEs
4. Open an issue on GitHub

---

**Built with ❤️ for ALX ProDev Frontend Engineering Program**
