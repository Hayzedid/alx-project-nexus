# Quick Reference Card

## 🚀 Start Everything (Copy-Paste)

### Terminal 1: Backend
```bash
cd social-media-backend
python manage.py runserver
```

### Terminal 2: Frontend
```bash
cd social-media-frontend
python -m http.server 3000
```

### Browser
```
http://localhost:3000
```

### Demo Credentials
```
Email: user@example.com
Password: password123
```

---

## 🎬 Record Demo (5 Minutes)

1. Download OBS: https://obsproject.com/
2. Start both servers (see above)
3. Open OBS and configure screen capture
4. Follow script in `DEMO_RECORDING_CHECKLIST.md`
5. Upload to YouTube or Loom

---

## 📤 Upload Video

### YouTube
- youtube.com/upload
- Add title and description
- Copy link

### Loom (Easiest)
- loom.com
- Record directly
- Auto-generates link

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `social-media-backend/` | Django API |
| `social-media-frontend/index.html` | Frontend app |
| `DEMO_RECORDING_CHECKLIST.md` | Recording guide |
| `COMPLETE_SETUP_GUIDE.md` | Full setup |
| `START_HERE.md` | Quick start |

---

## 🎯 Demo Script (5 Minutes)

- **0:00-0:30:** Introduction
- **0:30-1:30:** Frontend demo (login, feed)
- **1:30-2:30:** Create post, like post
- **2:30-3:30:** Show API integration
- **3:30-4:30:** Explain best practices
- **4:30-5:00:** Deployment overview

---

## 🔗 URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend | http://localhost:8000 |
| GraphQL | http://localhost:8000/graphql/ |
| Admin | http://localhost:8000/admin/ |

---

## 📋 Checklist

- [ ] Backend running
- [ ] Frontend running
- [ ] OBS installed
- [ ] Demo credentials tested
- [ ] Recording script ready
- [ ] Microphone tested
- [ ] Screen resolution 1920x1080
- [ ] Record demo
- [ ] Upload to YouTube/Loom
- [ ] Share link

---

## 🆘 Troubleshooting

### Backend won't start?
```bash
cd social-media-backend
python manage.py runserver
```

### Frontend won't load?
```bash
cd social-media-frontend
python -m http.server 3000
```

### Login fails?
- Check credentials: user@example.com / password123
- Verify backend is running
- Check browser console

### API errors?
- Verify backend is on port 8000
- Check CORS configuration
- Verify GraphQL endpoint

---

## 📚 Documentation

- `START_HERE.md` - Quick start
- `COMPLETE_SETUP_GUIDE.md` - Full guide
- `DEMO_RECORDING_CHECKLIST.md` - Recording steps
- `DEMO_VIDEO_GUIDE.md` - Detailed script
- `FRONTEND_SETUP.md` - Frontend details
- `DEPLOYMENT.md` - Deployment guide

---

## ✅ You're Ready!

1. Start servers
2. Test frontend
3. Record demo
4. Upload video
5. Share link

**Good luck! 🚀**
