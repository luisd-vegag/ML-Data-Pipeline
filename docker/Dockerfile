# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Airflow home
ENV AIRFLOW_HOME /app

# Expose the Airflow webserver and scheduler ports
EXPOSE 8080 5555

# Start the Airflow webserver and scheduler
CMD ["airflow", "webserver", "--port", "8080"] 
CMD ["airflow", "scheduler"]
