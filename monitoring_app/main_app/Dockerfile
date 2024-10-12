# Wybierz bazowy obraz Pythona
FROM python:3.9-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj plik z wymaganiami
COPY requirements.txt .

# Zainstaluj wymagane pakiety
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj resztę kodu
COPY . .

# Ustaw polecenie do uruchomienia aplikacji
CMD ["python", "main_app.py"]
