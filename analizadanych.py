def analyze_pings(data_json):
    # Wczytanie danych JSON
    data = json.loads(data_json)

    # Przetworzenie danych
    server_data = defaultdict(list)

    for entry in data:
        server = entry["server"]
        node_id = entry["node_id"]
        success = entry["success"]
        latency = entry["latency"]
        timestamp = entry["timestamp"]
        server_data[server].append((node_id, success, latency, timestamp))

    # Analiza danych
    analysis_results = []

    for server, pings in server_data.items():
        total_pings = len(pings)
        failed_pings = [ping for ping in pings if not ping[1]]
        successful_pings = [ping[2] for ping in pings if ping[1]]
        
        failure_rate = len(failed_pings) / total_pings
        avg_latency = statistics.mean(successful_pings) if successful_pings else None
        max_latency = max(successful_pings) if successful_pings else None
        min_latency = min(successful_pings) if successful_pings else None

        problem = None
        if failure_rate > 0.5:
            problem = "High failure rate"
        elif avg_latency and avg_latency > 100:
            problem = "High average latency"
        elif max_latency and max_latency > 200:
            problem = "High maximum latency"

        analysis_results.append({
            "server": server,
            "problem": problem,
            "details": {
                "total_pings": total_pings,
                "failed_pings": len(failed_pings),
                "failure_rate": failure_rate,
                "avg_latency": avg_latency,
                "max_latency": max_latency,
                "min_latency": min_latency
            }
        })

    return analysis_results