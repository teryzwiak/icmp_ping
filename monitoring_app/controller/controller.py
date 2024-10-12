import subprocess
import requests
import time

MAIN_APP_URL = 'http://<adres_ip_głównej_aplikacji>:5000/api/ping'  # Zmień na adres IP głównej aplikacji
HOSTS_API_URL = 'http://<adres_ip_głównej_aplikacji>:5000/api/hosts'  # Zmiana na adres API hostów

def ping(host):
    command = ['fping', '-c', '1', host]
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        avg_time = result.stdout.split()[2]  # Oczekiwany czas odpowiedzi
        status = 'alive'
    else:
        avg_time = 'N/A'
        status = 'dead'

    return {'host': host, 'status': status, 'avg_time': avg_time}

def get_hosts_to_monitor():
    try:
        response = requests.get(HOSTS_API_URL)
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching hosts: {e}")
        return []

if __name__ == "__main__":
    while True:
        hosts = get_hosts_to_monitor()  # Pobierz listę hostów do monitorowania
        for host in hosts:
            data = ping(host)
            try:
                response = requests.post(MAIN_APP_URL, json=data)
                print(f"Sent data for {host}: {response.json()}")
            except requests.exceptions.RequestException as e:
                print(f"Error sending data for {host}: {e}")

        time.sleep(60)  # Czekaj 60 sekund przed następnym pingowaniem
