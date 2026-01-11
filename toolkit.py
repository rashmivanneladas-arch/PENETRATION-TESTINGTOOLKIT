#!/usr/bin/env python3
"""
PENETRATION TESTING TOOLKIT - CodTech Internship Task 3
"""

import os
import sys
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

def main_menu():
    """Display main menu"""
    print("[*] Select a module to run:\n")
    
    modules = {
        '1': ('Port Scanner', 'Scan open ports'),
        '2': ('Directory Buster', 'Find hidden directories'),
        '3': ('Vulnerability Scanner', 'Check for SQLi/XSS'),
        '4': ('Brute Forcer', 'Test common passwords'),
        '0': ('Exit', 'Exit toolkit')
    }
    
    for key, (name, desc) in modules.items():
        print(f"  [{key}] {name:25} - {desc}")
    
    print("\n" + "─" * 60)
    return modules

def run_module(choice):
    """Run selected module"""
    clear_screen()
    print_banner()
    
    if choice == '1':
        from modules.port_scanner import PortScanner
        target = input("\n[?] Enter target (e.g., 192.168.1.1): ").strip()
        scanner = PortScanner(target)
        scanner.scan()
        
    elif choice == '2':
        from modules.directory_buster import DirectoryBuster
        target = input("\n[?] Enter URL (e.g., http://example.com): ").strip()
        buster = DirectoryBuster(target)
        buster.scan()
        
    elif choice == '3':
        from modules.vulnerability_scanner import VulnerabilityScanner
        target = input("\n[?] Enter URL: ").strip()
        scanner = VulnerabilityScanner(target)
        scanner.scan_all()
        
    elif choice == '4':
        from modules.brute_forcer import BruteForcer
        target = input("\n[?] Enter login URL: ").strip()
        username = input("[?] Username to test: ").strip()
        brute = BruteForcer(target, username)
        brute.start()
        
    elif choice == '0':
        print("\n[+] Thank you for using Penetration Testing Toolkit!")
        sys.exit(0)
    
    input("\n[*] Press Enter to continue...")

def main():
    """Main function"""
    clear_screen()
    print_banner()
    
    print("[*] Welcome! For educational purposes only!")
    print("[*] Only test systems you have permission to test!\n")
    
    while True:
        modules = main_menu()
        choice = input("\n[?] Select option (0-4): ").strip()
        
        if choice in modules:
            run_module(choice)
            clear_screen()
            print_banner()
        else:
            print("\n[!] Invalid choice. Please try again.")
            time.sleep(1)
            clear_screen()
            print_banner()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Toolkit interrupted by user.")
        sys.exit(0)
