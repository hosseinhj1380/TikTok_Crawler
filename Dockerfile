# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt requirements.txt

# Install Python dependencie

RUN pip install  -r requirements.txt

COPY . .


CMD ["python", "app/main.py"]