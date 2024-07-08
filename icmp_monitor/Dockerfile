# Wybierz obraz bazowy
FROM python:3.9-slim

# Ustaw zmienną środowiskową
ENV PYTHONUNBUFFERED=1

# Utwórz katalog roboczy
WORKDIR /app

# Skopiuj pliki do katalogu roboczego
COPY requirements.txt /app/
COPY host_service.py /app/

# Instalacja wymaganych pakietów
RUN pip install --no-cache-dir -r requirements.txt

# Uruchom aplikację
CMD ["python", "host_service.py"]
