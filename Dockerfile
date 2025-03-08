# Use an official Python runtime as a parent image for the build stage
FROM python:3.12-slim AS builder

# Install required system packages
RUN apt update && apt install -y python3-venv

# Set the working directory in the build stage
WORKDIR /app

# Copy the requirements file into the build stage container
COPY requirements.txt .

# Create a virtual environment
RUN python3 -m venv /env

# Install dependencies inside the virtual environment
RUN /env/bin/pip3 install -r requirements.txt

# Use a minimal runtime image
FROM python:3.12-slim

# Set the working directory in the final stage
WORKDIR /app

# Copy the virtualenv from the builder stage
COPY --from=builder /env /env

# Copy the application code
COPY . .
EXPOSE 8000 
# Use an official Python runtime as a parent image for the build stage
FROM python:3.12-slim AS builder

# Install required system packages
RUN apt update && apt install -y python3-venv postgresql-client

# Set the working directory in the build stage
WORKDIR /app

# Copy the requirements file into the build stage container
COPY requirements.txt .

# Create a virtual environment
RUN python3 -m venv /env

# Install dependencies inside the virtual environment
RUN /env/bin/pip3 install -r requirements.txt

# Use a minimal runtime image
FROM python:3.12-slim

# Install postgresql-client in the runtime image
RUN apt update && apt install -y postgresql-client

# Set the working directory in the final stage
WORKDIR /app

# Copy the virtualenv from the builder stage
COPY --from=builder /env /env

# Copy the application code
COPY . .
EXPOSE 8000 
CMD ["/app/wait-for-db.sh", "db", "/env/bin/python", "-m", "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "sc3.wsgi:application"]
