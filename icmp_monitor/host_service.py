from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
hosts = []
results = {}

# Endpoint do pobierania listy hostów
@app.route('/api/hosts', methods=['GET'])
def get_hosts():
    return jsonify(hosts)

# Endpoint do dodawania hostów
@app.route('/api/hosts', methods=['POST'])
def add_host():
    global hosts
    data = request.get_json()
    new_hosts = data.get('hosts', [])
    hosts.extend(new_hosts)
    hosts = list(set(hosts))  # Usuń duplikaty
    return jsonify({"status": "success", "hosts": hosts})

# Endpoint do odbierania wyników pingów
@app.route('/api/results', methods=['POST'])
def receive_results():
    global results
    data = request.get_json()
    for host, result in data.items():
        results[host] = result
    save_results_to_file()
    return jsonify({"status": "success"})

def save_results_to_file():
    with open('ping_results.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == '__main__':
    if os.path.exists('ping_results.json'):
        with open('ping_results.json', 'r') as f:
            results = json.load(f)
    app.run(host='0.0.0.0', port=5000)
