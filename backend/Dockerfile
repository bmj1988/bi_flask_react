FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for pdf2image
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create required directories
RUN mkdir -p uploads data

# Environment variables
ENV FLASK_APP=run.py
ENV PYTHONPATH=/app
ENV FLASK_DEBUG=1

EXPOSE 5000

CMD ["python", "run.py"]
