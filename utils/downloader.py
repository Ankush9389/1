import yt_dlp
import os
import tempfile
import logging
import re
from urllib.parse import urlparse, parse_qs

class YouTubeDownloader:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        logging.info(f"Created temp directory: {self.temp_dir}")
    
    def is_valid_youtube_url(self, url):
        """Check if URL is a valid YouTube URL"""
        youtube_regex = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        )
        return youtube_regex.match(url) is not None
    
    def get_video_info(self, url):
        """Get video information without downloading"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
                
        except Exception as e:
            logging.error(f"Error getting video info: {e}")
            return None
    
    def get_available_qualities(self, video_info):
        """Get available video qualities"""
        if not video_info or 'formats' not in video_info:
            return ['720p', '480p', '360p']  # Default fallback
        
        available_qualities = set()
        target_qualities = ['360p', '480p', '720p']
        
        for fmt in video_info['formats']:
            if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                height = fmt.get('height')
                if height:
                    if height >= 720:
                        available_qualities.add('720p')
                    elif height >= 480:
                        available_qualities.add('480p')
                    elif height >= 360:
                        available_qualities.add('360p')
        
        # Return in order of preference
        result = []
        for quality in target_qualities:
            if quality in available_qualities:
                result.append(quality)
        
        return result if result else ['720p', '480p', '360p']
    
    def download_video(self, url, quality='720p'):
        """Download video with specified quality"""
        try:
            # Map quality to height
            quality_map = {
                '360p': 360,
                '480p': 480,
                '720p': 720
            }
            
            max_height = quality_map.get(quality, 720)
            
            # Create unique filename
            import uuid
            filename = f"video_{uuid.uuid4().hex}.%(ext)s"
            output_path = os.path.join(self.temp_dir, filename)
            
            ydl_opts = {
                'format': f'best[height<={max_height}][ext=mp4]/best[height<={max_height}]/best[ext=mp4]/best',
                'outtmpl': output_path,
                'merge_output_format': 'mp4',
                'writesubtitles': False,
                'writeautomaticsub': False,
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Find the downloaded file
            for file in os.listdir(self.temp_dir):
                if file.startswith(f"video_{filename.split('_')[1].split('.')[0]}"):
                    return os.path.join(self.temp_dir, file)
            
            return None
            
        except Exception as e:
            logging.error(f"Error downloading video: {e}")
            return None
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        try:
            import shutil
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                logging.info(f"Cleaned up temp directory: {self.temp_dir}")
        except Exception as e:
            logging.error(f"Error cleaning up temp files: {e}")
