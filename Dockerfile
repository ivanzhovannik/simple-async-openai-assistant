FROM python:3.11-slim

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt ./
COPY app ./app
COPY core ./core
COPY config ./config

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt --progress-bar=off

# Make port 50050 available to the world outside this container
EXPOSE 50050

# Run app/main.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "50050"]
