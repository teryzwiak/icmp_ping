from flask import Flask, request, jsonify
import subprocess
import threading
import time
import requests

app = Flask(__name__)

main_app_url = "http://main_app:5000/ping_results"
API_KEY = "your_secure_api_key"

def ping_host(host):
    try:
        result = subprocess.run(['ping', '-c', '1', host], capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            time_str = result.stdout.split('time=')[-1].split(' ')[0]
            latency = float(time_str)
            return True, latency
        else:
            return False, None
    except Exception:
        return False, None

def monitor_hosts():
    while True:
        response = requests.get(f"http://main_app:5000/hosts")
        hosts = response.json().get('hosts', [])

        failed_pings = []
        high_latency = []

        for host in hosts:
            success, latency = ping_host(host)
            if not success:
                failed_pings.append(host)
            elif latency and latency > 1000:
                high_latency.append({'host': host, 'latency': latency})

        payload = {'failed_pings': failed_pings, 'high_latency': high_latency}
        headers = {'API-KEY': API_KEY}
        requests.post(main_app_url, json=payload, headers=headers)

        time.sleep(60)  # Czas oczekiwania między kolejnymi pingami

@app.route('/')
def home():
    return "Ping App is running"

if __name__ == '__main__':
    threading.Thread(target=monitor_hosts).start()
    app.run(host='0.0.0.0', port=5001)
