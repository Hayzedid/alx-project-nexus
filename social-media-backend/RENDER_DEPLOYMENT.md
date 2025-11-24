# Render Deployment Guide

## Build & Start Commands for Render

### Build Command
```bash
cd social-media-backend && pip install -r ../requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**What it does:**
1. `cd social-media-backend` - Changes to the Django app directory
2. `pip install -r ../requirements.txt` - Installs all Python dependencies from root
3. `python manage.py collectstatic --noinput` - Collects static files (CSS, JS, images)
4. `python manage.py migrate` - Runs database migrations

### Start Command
```bash
cd social-media-backend && gunicorn social_feed_api.wsgi:application --bind 0.0.0.0:$PORT --workers 4
```

**What it does:**
1. `cd social-media-backend` - Changes to the Django app directory
2. `gunicorn` - Production WSGI server
3. `social_feed_api.wsgi:application` - Django application entry point
4. `--bind 0.0.0.0:$PORT` - Binds to Render's dynamic port
5. `--workers 4` - Uses 4 worker processes for concurrency

---

## Step-by-Step Render Deployment

### 1. Prepare Your Repository
```bash
# Ensure requirements.txt is in the root of social-media-backend
# Ensure Procfile or render.yaml exists
# Commit all changes
git add .
git commit -m "Add Render deployment configuration"
git push
```

### 2. Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub account
- Authorize Render to access your repositories

### 3. Create New Web Service
1. Click "New +" → "Web Service"
2. Select your GitHub repository
3. Choose branch (main/master)
4. Fill in service details:
   - **Name:** `social-media-backend`
   - **Runtime:** Python 3
   - **Build Command:** (see below)
   - **Start Command:** (see below)
   - **Plan:** Free or Paid

### 4. Configure Build & Start Commands

**In Render Dashboard:**

**Build Command:**
```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**
```
gunicorn social_feed_api.wsgi:application --bind 0.0.0.0:$PORT --workers 4
```

### 5. Add Environment Variables

Click "Environment" and add:

| Key | Value |
|-----|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | Generate a secure key or use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `ALLOWED_HOSTS` | `your-service-name.onrender.com` |
| `DATABASE_URL` | Will be auto-populated if you create PostgreSQL database |
| `REDIS_URL` | Will be auto-populated if you create Redis instance |
| `CORS_ALLOWED_ORIGINS` | `https://your-frontend-domain.com,https://your-service-name.onrender.com` |

### 6. Create PostgreSQL Database (Optional)
1. Click "New +" → "PostgreSQL"
2. Fill in details:
   - **Name:** `social-media-db`
   - **Database:** `social_media_db`
   - **User:** `social_media_user`
   - **Region:** Same as web service
3. Render will auto-populate `DATABASE_URL`

### 7. Create Redis Instance (Optional)
1. Click "New +" → "Redis"
2. Fill in details:
   - **Name:** `social-media-redis`
   - **Region:** Same as web service
3. Render will auto-populate `REDIS_URL`

### 8. Deploy
1. Click "Create Web Service"
2. Render will automatically:
   - Build your app (run build command)
   - Start your app (run start command)
   - Deploy to production

3. Monitor deployment in the "Logs" tab

### 9. Access Your App
- GraphQL: `https://your-service-name.onrender.com/graphql/`
- Admin: `https://your-service-name.onrender.com/admin/`

---

## Troubleshooting

### Build Fails
**Check logs for errors:**
- Click "Logs" tab
- Look for error messages
- Common issues:
  - Missing dependencies in requirements.txt
  - Syntax errors in settings.py
  - Missing environment variables

**Solution:**
```bash
# Test locally first
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

### App Won't Start
**Check start command:**
- Ensure `gunicorn` is in requirements.txt
- Check `social_feed_api.wsgi` path is correct
- Verify `$PORT` variable is used

**Add to requirements.txt:**
```
gunicorn==21.2.0
```

### Database Connection Error
**Check DATABASE_URL:**
- Verify PostgreSQL service is created
- Check `DATABASE_URL` in environment variables
- Ensure database migrations ran successfully

**Test connection:**
```bash
python manage.py dbshell
```

### Static Files Not Loading
**Ensure collectstatic runs:**
- Add to build command: `python manage.py collectstatic --noinput`
- Check `STATIC_URL` and `STATIC_ROOT` in settings.py
- Verify static files directory exists

### CORS Errors
**Update CORS settings:**
```python
# In settings.py
CORS_ALLOWED_ORIGINS = [
    "https://your-service-name.onrender.com",
    "https://your-frontend-domain.com",
]
```

---

## Performance Optimization

### Gunicorn Workers
```bash
# Current: 4 workers
gunicorn social_feed_api.wsgi:application --bind 0.0.0.0:$PORT --workers 4

# For more traffic: 8 workers
gunicorn social_feed_api.wsgi:application --bind 0.0.0.0:$PORT --workers 8

# Formula: (2 × CPU cores) + 1
# Render free tier: 1 CPU → 3 workers
```

### Timeout Settings
```bash
# Increase timeout for long-running requests
gunicorn social_feed_api.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120
```

### Memory Optimization
```bash
# Limit worker memory
gunicorn social_feed_api.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --max-requests 1000
```

---

## Monitoring

### View Logs
- Go to "Logs" tab in Render dashboard
- Real-time logs of your application
- Useful for debugging issues

### Health Checks
Render automatically checks if your app is running:
- Sends HTTP request to your app
- If it fails, restarts the service
- Configure in "Health Check" settings

### Metrics
- View CPU usage
- View memory usage
- View request count
- View error rate

---

## Continuous Deployment

### Auto-Deploy on Push
1. Go to "Settings" tab
2. Enable "Auto-Deploy"
3. Select branch (main/master)
4. Every push to that branch triggers deployment

### Manual Deploy
1. Click "Manual Deploy"
2. Select branch
3. Click "Deploy latest commit"

---

## Environment Variables Reference

### Required
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-service-name.onrender.com
```

### Database
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

### Redis (for WebSockets & Caching)
```
REDIS_URL=redis://user:password@host:port
```

### CORS
```
CORS_ALLOWED_ORIGINS=https://your-service-name.onrender.com,https://frontend-domain.com
```

### Optional
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## Deployment Checklist

- [ ] Repository pushed to GitHub
- [ ] requirements.txt includes all dependencies
- [ ] requirements.txt includes `gunicorn`
- [ ] Build command configured correctly
- [ ] Start command configured correctly
- [ ] Environment variables set
- [ ] PostgreSQL database created (if needed)
- [ ] Redis instance created (if needed)
- [ ] Migrations run successfully
- [ ] Static files collected
- [ ] App accessible at service URL
- [ ] GraphQL endpoint working
- [ ] Admin panel accessible
- [ ] CORS configured for frontend

---

## Quick Reference

**Build Command (Copy-Paste):**
```
cd social-media-backend && pip install -r ../requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command (Copy-Paste):**
```
cd social-media-backend && gunicorn social_feed_api.wsgi:application --bind 0.0.0.0:$PORT --workers 4
```

**Service URL:**
```
https://your-service-name.onrender.com
```

**GraphQL Endpoint:**
```
https://your-service-name.onrender.com/graphql/
```

---

**Last Updated:** November 2025
