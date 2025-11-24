# Deployment Guide - Social Media Backend

## Local Development

### Prerequisites
- Python 3.11+
- pip
- Virtual environment

### Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

**Access:**
- GraphQL: http://localhost:8000/graphql/
- Admin: http://localhost:8000/admin/

---

## Docker Deployment (Local)

### Prerequisites
- Docker
- Docker Compose

### Setup

```bash
# Build and start containers
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f web
```

**Access:**
- GraphQL: http://localhost:8000/graphql/
- Admin: http://localhost:8000/admin/
- WebSocket: ws://localhost:8001/ws/

### Stop containers
```bash
docker-compose down
```

---

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed
- Git repository initialized

### Setup

```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis addon
heroku addons:create heroku-redis:premium-0

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# View logs
heroku logs --tail
```

**Access:**
- GraphQL: https://your-app-name.herokuapp.com/graphql/
- Admin: https://your-app-name.herokuapp.com/admin/

---

## AWS Deployment (EC2 + RDS)

### Prerequisites
- AWS account
- EC2 instance (Ubuntu 22.04)
- RDS PostgreSQL instance
- Elastic IP

### Setup

```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip postgresql-client nginx supervisor

# Clone repository
git clone https://github.com/your-username/alx-project-nexus.git
cd alx-project-nexus/social-media-backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env file
nano .env
# Add your configuration

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create supervisor config
sudo nano /etc/supervisor/conf.d/social_media.conf
```

**Supervisor config:**
```ini
[program:social_media]
directory=/home/ubuntu/alx-project-nexus/social-media-backend
command=/home/ubuntu/alx-project-nexus/social-media-backend/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:8000 social_feed_api.wsgi:application
user=ubuntu
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/social_media.log
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /home/ubuntu/alx-project-nexus/social-media-backend/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/alx-project-nexus/social-media-backend/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable Nginx config
sudo ln -s /etc/nginx/sites-available/social_media /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Start supervisor
sudo systemctl restart supervisor

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## DigitalOcean App Platform

### Prerequisites
- DigitalOcean account
- GitHub repository

### Setup

1. **Connect GitHub repository**
   - Go to DigitalOcean App Platform
   - Click "Create App"
   - Select GitHub repository

2. **Configure app.yaml**
   ```yaml
   name: social-media-backend
   services:
   - name: web
     github:
       repo: your-username/alx-project-nexus
       branch: main
     build_command: pip install -r requirements.txt && python manage.py collectstatic --noinput
     run_command: gunicorn social_feed_api.wsgi:application --bind 0.0.0.0:8080
     envs:
     - key: DEBUG
       value: "False"
     - key: DATABASE_URL
       scope: RUN_AND_BUILD_TIME
       value: ${db.connection_string}
     http_port: 8080
   databases:
   - name: db
     engine: PG
     version: "15"
   ```

3. **Deploy**
   - Push to GitHub
   - DigitalOcean automatically deploys

---

## Build Commands

### Development Build
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Production Build (Heroku)
```bash
# Procfile handles build and start automatically
# Build: pip install -r requirements.txt
# Start: gunicorn social_feed_api.wsgi
```

### Production Build (Docker)
```bash
# Build Docker image
docker build -t social-media-backend .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/dbname \
  -e REDIS_URL=redis://redis:6379/0 \
  social-media-backend
```

### Production Build (AWS/DigitalOcean)
```bash
# Build
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Start
gunicorn --workers 4 --bind 0.0.0.0:8000 social_feed_api.wsgi:application
```

---

## Environment Variables

### Required
- `DEBUG` - Set to False in production
- `SECRET_KEY` - Django secret key
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DATABASE_URL` - PostgreSQL connection string

### Optional
- `REDIS_URL` - Redis connection string
- `CORS_ALLOWED_ORIGINS` - Comma-separated list of allowed origins
- `EMAIL_HOST_USER` - Email for notifications
- `EMAIL_HOST_PASSWORD` - Email password

---

## Database Setup

### PostgreSQL (Production)
```bash
# Create database
createdb social_media_db

# Create user
createuser social_media_user

# Set password
psql -c "ALTER USER social_media_user WITH PASSWORD 'your-password';"

# Grant privileges
psql -c "GRANT ALL PRIVILEGES ON DATABASE social_media_db TO social_media_user;"
```

### Connection String
```
postgresql://social_media_user:your-password@localhost:5432/social_media_db
```

---

## Monitoring & Maintenance

### Logs
```bash
# Heroku
heroku logs --tail

# Docker
docker-compose logs -f web

# AWS/DigitalOcean
tail -f /var/log/social_media.log
```

### Database Backups
```bash
# PostgreSQL backup
pg_dump social_media_db > backup.sql

# Restore
psql social_media_db < backup.sql
```

### Health Check
```bash
# Test GraphQL endpoint
curl http://localhost:8000/graphql/

# Test admin
curl http://localhost:8000/admin/
```

---

## Troubleshooting

### Issue: Database connection error
- Check DATABASE_URL format
- Verify database is running
- Check credentials

### Issue: Static files not loading
- Run `python manage.py collectstatic --noinput`
- Check STATIC_URL and STATIC_ROOT settings

### Issue: CORS errors
- Verify CORS_ALLOWED_ORIGINS includes frontend URL
- Check browser console for specific error

### Issue: WebSocket connection fails
- Ensure Channels is configured
- Check Redis connection
- Verify WebSocket URL is correct

---

## Performance Optimization

### Caching
```python
# Add Redis caching
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
    }
}
```

### Database Optimization
- Use select_related() for foreign keys
- Use prefetch_related() for reverse relations
- Add database indexes
- Use pagination

### API Optimization
- Enable gzip compression
- Use CDN for static files
- Implement rate limiting
- Cache GraphQL queries

---

## Security Checklist

- [ ] DEBUG = False in production
- [ ] SECRET_KEY is secure and unique
- [ ] ALLOWED_HOSTS configured correctly
- [ ] HTTPS/SSL enabled
- [ ] CORS configured for specific origins
- [ ] Database credentials in environment variables
- [ ] Regular security updates
- [ ] Database backups enabled
- [ ] Monitoring and logging configured
- [ ] Rate limiting enabled

---

**Last Updated:** November 2025
