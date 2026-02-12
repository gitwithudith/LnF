# 🚀 Deployment Guide

This guide shows you how to deploy your Campus Lost & Found app online for free.

---

## Option 1: Render (Recommended - Easiest)

### Why Render?
- Free tier available
- Auto-detects Python apps
- Easy database setup
- HTTPS included
- Simple dashboard

### Steps:

#### 1. Prepare Your Code

Add a `render.yaml` file to your project root:

```yaml
services:
  - type: web
    name: campus-lost-and-found
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: FLASK_ENV
        value: production
```

Add `gunicorn` to your requirements.txt:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

#### 2. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

#### 3. Deploy on Render
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render auto-detects settings from `render.yaml`
5. Click "Create Web Service"
6. Wait 2-3 minutes for deployment

#### 4. Set Environment Variables
In Render dashboard:
- Go to your service
- Click "Environment"
- Add: `SECRET_KEY` (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)
- Add: `FLASK_ENV` = `production`

Your app is now live! Render gives you a URL like: `https://campus-lost-and-found.onrender.com`

---

## Option 2: Railway

### Why Railway?
- Very simple setup
- Good free tier
- Nice CLI tool
- Fast deployments

### Steps:

#### 1. Add Procfile
Create a file named `Procfile` (no extension):
```
web: gunicorn run:app
```

#### 2. Add `gunicorn` to requirements.txt
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

#### 3. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git push -u origin main
```

#### 4. Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-deploys!

#### 5. Add Environment Variables
In Railway dashboard:
- Click your project → Variables
- Add `SECRET_KEY`
- Add `FLASK_ENV=production`

---

## Option 3: PythonAnywhere

### Why PythonAnywhere?
- Specifically designed for Python
- Very generous free tier
- Great for learning
- Direct server access

### Steps:

#### 1. Sign Up
- Go to [pythonanywhere.com](https://www.pythonanywhere.com)
- Create free account

#### 2. Upload Your Code
```bash
# On PythonAnywhere Bash console
git clone <your-github-repo-url>
cd campus-lost-and-found
```

#### 3. Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 myenv
pip install -r requirements.txt
```

#### 4. Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Choose Python 3.10
5. Set up WSGI file:

```python
import sys
import os

# Add your project directory
project_home = '/home/yourusername/campus-lost-and-found'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['SECRET_KEY'] = 'your-secret-key-here'
os.environ['FLASK_ENV'] = 'production'

# Import your app
from run import app as application
```

6. Set virtualenv path: `/home/yourusername/.virtualenvs/myenv`
7. Click "Reload"

Your app is live at: `https://yourusername.pythonanywhere.com`

---

## Important: Production Checklist

Before deploying to production:

### 1. Update config.py
```python
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
    # Use environment variable for secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Use PostgreSQL in production (if needed)
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

### 2. Add .env to .gitignore
Make sure `.env` is in your `.gitignore`:
```
.env
*.db
instance/
```

### 3. Set Strong Secret Key
Never use the default! Generate one:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Update Allowed Hosts (if needed)
Some platforms require you to specify allowed hosts.

### 5. Static Files
Make sure your static files are served correctly. Most platforms handle this automatically.

---

## Database Considerations

### SQLite (Current Setup)
- **Pros**: No setup needed, works everywhere
- **Cons**: Not ideal for high traffic, can have issues with some platforms
- **Best for**: Small campus use, testing, demos

### Upgrade to PostgreSQL (Optional)
For production with many users:

1. **Add to requirements.txt**:
```
psycopg2-binary==2.9.9
```

2. **Update config.py**:
```python
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'lost_found.db')
```

3. **On Render/Railway**, add PostgreSQL:
   - Render: Add PostgreSQL database
   - Railway: Add PostgreSQL plugin
   - Both will provide `DATABASE_URL` automatically

---

## Custom Domain (Optional)

If you want `lostandfound.yourschool.edu`:

### On Render:
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS records (they'll show you how)

### On Railway:
1. Click your service → Settings → Domains
2. Add custom domain
3. Update DNS records

---

## Monitoring Your App

### Check Logs
- **Render**: Logs tab in dashboard
- **Railway**: Deployments → View logs
- **PythonAnywhere**: Error log and Server log tabs

### Common Issues:

**"Application Error" on page load**:
- Check logs for errors
- Verify environment variables are set
- Make sure database is created

**Images not showing**:
- Check upload folder permissions
- Verify UPLOAD_FOLDER path in production
- Consider using cloud storage (Cloudinary, AWS S3)

**Database errors**:
- Make sure database is initialized
- Check connection string
- Verify migrations ran

---

## Performance Tips

### 1. Enable Caching
Add to config.py:
```python
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 300
```

### 2. Compress Images
Before upload, compress images to reduce storage.

### 3. Use CDN for Static Files
For larger deployments, use a CDN for CSS/JS.

### 4. Database Indexing
Already done! We have indexes on frequently queried fields.

---

## Security Best Practices

### 1. HTTPS Only
All mentioned platforms provide HTTPS automatically.

### 2. Secret Key
Never commit it! Always use environment variables.

### 3. Rate Limiting
For production, add rate limiting:
```bash
pip install Flask-Limiter
```

### 4. Input Validation
Already implemented in forms!

### 5. File Upload Limits
Already set to 16MB max.

---

## Updating Your Deployed App

### Render/Railway:
Just push to GitHub:
```bash
git add .
git commit -m "Update feature X"
git push
```
Auto-deploys in 2-3 minutes!

### PythonAnywhere:
```bash
# SSH into PythonAnywhere
cd campus-lost-and-found
git pull
# Reload web app from dashboard
```

---

## Backup Your Data

### Download Database:
```bash
# SQLite
scp user@server:/path/to/instance/lost_found.db ./backup.db
```

### PostgreSQL:
Use the platform's backup feature or:
```bash
pg_dump DATABASE_URL > backup.sql
```

---

## Cost Considerations

### Free Tier Limits:

**Render**:
- 750 hours/month (enough for 1 app)
- Sleeps after 15 min inactivity
- Wakes on request (15-30 second delay)

**Railway**:
- $5 free credit/month
- Pay only for usage
- No sleep mode

**PythonAnywhere**:
- 1 web app
- Always on
- Limited CPU/storage

### When to Upgrade:
- High traffic (>1000 daily users)
- Need always-on (no sleep)
- Multiple apps
- Custom domain

---

## Demo Day Tips

If demoing your deployed app:

1. **Test beforehand**: Make sure it's working
2. **Have backup**: Screenshots if internet fails
3. **Know the URL**: Write it down
4. **Explain the stack**: "It's deployed on Render using Flask and SQLite"
5. **Show logs**: Demonstrate you understand monitoring

---

## Need Help?

### Platform Support:
- **Render**: [docs.render.com](https://docs.render.com)
- **Railway**: [docs.railway.app](https://docs.railway.app)
- **PythonAnywhere**: [help.pythonanywhere.com](https://help.pythonanywhere.com)

### Common Resources:
- [Flask Deployment](https://flask.palletsprojects.com/en/latest/deploying/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/flask)

---

**Remember**: Start with Render if you're unsure - it's the easiest!

Good luck with deployment! 🚀
