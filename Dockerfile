# Use an official Python runtime as a parent image
FROM python:3.6.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages
RUN cd /app && pip install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.6.0/wait /wait
RUN chmod +x /wait && chmod +x ./start.sh

CMD ./start.sh

# Make port 8081 available to the world outside this container
EXPOSE 8081
