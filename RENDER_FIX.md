# Render Deployment Fix

## Problem
Render couldn't find `requirements.txt` because it's looking in the root directory, but your Django app is in the `social-media-backend` subdirectory.

## Solution
I've created the necessary files to fix this:

### 1. Root-level `requirements.txt`
Created `/requirements.txt` in the project root with all dependencies including:
- Django 5.2.6
- Graphene Django
- Channels & Redis
- Gunicorn (for production)
- Daphne (for WebSocket support)

### 2. Updated Build & Start Commands

**New Build Command:**
```bash
cd social-media-backend && pip install -r ../requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**New Start Command:**
```bash
cd social-media-backend && gunicorn social_feed_api.wsgi:application --bind 0.0.0.0:$PORT --workers 4
```

### 3. Updated render.yaml
Updated `/render.yaml` with correct paths to handle subdirectory structure.

---

## How to Deploy to Render

### Step 1: Commit Changes
```bash
git add .
git commit -m "Add root requirements.txt and fix Render deployment"
git push origin main
```

### Step 2: Update Render Dashboard

1. Go to your Render service dashboard
2. Click "Settings" → "Build & Deploy"
3. Update **Build Command:**
   ```
   cd social-media-backend && pip install -r ../requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   ```
4. Update **Start Command:**
   ```
   cd social-media-backend && gunicorn social_feed_api.wsgi:application --bind 0.0.0.0:$PORT --workers 4
   ```
5. Click "Save"

### Step 3: Trigger Redeploy
1. Click "Manual Deploy" → "Deploy latest commit"
2. Monitor the build in "Logs" tab
3. Wait for "Your service is live" message

---

## What Changed

| File | Change |
|------|--------|
| `/requirements.txt` | Created new file in root with all dependencies |
| `/render.yaml` | Updated with `cd social-media-backend` prefix |
| `/social-media-backend/RENDER_DEPLOYMENT.md` | Updated commands with correct paths |

---

## Verify Deployment

Once deployed, check:

1. **GraphQL Endpoint:**
   ```
   https://your-service-name.onrender.com/graphql/
   ```

2. **Admin Panel:**
   ```
   https://your-service-name.onrender.com/admin/
   ```

3. **Logs:**
   - Go to Render dashboard → Logs
   - Look for "Your service is live" message

---

## Troubleshooting

### Still getting "requirements.txt not found"?
1. Verify `/requirements.txt` exists in root
2. Check that `git push` was successful
3. Trigger manual redeploy in Render dashboard

### Build still fails?
1. Check Render logs for specific error
2. Verify all dependencies are in `/requirements.txt`
3. Ensure `gunicorn` is in requirements.txt

### App won't start?
1. Check that `social_feed_api.wsgi` exists
2. Verify `manage.py` is in `social-media-backend/`
3. Check environment variables are set

---

## Files Ready for Deployment

✅ `/requirements.txt` - Root-level dependencies
✅ `/render.yaml` - Infrastructure configuration
✅ `/social-media-backend/Procfile` - Heroku config (optional)
✅ `/social-media-backend/Dockerfile` - Docker config (optional)
✅ `/social-media-backend/docker-compose.yml` - Local Docker setup

---

## Next Steps

1. **Commit and push** the changes
2. **Update Render dashboard** with new commands
3. **Trigger redeploy** and monitor logs
4. **Test endpoints** once deployed

Your app should now deploy successfully to Render! 🚀
