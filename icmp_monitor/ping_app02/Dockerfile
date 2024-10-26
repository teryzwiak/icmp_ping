# Dockerfile for ping app
FROM python:3.9-slim

WORKDIR /app

COPY ping_app.py /app
RUN pip install flask requests
RUN apt update && apt install -y iputils-ping

EXPOSE 5002
CMD ["python", "ping_app.py"]
