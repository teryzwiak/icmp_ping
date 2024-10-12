# Dockerfile for main app
FROM python:3.9-slim

WORKDIR /app

COPY main_app.py /app
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*
RUN pip install flask requests

EXPOSE 5000
CMD ["python", "main_app.py"]