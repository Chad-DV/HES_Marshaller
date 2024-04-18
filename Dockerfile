# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment
RUN python -m venv /venv

# Set up the environment
ENV PATH="/venv/bin:$PATH"

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Define environment variable
ENV NAME World

# Expose port 8883 for MQTT
EXPOSE 8883

# Expose port 1883 for MQTT
EXPOSE 1883

# Expose port 3306 for MySQL
EXPOSE 3306

# Run main.py when the container launches
CMD ["python", "main.py"]
