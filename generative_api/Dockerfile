# Use a Python base image from Docker Hub
FROM python:3.9-slim

# Set environment variables to prevent Python from writing pyc files to disk and to ensure the app runs in production
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV=development

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Flask application into the container
COPY . /app/

# Expose the port on which the Flask app will run
EXPOSE 5000

# Define the command to run the Flask app with Gunicorn (production-ready WSGI server)
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debugger"]
CMD ["python", "app.py", "--host=0.0.0.0", "--port=5000", "--debugger"]
