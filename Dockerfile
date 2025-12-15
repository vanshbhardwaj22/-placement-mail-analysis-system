FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY web/ ./web/
COPY data/ ./data/
COPY .env.example ./.env.example

# Create data directory if not exists
RUN mkdir -p data

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "8000"]
