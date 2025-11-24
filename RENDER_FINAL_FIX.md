# Render Deployment - Final Fix

## Problem Analysis

The build failed because:
1. ✅ Dependencies installed successfully
2. ❌ `manage.py` not found at `/opt/render/project/src/manage.py`

**Root Cause:** Render was looking for `manage.py` in the root directory, but it's in `social-media-backend/` subdirectory.

---

## Solution

### Corrected Build Command
```bash
pip install -r requirements.txt && cd social-media-backend && python manage.py collectstatic --noinput && python manage.py migrate
```

**Execution order:**
1. Install dependencies from `/requirements.txt` (root)
2. Change directory to `social-media-backend/`
3. Run Django collectstatic
4. Run Django migrations

### Corrected Start Command
```bash
cd social-media-backend && gunicorn social_feed_api.wsgi:application --bind 0.0.0.0:$PORT --workers 4
```

**Execution order:**
1. Change directory to `social-media-backend/`
2. Start Gunicorn with Django WSGI application

---

## Update Render Dashboard

### Step 1: Navigate to Settings
1. Go to your Render service dashboard
2. Click "Settings" tab
3. Click "Build & Deploy"

### Step 2: Update Build Command
Replace the current build command with:
```
pip install -r requirements.txt && cd social-media-backend && python manage.py collectstatic --noinput && python manage.py migrate
```

### Step 3: Update Start Command
Replace the current start command with:
```
cd social-media-backend && gunicorn social_feed_api.wsgi:application --bind 0.0.0.0:$PORT --workers 4
```

### Step 4: Save Changes
Click "Save" button

### Step 5: Trigger Redeploy
1. Click "Manual Deploy"
2. Select "Deploy latest commit"
3. Monitor the build in "Logs" tab

---

## Expected Build Output

✅ Dependencies installing successfully (you saw this)
✅ Changing to social-media-backend directory
✅ Running collectstatic
✅ Running migrations
✅ "Your service is live" message

---

## Verify Deployment

Once deployed successfully:

1. **GraphQL Endpoint:**
   ```
   https://your-service-name.onrender.com/graphql/
   ```

2. **Admin Panel:**
   ```
   https://your-service-name.onrender.com/admin/
   ```

3. **Check Logs:**
   - Go to Render dashboard
   - Click "Logs" tab
   - Look for "Your service is live"

---

## Files Updated

| File | Change |
|------|--------|
| `/render.yaml` | Updated build command order |
| `/social-media-backend/RENDER_DEPLOYMENT.md` | Updated commands |
| `/RENDER_FIX.md` | Updated commands |

---

## Key Takeaway

When deploying a Django app in a subdirectory:
1. Install dependencies from root level
2. Change to subdirectory for Django commands
3. Use `&&` to chain commands in correct order

---

## Troubleshooting

### If build still fails:
1. Check Render logs for exact error
2. Verify `requirements.txt` exists in root
3. Verify `manage.py` exists in `social-media-backend/`
4. Ensure all files are committed to git

### If app won't start:
1. Check that `social_feed_api/wsgi.py` exists
2. Verify environment variables are set
3. Check database connection string

### If endpoints return 404:
1. Verify migrations ran successfully
2. Check `ALLOWED_HOSTS` includes your domain
3. Verify static files collected properly

---

**Status:** Ready for deployment ✅
**Next Step:** Update Render dashboard and trigger redeploy
