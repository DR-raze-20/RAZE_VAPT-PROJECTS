import requests

xss_payloads = [
    "<script>alert(1)</script>",
    '"><img src=x onerror=alert(1)>',
    "<svg/onload=alert(1)>"
]

def check_xss(target):
    results = []

    for payload in xss_payloads:
        try:
            r = requests.get(target, params={"q": payload}, timeout=5)

            if payload in r.text:
                results.append(f"Possible XSS with payload: {payload}")
        except:
            continue

    if not results:
        return ["No XSS vulnerabilities detected."]

    return results
