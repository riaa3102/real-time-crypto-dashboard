# Use an official Python runtime as a parent image
FROM python:3.9.10-slim-buster

# Install system dependencies required for building Python packages and make utility
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential libffi-dev make

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Install Poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Configure Poetry:
RUN poetry config virtualenvs.create false && \
    poetry config --list

# Install dependencies using Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

# Make port 8080 available
EXPOSE 8080

# Run main.py when the container launches
ENTRYPOINT ["poetry", "run","streamlit", "run", "app.py", "--server.port=8080"]
