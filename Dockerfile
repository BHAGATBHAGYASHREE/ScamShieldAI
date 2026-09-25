# ScamShield AI - Production Container Image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (curl for healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application artifacts
COPY features.py .
COPY app/ app/
COPY models/ models/
COPY streamlit_app.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
