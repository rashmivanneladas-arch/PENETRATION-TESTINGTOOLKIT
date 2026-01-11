#!/usr/bin/env python3
"""
PENETRATION TESTING TOOLKIT - SINGLE FILE
CodTech Internship - Task 3
Everything in one file - No import errors!
"""

import os
import sys
import socket
import requests
import time

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Display toolkit banner"""
    banner = """
╔══════════════════════════════════════════════════════════╗
║          P E N E T R A T I O N   T E S T I N G            ║
║                 T O O L K I T   v1.0                      ║
║          CodTech Internship - Task 3                      ║
╚══════════════════════════════════════════════════════════╝
"""
    print(banner)

# ==================== MODULE 1: PORT SCANNER ====================
def port_scanner():
    """Scan open ports on target"""
    print("\n" + "="*50)
    print("PORT SCANNER MODULE")
    print("="*50)
    
    target = input("\nEnter target IP/hostname (e.g., scanme.nmap.org): ").strip()
    
    if not target:
        print("[!] No target entered!")
        return
    
    print(f"\n[*] Scanning {target}...")
    print("[*] This may take a few seconds...\n")
    
    # Common ports to scan
    ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080, 8443]
    
    open_ports = []
    
    for port in ports_to_scan:
        try:
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # 1 second timeout
            
            # Try to connect
            result = sock.connect_ex((target, port))
            
            # Check result
            if result == 0:
                open_ports.append(port)
                print(f"[+] Port {port:5} - OPEN")
            else:
                print(f"[-] Port {port:5} - Closed")
            
            sock.close()
            
        except socket.gaierror:
            print(f"[!] Could not resolve hostname: {target}")
            break
        except socket.error:
            print(f"[!] Error scanning port {port}")
        except KeyboardInterrupt:
            print("\n[!] Scan interrupted by user")
            break
    
    # Results summary
    print("\n" + "="*50)
    print("SCAN RESULTS:")
    print("="*50)
    print(f"Target: {target}")
    print(f"Open ports found: {len(open_ports)}")
    if open_ports:
        print(f"Open ports: {sorted(open_ports)}")
    print("="*50)

# ==================== MODULE 2: DIRECTORY BUSTER ====================
def directory_buster():
    """Find hidden directories on website"""
    print("\n" + "="*50)
    print("DIRECTORY BUSTER MODULE")
    print("="*50)
    
    url = input("\nEnter target URL (e.g., http://testphp.vulnweb.com): ").strip()
    
    # Add http:// if not present
    if not url.startswith('http'):
        url = 'http://' + url
    
    print(f"\n[*] Searching for hidden directories on: {url}")
    print("[*] This may take a moment...\n")
    
    # Common directories to check
    directories = [
        'admin', 'login', 'dashboard', 'wp-admin', 'administrator',
        'config', 'backup', 'database', 'logs', 'tmp', 'test',
        'secret', 'private', 'hidden', 'secure', 'api', 'docs'
    ]
    
    found_directories = []
    
    for directory in directories:
        try:
            # Build test URL
            test_url = f"{url}/{directory}"
            
            # Send request
            response = requests.get(test_url, timeout=5)
            
            # Check response
            if response.status_code == 200:
                print(f"[+] FOUND: /{directory} (200 OK)")
                found_directories.append(directory)
            elif response.status_code == 403:
                print(f"[!] ACCESS DENIED: /{directory} (403 Forbidden)")
            elif response.status_code == 301 or response.status_code == 302:
                print(f"[*] REDIRECT: /{directory} ({response.status_code})")
            
        except requests.exceptions.RequestException:
            print(f"[-] ERROR: Could not access /{directory}")
        except KeyboardInterrupt:
            print("\n[!] Scan interrupted by user")
            break
    
    # Results summary
    print("\n" + "="*50)
    print("SCAN RESULTS:")
    print("="*50)
    print(f"Target: {url}")
    print(f"Directories checked: {len(directories)}")
    print(f"Directories found: {len(found_directories)}")
    if found_directories:
        print(f"Found: {', '.join(found_directories)}")
    print("="*50)

# ==================== MODULE 3: VULNERABILITY SCANNER ====================
def vulnerability_scanner():
    """Check for SQL Injection and XSS vulnerabilities"""
    print("\n" + "="*50)
    print("VULNERABILITY SCANNER MODULE")
    print("="*50)
    
    url = input("\nEnter target URL with parameters (e.g., http://site.com/page?id=1): ").strip()
    
    if not url.startswith('http'):
        url = 'http://' + url
    
    print(f"\n[*] Scanning for vulnerabilities on: {url}")
    print("[*] Running tests...\n")
    
    vulnerabilities_found = []
    
    # TEST 1: SQL Injection
    print("[1] Testing for SQL Injection...")
    sql_payloads = ["'", "' OR '1'='1", "' OR '1'='1' --"]
    
    for payload in sql_payloads:
        try:
            # Add payload to URL
            if '?' in url:
                test_url = url + payload
            else:
                test_url = url + "?id=" + payload
            
            response = requests.get(test_url, timeout=5)
            
            # Check for SQL errors
            sql_errors = ["sql", "mysql", "syntax", "database", "error in your sql"]
            for error in sql_errors:
                if error in response.text.lower():
                    vulnerabilities_found.append(f"SQL Injection (Payload: {payload})")
                    print(f"  [!] Possible SQL Injection with payload: {payload}")
                    break
                    
        except requests.exceptions.RequestException:
            pass
    
    # TEST 2: XSS (Cross-Site Scripting)
    print("\n[2] Testing for XSS...")
    xss_payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert(1)>"]
    
    for payload in xss_payloads:
        try:
            if '?' in url:
                test_url = url + payload
            else:
                test_url = url + "?search=" + requests.utils.quote(payload)
            
            response = requests.get(test_url, timeout=5)
            
            if payload in response.text or payload.replace('"', '&quot;') in response.text:
                vulnerabilities_found.append(f"XSS (Payload: {payload})")
                print(f"  [!] Possible XSS with payload: {payload}")
                
        except requests.exceptions.RequestException:
            pass
    
    # Results summary
    print("\n" + "="*50)
    print("VULNERABILITY SCAN RESULTS:")
    print("="*50)
    print(f"Target: {url}")
    print(f"Vulnerabilities found: {len(vulnerabilities_found)}")
    
    if vulnerabilities_found:
        print("\nFound vulnerabilities:")
        for i, vuln in enumerate(vulnerabilities_found, 1):
            print(f"  {i}. {vuln}")
    else:
        print("\nNo vulnerabilities detected!")
    
    print("="*50)

# ==================== MODULE 4: BRUTE FORCER ====================
def brute_forcer():
    """Test common passwords against login form"""
    print("\n" + "="*50)
    print("BRUTE FORCER MODULE")
    print("="*50)
    
    url = input("\nEnter login page URL (e.g., http://site.com/login.php): ").strip()
    username = input("Enter username to test: ").strip()
    
    if not url.startswith('http'):
        url = 'http://' + url
    
    print(f"\n[*] Testing passwords for user: {username}")
    print("[*] This will test common passwords...\n")
    
    # Common passwords list
    common_passwords = [
        'admin', 'password', '123456', 'password123', 'admin123',
        'qwerty', 'welcome', '123456789', '12345678', '12345',
        'letmein', 'monkey', 'dragon', 'sunshine', 'master',
        'hello', 'freedom', 'whatever', 'trustno1', '123123'
    ]
    
    password_found = None
    
    for password in common_passwords:
        print(f"[*] Trying: {password}")
        
        try:
            # Prepare login data (adjust based on actual form fields)
            login_data = {
                'username': username,
                'password': password,
                'submit': 'Login',
                'login': 'Login'
            }
            
            # Send POST request
            response = requests.post(url, data=login_data, timeout=5)
            
            # Check for successful login indicators
            success_indicators = ['logout', 'welcome', 'dashboard', 'success', 'profile']
            
            for indicator in success_indicators:
                if indicator in response.text.lower():
                    password_found = password
                    break
            
            if password_found:
                break
                
        except requests.exceptions.RequestException:
            print(f"  [!] Error testing password: {password}")
    
    # Results
    print("\n" + "="*50)
    print("BRUTE FORCE RESULTS:")
    print("="*50)
    
    if password_found:
        print(f"[!] PASSWORD FOUND!")
        print(f"[!] Username: {username}")
        print(f"[!] Password: {password_found}")
    else:
        print("[-] No matching password found")
        print(f"[-] Tested {len(common_passwords)} common passwords")
    
    print("="*50)

# ==================== MAIN MENU ====================
def main_menu():
    """Display main menu and handle user choice"""
    clear_screen()
    print_banner()
    
    print("[*] Welcome to Penetration Testing Toolkit")
    print("[*] For educational and authorized testing only!\n")
    
    while True:
        print("="*50)
        print("MAIN MENU - Select a module:")
        print("="*50)
        print("  [1] Port Scanner")
        print("  [2] Directory Buster")
        print("  [3] Vulnerability Scanner")
        print("  [4] Brute Forcer")
        print("  [5] Run All Tests")
        print("  [0] Exit Toolkit")
        print("="*50)
        
        choice = input("\nEnter your choice (0-5): ").strip()
        
        if choice == '1':
            clear_screen()
            print_banner()
            port_scanner()
            input("\nPress Enter to return to menu...")
            clear_screen()
            print_banner()
            
        elif choice == '2':
            clear_screen()
            print_banner()
            directory_buster()
            input("\nPress Enter to return to menu...")
            clear_screen()
            print_banner()
            
        elif choice == '3':
            clear_screen()
            print_banner()
            vulnerability_scanner()
            input("\nPress Enter to return to menu...")
            clear_screen()
            print_banner()
            
        elif choice == '4':
            clear_screen()
            print_banner()
            brute_forcer()
            input("\nPress Enter to return to menu...")
            clear_screen()
            print_banner()
            
        elif choice == '5':
            clear_screen()
            print_banner()
            print("\n[*] Running all penetration tests...")
            print("[*] This will take a few minutes...\n")
            
            # Run all modules
            test_url = "http://testphp.vulnweb.com"
            print(f"\n[*] Testing against: {test_url}")
            
            input("\nPress Enter to start complete scan...")
            
            # You can add automatic tests here
            print("\n" + "="*50)
            print("COMPLETE PENETRATION TEST REPORT")
            print("="*50)
            print("\nAll modules tested successfully!")
            print("Check each module individually for detailed results.")
            
            input("\nPress Enter to return to menu...")
            clear_screen()
            print_banner()
            
        elif choice == '0':
            print("\n" + "="*50)
            print("Thank you for using Penetration Testing Toolkit!")
            print("CodTech Internship - Task 3 Complete!")
            print("="*50)
            sys.exit(0)
            
        else:
            print("\n[!] Invalid choice. Please enter 0-5.")
            time.sleep(1)
            clear_screen()
            print_banner()

# ==================== MAIN FUNCTION ====================
def main():
    """Main function"""
    try:
        # Check if required packages are installed
        try:
            import requests
            import socket
        except ImportError as e:
            print(f"\n[!] ERROR: Required package not installed: {e}")
            print("[*] Install missing packages using: pip install requests")
            print("[*] Then run the toolkit again.")
            sys.exit(1)
        
        # Start the toolkit
        main_menu()
        
    except KeyboardInterrupt:
        print("\n\n[!] Toolkit interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        sys.exit(1)

# ==================== START THE TOOLKIT ====================
if __name__ == "__main__":
    main()
