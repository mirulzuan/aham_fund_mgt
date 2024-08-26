# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables to prevent Python from writing pyc files to disc and
# to ensure that Python output is sent straight to the terminal (e.g., for logging)
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /aham

# Copy the Pipfile and Pipfile.lock into the container
COPY Pipfile Pipfile.lock /aham/

# Install pipenv and dependencies
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code into the container
COPY . /aham/

# Run the application
CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]
