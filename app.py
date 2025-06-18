import os
import logging
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from utils.downloader import YouTubeDownloader
import tempfile
import threading
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize YouTube downloader
downloader = YouTubeDownloader()

@app.route('/')
def index():
    """Main page with download form"""
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    """Handle video download request"""
    try:
        url = request.form.get('url', '').strip()
        quality = request.form.get('quality', '720p')
        
        if not url:
            flash('Please enter a YouTube URL', 'error')
            return redirect(url_for('index'))
        
        # Validate YouTube URL
        if not downloader.is_valid_youtube_url(url):
            flash('Please enter a valid YouTube URL', 'error')
            return redirect(url_for('index'))
        
        # Get video info
        video_info = downloader.get_video_info(url)
        if not video_info:
            flash('Could not fetch video information. Please check the URL and try again.', 'error')
            return redirect(url_for('index'))
        
        # Download video
        download_path = downloader.download_video(url, quality)
        if not download_path:
            flash('Download failed. The requested quality might not be available.', 'error')
            return redirect(url_for('index'))
        
        # Clean up file after sending (in background)
        def cleanup_file(file_path):
            time.sleep(60)  # Wait 1 minute before cleanup
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logging.info(f"Cleaned up file: {file_path}")
            except Exception as e:
                logging.error(f"Error cleaning up file {file_path}: {e}")
        
        # Start cleanup thread
        cleanup_thread = threading.Thread(target=cleanup_file, args=(download_path,))
        cleanup_thread.daemon = True
        cleanup_thread.start()
        
        # Generate filename for download
        filename = f"{video_info.get('title', 'video')}_{quality}.mp4"
        # Clean filename
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
        
        return send_file(
            download_path,
            as_attachment=True,
            download_name=filename,
            mimetype='video/mp4'
        )
        
    except Exception as e:
        logging.error(f"Download error: {e}")
        flash('An error occurred during download. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/info', methods=['POST'])
def get_video_info():
    """Get video information via AJAX"""
    try:
        url = request.json.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'Please enter a YouTube URL'}), 400
        
        if not downloader.is_valid_youtube_url(url):
            return jsonify({'error': 'Please enter a valid YouTube URL'}), 400
        
        video_info = downloader.get_video_info(url)
        if not video_info:
            return jsonify({'error': 'Could not fetch video information'}), 400
        
        return jsonify({
            'title': video_info.get('title', 'Unknown'),
            'duration': video_info.get('duration_string', 'Unknown'),
            'thumbnail': video_info.get('thumbnail', ''),
            'uploader': video_info.get('uploader', 'Unknown'),
            'view_count': video_info.get('view_count', 0),
            'available_qualities': downloader.get_available_qualities(video_info)
        })
        
    except Exception as e:
        logging.error(f"Info error: {e}")
        return jsonify({'error': 'An error occurred while fetching video information'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
