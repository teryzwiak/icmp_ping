# Dockerfile for ping app
FROM python:3.9-slim

WORKDIR /app

COPY ping_app.py /app
COPY .env /app
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*
RUN pip install flask requests python-dotenv 

EXPOSE 5001
CMD ["python", "ping_app.py"]
