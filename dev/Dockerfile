# Set base image (host OS)
FROM python:3.8-alpine

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY app.py .
COPY database.py .

# Create template directory
RUN mkdir templates
COPY templates/ ./templates/

# Specify the command to run on container start
COPY start.sh .
RUN chmod +x /start.sh

CMD ["/start.sh"]
