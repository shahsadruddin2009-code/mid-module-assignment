# Multi-stage Dockerfile for Online Bookstore Flask App

# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Create non-root user for security
RUN groupadd -r bookstore && useradd -r -g bookstore bookstore

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /home/bookstore/.local

# Copy application files
COPY app.py .
COPY models.py .
COPY static/ static/
COPY templates/ templates/
COPY requirements.txt .

# Create directories and set permissions
RUN mkdir -p logs && \
    chown -R bookstore:bookstore /app && \
    chmod +x app.py

# Switch to non-root user
USER bookstore

# Add user's local bin to PATH
ENV PATH=/home/bookstore/.local/bin:$PATH
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expose port
EXPOSE 5000

# Health check for the bookstore application
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run the Flask application
CMD ["python", "app.py"]