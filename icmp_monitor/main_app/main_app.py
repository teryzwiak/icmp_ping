from flask import Flask, request, jsonify, abort
import requests
import logging
from datetime import datetime

app = Flask(__name__)

# Domyślne serwery do pingowania
hosts = ["8.8.8.8", "8.8.4.4"]
API_KEY = "your_secure_api_key"

# Konfiguracja logowania
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s %(message)s')

# Lista do przechowywania wyników pingów
ping_results = []

@app.route('/hosts', methods=['GET', 'POST'])
def manage_hosts():
    if request.method == 'POST':
        data = request.get_json()
        new_hosts = data.get('hosts', [])
        for host in new_hosts:
            if host not in hosts:
                hosts.append(host)
        return jsonify({'hosts': hosts})
    return jsonify({'hosts': hosts})

@app.route('/hosts/remove', methods=['POST'])
def remove_hosts():
    data = request.get_json()
    remove_hosts = data.get('hosts', [])
    for host in remove_hosts:
        if host in hosts:
            hosts.remove(host)
    return jsonify({'hosts': hosts})

@app.route('/ping_results', methods=['POST'])
def receive_ping_results():
    if request.headers.get('API-KEY') != API_KEY:
        abort(403)

    data = request.get_json()
    failed_pings = data.get('failed_pings', [])
    high_latency = data.get('high_latency', [])

    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    for host in failed_pings:
        ping_results.append({'host': host, 'status': 'failed', 'latency': None, 'timestamp': timestamp})
    for entry in high_latency:
        ping_results.append({'host': entry['host'], 'status': 'high_latency', 'latency': entry['latency'], 'timestamp': timestamp})

    # Analiza wyników
    if len(failed_pings) > 0 or len(high_latency) > 0:
        # Zapis do log.txt
        logging.info(f"Failed pings: {failed_pings}")
        logging.info(f"High latency: {high_latency}")

        # Wysyłanie do Zabbix (załóżmy, że mamy endpoint do tego)
        zabbix_url = "http://zabbix_server/api"
        payload = {'failed_pings': failed_pings, 'high_latency': high_latency}
        requests.post(zabbix_url, json=payload)

    return jsonify({'status': 'success'})

@app.route('/ping_results', methods=['GET'])
def get_ping_results():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = ping_results[start:end]
    return jsonify({
        'ping_results': paginated_results,
        'page': page,
        'per_page': per_page,
        'total': len(ping_results)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
