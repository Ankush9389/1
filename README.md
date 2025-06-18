# Makeba - YouTube Video Downloader

A privacy-focused YouTube video downloader that supports 360p, 480p, and 720p video downloads. No user history is saved, ensuring complete privacy.

## Features

- ✅ Download YouTube videos and Shorts
- ✅ Multiple quality options (360p, 480p, 720p)
- ✅ Privacy-first (no history saved)
- ✅ Clean, responsive UI with dark theme
- ✅ Real-time video information preview
- ✅ Mobile-friendly design

## Local Development

### Prerequisites

- Python 3.11 or higher
- pip or uv package manager

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd makeba-youtube-downloader
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export SESSION_SECRET="your-secure-session-key-here"
```

4. Run the application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Production Deployment

### Environment Variables

Set the following environment variables:

- `SESSION_SECRET`: A secure random string for session management

### Using Gunicorn (Recommended)

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
```

### Using Docker

```bash
docker build -t makeba-downloader .
docker run -p 5000:5000 -e SESSION_SECRET="your-secret-key" makeba-downloader
```

## Deployment Platforms

### Heroku

1. Create a `Procfile`:
```
web: gunicorn --bind 0.0.0.0:$PORT main:app
```

2. Deploy:
```bash
heroku create your-app-name
heroku config:set SESSION_SECRET="your-secret-key"
git push heroku main
```

### Railway

1. Connect your GitHub repository
2. Set environment variable: `SESSION_SECRET`
3. Deploy automatically

### DigitalOcean App Platform

1. Connect your GitHub repository
2. Set environment variables
3. Deploy with automatic scaling

### VPS/Self-hosted

1. Install Python 3.11+
2. Clone the repository
3. Install dependencies
4. Set up a reverse proxy (nginx recommended)
5. Use systemd or supervisor for process management

## File Structure

```
makeba-youtube-downloader/
├── app.py              # Main Flask application
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
├── utils/
│   └── downloader.py   # YouTube download logic
├── templates/
│   └── index.html      # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css   # Custom styles
│   └── js/
│       └── app.js      # Client-side JavaScript
├── Dockerfile          # Docker configuration
└── README.md           # This file
```

## Security Notes

- The application doesn't store any user data or download history
- Session secrets should be kept secure and rotated regularly
- Consider implementing rate limiting for production use
- All downloads are automatically cleaned up after 1 minute

## Legal Considerations

This tool is for educational purposes. Users are responsible for ensuring they have the right to download content and comply with YouTube's Terms of Service and applicable copyright laws.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).