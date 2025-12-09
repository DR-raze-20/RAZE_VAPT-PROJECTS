from modules.sql_injection import check_sqli
from modules.xss_scanner import check_xss
from modules.port_scanner import fast_scan, full_scan, custom_scan, single_port
from modules.report_generator import generate_report

def get_int(prompt):
    """Safe integer input"""
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("❌ Invalid number! Try again.")

def main():
    print("🔥 Raze-Vuln-Tool — VAPT Scanner")
    print("------------------------------------")

    target = input("Enter target URL / IP: ").strip()

    print("\n[1] SQL Injection Scan")
    print("[2] XSS Scan")
    print("[3] Port Scan")
    print("[4] Full Scan")
    print("[5] Exit\n")

    choice = input("Select option: ").strip()

    results = {}

    # -------------------------------- SQLi -----------------------------
    if choice == "1":
        results["SQL Injection"] = check_sqli(target)

    # -------------------------------- XSS ------------------------------
    elif choice == "2":
        results["XSS"] = check_xss(target)

    # -------------------------------- Port Scan ------------------------
    elif choice == "3":
        print("\nPort Scan Types:")
        print("1. Fast Scan (Common Ports)")
        print("2. Full Scan (1–1024)")
        print("3. Custom Range")
        print("4. Single Port\n")

        scan_choice = input("Select scan type: ").strip()

        if scan_choice == "1":
            results["Port Scan"] = fast_scan(target)

        elif scan_choice == "2":
            results["Port Scan"] = full_scan(target)

        elif scan_choice == "3":
            start = get_int("Start port: ")
            end = get_int("End port: ")
            results["Port Scan"] = custom_scan(target, start, end)

        elif scan_choice == "4":
            port = get_int("Enter port: ")
            results["Port Scan"] = single_port(target, port)

        else:
            print("❌ Invalid port scan type.")
            return

    # -------------------------------- Full Scan -------------------------
    elif choice == "4":
        print("\nRunning SQLi...")
        results["SQL Injection"] = check_sqli(target)

        print("\nRunning XSS...")
        results["XSS"] = check_xss(target)

        print("\nRunning Port Scan...")
        results["Port Scan"] = fast_scan(target)

    # -------------------------------- Exit ------------------------------
    elif choice == "5":
        print("Exiting...")
        return

    else:
        print("❌ Invalid menu choice!")
        return

    # -------------------------------- Report Generation ------------------
    print("\n📄 Generating report...")
    generate_report(results, target)

    print("✅ Report generated successfully in the 'reports/' folder!")

if __name__ == "__main__":
    main()
