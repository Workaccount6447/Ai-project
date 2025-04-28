# Use the official Python image from the DockerHub
FROM python:3.9-slim

# Set environment variables to ensure the output is not buffered
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot script into the container
COPY Ai\ Bot.py /app/

# Command to run the bot script when the container starts
CMD ["python", "Ai Bot.py"]
