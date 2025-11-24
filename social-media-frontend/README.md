# Social Media Frontend

A lightweight, vanilla JavaScript frontend for the Social Media Backend API built with GraphQL.

## Features

- ✅ User authentication (login/logout)
- ✅ Feed display with posts
- ✅ Create new posts
- ✅ Like posts
- ✅ Real-time updates
- ✅ Responsive design
- ✅ No build process required

## Quick Start

### Option 1: Simple HTTP Server (Recommended)

```bash
cd social-media-frontend

# Start server on port 3000
python -m http.server 3000

# Open browser to http://localhost:3000
```

### Option 2: Using Node.js

```bash
cd social-media-frontend

# Install dependencies
npm install

# Start server
npm start

# Open browser to http://localhost:3000
```

### Option 3: Direct File Access

Simply open `index.html` in your browser:
```bash
cd social-media-frontend
open index.html  # macOS
start index.html # Windows
xdg-open index.html # Linux
```

## Configuration

The frontend connects to the backend GraphQL API. Update the API URL in `index.html`:

```javascript
const API_URL = 'http://localhost:8000/graphql/';
```

### Environment Variables

Create a `.env` file (optional):
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GRAPHQL_URL=http://localhost:8000/graphql/
```

## Demo Credentials

Use these credentials to test the application:

```
Email: user@example.com
Password: password123
```

## Project Structure

```
social-media-frontend/
├── index.html          # Main HTML file with embedded JavaScript
├── package.json        # Project metadata
├── README.md          # This file
└── .env.example       # Environment variables template
```

## Features Implemented

### Authentication
- User login with email and password
- JWT token storage in localStorage
- Automatic token inclusion in API requests
- Logout functionality

### Feed
- Display posts from followed users
- Show post author information
- Display like and comment counts
- Real-time feed updates

### Post Creation
- Create new posts with text content
- Automatic feed refresh after posting
- Form validation

### Interactions
- Like/unlike posts
- View like counts
- View comment counts

## GraphQL Queries & Mutations

### Login Mutation
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

### Get Feed Query
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

### Create Post Mutation
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

### Like Post Mutation
```graphql
mutation LikePost($postId: ID!) {
  likePost(postId: $postId) {
    success
  }
}
```

## API Integration

The frontend uses Axios to make HTTP requests to the GraphQL API. All requests include:

- `Content-Type: application/json`
- `Authorization: Bearer {token}` (when authenticated)

## Styling

The frontend uses Tailwind CSS via CDN for styling:

```html
<script src="https://cdn.tailwindcss.com"></script>
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Deployment

### Netlify (Recommended)

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=.
```

### Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

### GitHub Pages

1. Push to GitHub
2. Enable GitHub Pages in repository settings
3. Select `main` branch as source

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
EXPOSE 3000
CMD ["python", "-m", "http.server", "3000"]
```

## Troubleshooting

### CORS Errors
If you see CORS errors, ensure the backend has CORS configured:

```python
# In Django settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### API Connection Issues
1. Verify backend is running: `python manage.py runserver`
2. Check API URL in `index.html`
3. Verify CORS headers are correct
4. Check browser console for errors

### Login Fails
1. Verify credentials are correct
2. Check backend is running
3. Look for error messages in browser console
4. Verify database has test user

## Performance Optimization

- Lazy loading of posts
- Efficient GraphQL queries
- Minimal JavaScript bundle
- CSS via CDN
- Local storage for token caching

## Security

- JWT token stored in localStorage
- CORS protection
- Input validation
- XSS prevention via textContent
- CSRF protection via backend

## Future Enhancements

- [ ] User profiles
- [ ] Follow/unfollow users
- [ ] Comments and nested replies
- [ ] Real-time notifications via WebSocket
- [ ] Image uploads
- [ ] Search functionality
- [ ] Dark/light theme toggle
- [ ] Infinite scroll pagination

## Development

### Local Development

```bash
# Start backend
cd ../social-media-backend
python manage.py runserver

# In another terminal, start frontend
cd ../social-media-frontend
python -m http.server 3000
```

### Testing

Test the GraphQL API directly:
1. Go to `http://localhost:8000/graphql/`
2. Use GraphQL Playground to test queries/mutations
3. Copy working queries to frontend

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review backend logs
3. Check browser console for errors
4. Open an issue on GitHub

## Resources

- [GraphQL Documentation](https://graphql.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Axios Documentation](https://axios-http.com/)
- [Django GraphQL](https://docs.graphene-python.org/)

---

**Ready to use!** Start the backend and frontend servers, then open `http://localhost:3000` in your browser.
