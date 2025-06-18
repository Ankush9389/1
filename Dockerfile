FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install only necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Set environment variables
ENV PYTHONPATH=/app
ENV SESSION_SECRET=change-this-in-production

# Start the application
CMD sh -c 'gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 4 main:app'

