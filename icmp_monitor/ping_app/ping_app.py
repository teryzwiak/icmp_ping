from flask import Flask, request, jsonify
import subprocess
import threading
import time
import requests
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
MAIN_APP_HOST_NAME = os.getenv("MAIN_APP_HOST_NAME")
MAIN_APP_URL = os.getenv("MAIN_APP_URL")
MAIN_APP_URL_PING_RESULTS = os.getenv("MAIN_APP_URL_PING_RESULTS")
MAIN_APP_URL_PING_HOSTS = os.getenv("MAIN_APP_URL_PING_HOSTS")
PING_HOST_NAME = os.getenv("PING_HOST_NAME")

app = Flask(__name__)

API_KEY = "be6bb4c9eff7f4c46a1a2b6feefde331"

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
        response = requests.get(MAIN_APP_URL_PING_HOSTS)
        hosts = response.json().get('hosts', [])
        failed_pings = []
        high_latency = []

        for host in hosts:
            success, latency = ping_host(host)
            if not success:
                failed_pings.append(host)
            elif latency and latency > 700:
                high_latency.append({'host': host, 'latency': latency})

        payload = {'failed_pings': failed_pings, 'high_latency': high_latency}
        headers = {'API-KEY': API_KEY}
        requests.post(MAIN_APP_URL_PING_RESULTS, json=payload)

        time.sleep(5)  # Czas oczekiwania między kolejnymi pingami

@app.route('/')
def home():
    return "Ping App is running"

if __name__ == '__main__':
    threading.Thread(target=monitor_hosts).start()
    app.run(host='0.0.0.0', port=5001)
