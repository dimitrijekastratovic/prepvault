# Use an official Python runtime as a parent image
# '-slim' variants are smaller and faster to build
FROM python:3.14-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port your app runs on (e.g., 8000 for FastAPI/Django, 5000 for Flask)
EXPOSE 8000

# Define the command to run your app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]