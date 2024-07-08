# Wybierz obraz bazowy
FROM python:3.9-slim

# Ustaw zmienną środowiskową
ENV PYTHONUNBUFFERED=1

# Utwórz katalog roboczy
WORKDIR /app

# Skopiuj pliki do katalogu roboczego
COPY requirements.txt /app/
COPY monitor.py /app/

# Instalacja wymaganych pakietów
RUN pip install --no-cache-dir -r requirements.txt && apt-get update && apt-get install -y iputils-ping

# Uruchom aplikację
CMD ["python", "monitor.py"]
