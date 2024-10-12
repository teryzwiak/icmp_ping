from flask import Flask, jsonify, request

app = Flask(__name__)

# Przechowywanie danych pingów
ping_data = {}
hosts_to_monitor = []

@app.route('/api/hosts', methods=['GET', 'POST', 'DELETE'])
def manage_hosts():
    if request.method == 'POST':
        host = request.json.get('host')
        if host and host not in hosts_to_monitor:
            hosts_to_monitor.append(host)
            return jsonify({'message': f'Host {host} added to monitoring.'}), 201
        return jsonify({'message': 'Host already exists or invalid.'}), 400

    elif request.method == 'DELETE':
        host = request.json.get('host')
        if host in hosts_to_monitor:
            hosts_to_monitor.remove(host)
            return jsonify({'message': f'Host {host} removed from monitoring.'}), 200
        return jsonify({'message': 'Host not found.'}), 404

    return jsonify(hosts_to_monitor)

@app.route('/api/ping', methods=['POST'])
def receive_ping_data():
    data = request.json
    host = data.get('host')
    status = data.get('status')
    avg_time = data.get('avg_time')

    if host not in ping_data:
        ping_data[host] = []

    ping_data[host].append({'status': status, 'avg_time': avg_time})

    return jsonify({'message': 'Data received'}), 200

@app.route('/api/pingdata', methods=['GET'])
def get_ping_data():
    return jsonify(ping_data)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
