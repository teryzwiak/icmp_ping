import json

def analyze_results():
    with open('ping_results.json', 'r') as f:
        results = json.load(f)
    
    offline_hosts = [host for host, result in results.items() if result['status'] == 'Offline']
    slow_hosts = [host for host, result in results.items() if result['status'] == 'Slow']

    print(f"Offline hosts: {offline_hosts}")
    print(f"Slow hosts: {slow_hosts}")

if __name__ == '__main__':
    analyze_results()
