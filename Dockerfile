# Use the official Python base image
FROM python:3.11.8-slim

# Set working directory inside the container
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all other files into the container
COPY . .

# Expose port
EXPOSE 8000

# Command to run the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
