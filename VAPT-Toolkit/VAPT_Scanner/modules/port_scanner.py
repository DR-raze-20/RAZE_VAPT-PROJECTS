import socket
import threading

# Common ports + service names
PORT_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP",
    68: "DHCP",
    69: "TFTP",
    80: "HTTP",
    110: "POP3",
    123: "NTP",
    137: "NetBIOS",
    138: "NetBIOS",
    139: "NetBIOS",
    143: "IMAP",
    161: "SNMP",
    389: "LDAP",
    443: "HTTPS",
    445: "SMB",
    514: "Syslog",
    587: "SMTP Secure",
    631: "IPP",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
}

COMMON_PORTS = list(PORT_SERVICES.keys())


# -------------------------- TCP Scan --------------------------

def tcp_scan(target, port, results):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.4)
        conn = s.connect_ex((target, port))

        if conn == 0:
            banner = grab_banner(target, port)
            service = PORT_SERVICES.get(port, "Unknown")
            results.append(f"[OPEN] TCP {port} ({service}) | Banner: {banner}")

        s.close()
    except:
        pass


# -------------------------- UDP Scan --------------------------

def udp_scan(target, port, results):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.sendto(b"test", (target, port))

        try:
            data, _ = s.recvfrom(1024)  # if response → open
            service = PORT_SERVICES.get(port, "Unknown")
            results.append(f"[OPEN] UDP {port} ({service}) - Responded")
        except socket.timeout:
            # UDP ports often "open|filtered" → no response
            results.append(f"[UNSURE] UDP {port} may be open/filtered")

    except:
        pass


# -------------------------- Banner Grabbing --------------------------

def grab_banner(target, port):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        s.connect((target, port))
        banner = s.recv(1024).decode(errors="ignore").strip()
        s.close()
        return banner if banner else "No banner"
    except:
        return "No banner"


# -------------------------- Scan Types --------------------------

def fast_scan(target):
    results = []
    threads = []

    for port in COMMON_PORTS:
        t = threading.Thread(target=tcp_scan, args=(target, port, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return results


def full_scan(target):
    results = []
    threads = []

    for port in range(1, 1025):  # first 1024 ports (most important)
        t = threading.Thread(target=tcp_scan, args=(target, port, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return results


def custom_scan(target, start, end):
    results = []
    threads = []

    for port in range(start, end + 1):
        t = threading.Thread(target=tcp_scan, args=(target, port, results))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return results


def single_port(target, port):
    results = []
    tcp_scan(target, port, results)
    udp_scan(target, port, results)
    return results
