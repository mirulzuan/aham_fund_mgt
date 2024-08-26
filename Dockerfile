# Use a Python base image
FROM python:3.8.19-slim-bullseye

# Set environment variables to prevent Python from writing .pyc files to disc
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libmariadb-dev \
       pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install pipenv

# Create and set the working directory
WORKDIR /aham

# Copy Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /aham/

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of your application code
COPY . /aham/

# Expose the port the app runs on
EXPOSE 5000

# Command to run the Flask application
CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]
