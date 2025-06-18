# Deployment Guide for Makeba YouTube Downloader

## Quick GitHub Deployment Steps

### 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it `makeba-youtube-downloader` (or your preferred name)
3. Make it public or private as desired
4. Don't initialize with README (we'll upload our files)

### 2. Upload Your Code

Option A: Using GitHub Web Interface
1. Download the zip file from this project
2. Extract it locally
3. Go to your empty GitHub repository
4. Click "uploading an existing file"
5. Drag and drop all the extracted files
6. Commit the files

Option B: Using Git CLI
```bash
# In your local project folder
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/makeba-youtube-downloader.git
git push -u origin main
```

## Deployment Options

### Option 1: Heroku (Free/Paid)

1. **Install Heroku CLI** from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login and create app:**
```bash
heroku login
heroku create your-app-name
```

3. **Set environment variables:**
```bash
heroku config:set SESSION_SECRET="your-very-secure-random-string-here"
```

4. **Deploy:**
```bash
git push heroku main
```

5. **Open your app:**
```bash
heroku open
```

### Option 2: Railway (Recommended - Easy)

1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variable:
   - `SESSION_SECRET`: `your-secure-random-string`
6. Deploy automatically!

### Option 3: Render (Free Tier Available)

1. Go to [Render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your GitHub repository
5. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT main:app`
6. Add environment variable:
   - `SESSION_SECRET`: `your-secure-random-string`
7. Deploy!

### Option 4: DigitalOcean App Platform

1. Go to [DigitalOcean](https://cloud.digitalocean.com/apps)
2. Create new app from GitHub repository
3. Configure:
   - **Resource Type:** Web Service
   - **Build Phase:** `pip install -r requirements.txt`
   - **Run Command:** `gunicorn --bind 0.0.0.0:$PORT main:app`
4. Add environment variables
5. Deploy

### Option 5: Vercel (Serverless)

1. Go to [Vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Vercel will auto-detect it's a Python app
4. Add environment variables in settings
5. Deploy

### Option 6: Self-Hosted VPS

For Ubuntu/Debian VPS:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip nginx git ffmpeg -y

# Clone your repository
git clone https://github.com/yourusername/makeba-youtube-downloader.git
cd makeba-youtube-downloader

# Install Python dependencies
pip3 install -r requirements.txt

# Set environment variable
export SESSION_SECRET="your-secure-random-string"

# Test the app
python3 main.py

# For production, use gunicorn with systemd
sudo nano /etc/systemd/system/makeba.service
```

**Systemd service file content:**
```ini
[Unit]
Description=Makeba YouTube Downloader
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/makeba-youtube-downloader
Environment=SESSION_SECRET=your-secure-random-string
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:5000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start the service:**
```bash
sudo systemctl enable makeba
sudo systemctl start makeba
```

**Nginx configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Environment Variables

All deployments need these environment variables:

- `SESSION_SECRET`: A secure random string (generate with `python -c "import secrets; print(secrets.token_hex(32))"`)

## Domain Configuration

After deployment:

1. **Custom Domain:** Most platforms allow custom domain setup in settings
2. **SSL:** Usually provided automatically by the platforms
3. **CDN:** Consider using Cloudflare for better performance

## Monitoring and Maintenance

1. **Logs:** Check platform-specific logging
2. **Updates:** Regularly update dependencies
3. **Backups:** Your code is safe on GitHub
4. **Scaling:** Most platforms offer auto-scaling

## Security Recommendations

1. Use strong session secrets
2. Keep dependencies updated
3. Consider adding rate limiting
4. Monitor for abuse
5. Regularly rotate secrets

## Cost Estimates

- **Railway:** $5-20/month
- **Heroku:** $7-25/month
- **Render:** Free tier available, $7+/month for paid
- **DigitalOcean:** $5-10/month
- **VPS:** $5-20/month depending on provider

## Troubleshooting

**Common Issues:**
1. **Port binding:** Ensure app binds to `0.0.0.0:$PORT`
2. **Dependencies:** Make sure all packages in requirements.txt
3. **Environment variables:** Double-check they're set correctly
4. **Disk space:** YouTube downloads need temporary storage

**Getting Help:**
- Check platform-specific documentation
- Review application logs
- Test locally first
- GitHub Issues for code problems

## Legal Notice

Remember to comply with:
- YouTube Terms of Service
- Local copyright laws
- Platform-specific terms
- Data protection regulations

This tool is for educational purposes. Users are responsible for legal compliance.