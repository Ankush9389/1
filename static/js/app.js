// Makeba YouTube Downloader - Client-side functionality

document.addEventListener('DOMContentLoaded', function() {
    const urlInput = document.getElementById('url');
    const fetchInfoBtn = document.getElementById('fetchInfo');
    const downloadForm = document.getElementById('downloadForm');
    const downloadBtn = document.getElementById('downloadBtn');
    const videoInfo = document.getElementById('videoInfo');
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    
    // Video info elements
    const videoThumbnail = document.getElementById('videoThumbnail');
    const videoTitle = document.getElementById('videoTitle');
    const videoUploader = document.getElementById('videoUploader');
    const videoDuration = document.getElementById('videoDuration');
    const videoViews = document.getElementById('videoViews');
    const qualitySelect = document.getElementById('quality');
    
    // Fetch video info
    fetchInfoBtn.addEventListener('click', async function() {
        const url = urlInput.value.trim();
        
        if (!url) {
            showAlert('Please enter a YouTube URL', 'warning');
            return;
        }
        
        if (!isValidYouTubeUrl(url)) {
            showAlert('Please enter a valid YouTube URL', 'warning');
            return;
        }
        
        try {
            fetchInfoBtn.disabled = true;
            fetchInfoBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            
            const response = await fetch('/info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                displayVideoInfo(data);
            } else {
                showAlert(data.error || 'Failed to fetch video information', 'danger');
                hideVideoInfo();
            }
        } catch (error) {
            console.error('Error fetching video info:', error);
            showAlert('Network error. Please check your connection and try again.', 'danger');
            hideVideoInfo();
        } finally {
            fetchInfoBtn.disabled = false;
            fetchInfoBtn.innerHTML = '<i class="fas fa-info-circle"></i>';
        }
    });
    
    // Handle form submission
    downloadForm.addEventListener('submit', function(e) {
        const url = urlInput.value.trim();
        
        if (!url) {
            e.preventDefault();
            showAlert('Please enter a YouTube URL', 'warning');
            return;
        }
        
        if (!isValidYouTubeUrl(url)) {
            e.preventDefault();
            showAlert('Please enter a valid YouTube URL', 'warning');
            return;
        }
        
        // Show loading modal
        loadingModal.show();
        downloadBtn.disabled = true;
        downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        
        // Hide loading modal after form submission
        setTimeout(() => {
            downloadBtn.disabled = false;
            downloadBtn.innerHTML = '<i class="fas fa-download me-2"></i>Download Video';
            loadingModal.hide();
        }, 3000);
    });
    
    // Auto-fetch info when URL is pasted
    urlInput.addEventListener('paste', function() {
        setTimeout(() => {
            if (isValidYouTubeUrl(urlInput.value.trim())) {
                fetchInfoBtn.click();
            }
        }, 100);
    });
    
    // Clear video info when URL is cleared
    urlInput.addEventListener('input', function() {
        if (!urlInput.value.trim()) {
            hideVideoInfo();
        }
    });
    
    // Function to validate YouTube URL
    function isValidYouTubeUrl(url) {
        const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)\/(watch\?v=|embed\/|v\/|.+\?v=)?([^&=%\?]{11})/;
        return youtubeRegex.test(url);
    }
    
    // Function to display video information
    function displayVideoInfo(data) {
        videoThumbnail.src = data.thumbnail || '';
        videoThumbnail.alt = data.title || 'Video thumbnail';
        videoTitle.textContent = data.title || 'Unknown title';
        videoUploader.textContent = data.uploader || 'Unknown uploader';
        videoDuration.textContent = data.duration || 'Unknown duration';
        videoViews.textContent = formatNumber(data.view_count || 0);
        
        // Update quality options if available
        if (data.available_qualities && data.available_qualities.length > 0) {
            updateQualityOptions(data.available_qualities);
        }
        
        videoInfo.style.display = 'block';
        videoInfo.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    // Function to hide video information
    function hideVideoInfo() {
        videoInfo.style.display = 'none';
    }
    
    // Function to update quality options
    function updateQualityOptions(availableQualities) {
        const currentValue = qualitySelect.value;
        qualitySelect.innerHTML = '';
        
        const qualityLabels = {
            '720p': '720p HD (Recommended)',
            '480p': '480p Standard', 
            '360p': '360p Mobile'
        };
        
        availableQualities.forEach(quality => {
            const option = document.createElement('option');
            option.value = quality;
            option.textContent = qualityLabels[quality] || quality;
            qualitySelect.appendChild(option);
        });
        
        // Try to keep the current selection if available
        if (availableQualities.includes(currentValue)) {
            qualitySelect.value = currentValue;
        } else {
            qualitySelect.value = availableQualities[0];
        }
    }
    
    // Function to show alerts
    function showAlert(message, type = 'info') {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());
        
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        const header = container.querySelector('header');
        header.insertAdjacentElement('afterend', alertDiv);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv && alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
    
    // Function to format numbers
    function formatNumber(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }
    
    // Handle keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to download
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (!downloadBtn.disabled) {
                downloadForm.submit();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            loadingModal.hide();
        }
    });
    
    // Handle paste events globally
    document.addEventListener('paste', function(e) {
        if (e.target !== urlInput) {
            const pastedText = (e.clipboardData || window.clipboardData).getData('text');
            if (isValidYouTubeUrl(pastedText)) {
                urlInput.value = pastedText;
                urlInput.focus();
                fetchInfoBtn.click();
                e.preventDefault();
            }
        }
    });
});
