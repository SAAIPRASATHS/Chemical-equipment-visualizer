# Deployment Guide

## 🚀 Quick Start (Development)

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
**Backend running at:** http://localhost:8000

### Web Frontend
```bash
cd web-frontend
npm install
npm run dev
```
**Frontend running at:** http://localhost:3000

---

## 🌐 Production Deployment

### Option 1: Deploy to Render (Recommended)

#### Backend Deployment

1. **Create `render.yaml`** (already created)
2. **Push to GitHub**
3. **Connect to Render:**
   - Go to https://render.com
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will auto-deploy based on `render.yaml`

#### Frontend Deployment

1. **Build the frontend:**
   ```bash
   cd web-frontend
   npm run build
   ```

2. **Deploy to Render Static Site:**
   - Go to Render Dashboard
   - Click "New +" → "Static Site"
   - Connect repository
   - Build Command: `cd web-frontend && npm install && npm run build`
   - Publish Directory: `web-frontend/dist`

### Option 2: Deploy to Vercel (Frontend) + Railway (Backend)

#### Backend on Railway

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy:**
   ```bash
   cd backend
   railway login
   railway init
   railway up
   ```

3. **Set Environment Variables:**
   - `DEBUG=False`
   - `SECRET_KEY=<your-secret-key>`
   - `ALLOWED_HOSTS=your-domain.railway.app`

#### Frontend on Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   cd web-frontend
   vercel
   ```

3. **Update API URL:**
   - Edit `src/services/api.js`
   - Change `API_BASE_URL` to your Railway backend URL

### Option 3: Docker Deployment

#### Using Docker Compose (already configured)

```bash
docker-compose up -d
```

This will start:
- Backend on port 8000
- Frontend on port 3000
- PostgreSQL database

---

## 📋 Pre-Deployment Checklist

### Backend
- [ ] Set `DEBUG=False` in production
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Switch to PostgreSQL (recommended)
- [ ] Set up static file serving
- [ ] Configure CORS for production domain
- [ ] Set up SSL/HTTPS

### Frontend
- [ ] Update API URL in `src/services/api.js`
- [ ] Build production bundle
- [ ] Configure environment variables
- [ ] Set up CDN (optional)

---

## 🔒 Security Considerations

1. **Environment Variables:**
   - Never commit `.env` files
   - Use platform-specific secret management

2. **Database:**
   - Use PostgreSQL in production
   - Enable SSL connections
   - Regular backups

3. **API:**
   - Rate limiting
   - HTTPS only
   - CORS configuration

---

## 📊 Monitoring

- **Backend:** Django admin at `/admin`
- **Logs:** Check platform logs (Render/Railway/Vercel)
- **Errors:** Set up error tracking (Sentry recommended)

---

## 🔄 CI/CD

The project includes GitHub Actions workflow for automatic deployment on push to main branch.

---

## 📱 Desktop Application

To package the desktop application:

```bash
cd desktop-frontend
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

The executable will be in `dist/main.exe`
