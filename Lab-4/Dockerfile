FROM python:3.11-slim

WORKDIR /app

# Copy application code into container
COPY persistent_auditor.py .

# Run script with unbuffered output for real-time interactive terminal streaming
CMD ["python", "-u", "persistent_auditor.py"]