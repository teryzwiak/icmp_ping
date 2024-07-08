import subprocess
import time
from datetime import datetime
import requests

# Konfiguracja
api_url = "http://host_service:5000/api/hosts"  # URL do serwisu API z listą hostów
report_url = "http://host_service:5000/api/results"  # URL do serwisu API do raportowania wyników
threshold_time = 0.5  # sekundy
results = {}

# Funkcja do pobierania listy hostów z serwisu API
def fetch_hosts():
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        log_issue(f"Error fetching hosts: {e}")
        return []

# Funkcja do pingowania hosta
def ping_host(host):
    try:
        output = subprocess.check_output(["ping", "-c", "1", host], stderr=subprocess.STDOUT, universal_newlines=True)
        if "1 packets transmitted, 1 received" in output:
            lines = output.split('\n')
            for line in lines:
                if "time=" in line:
                    time_ms = float(line.split('time=')[1].split(' ')[0])
                    return time_ms
        return None
    except subprocess.CalledProcessError as e:
        log_issue(f"Error pinging {host}: {e.output.strip()}")
        return None

# Funkcja do logowania
def log_issue(issue):
    with open("log.txt", "a") as f:
        f.write(f"{datetime.now()}: {issue}\n")

# Funkcja do monitorowania hostów
def monitor_hosts():
    global results
    hosts = fetch_hosts()
    results = {host: {"status": "Unknown", "last_checked": None, "latency": None} for host in hosts}
    for host in hosts:
        time_ms = ping_host(host)
        if time_ms is not None:
            results[host] = {
                "status": "Online" if time_ms <= threshold_time * 1000 else "Slow",
                "last_checked": datetime.now().isoformat(),
                "latency": time_ms
            }
        else:
            results[host] = {
                "status": "Offline",
                "last_checked": datetime.now().isoformat(),
                "latency": None
            }
    return results

# Funkcja do raportowania wyników do serwisu API
def report_results():
    try:
        response = requests.post(report_url, json=results)
        response.raise_for_status()
    except requests.RequestException as e:
        log_issue(f"Error reporting results: {e}")

# Główna funkcja monitorująca
def main():
    while True:
        monitor_hosts()
        report_results()
        time.sleep(60)  # Sprawdzanie hostów co 60 sekund

if __name__ == '__main__':
    main()
