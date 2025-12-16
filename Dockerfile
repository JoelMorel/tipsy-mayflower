FROM python:3.11-slim

# Install git (required for installing LivePopularTimes from git)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Use gunicorn for production (matching Procfile)
CMD ["gunicorn", "app:app", "--workers", "2", "--bind", "0.0.0.0:${PORT:-5000}"]