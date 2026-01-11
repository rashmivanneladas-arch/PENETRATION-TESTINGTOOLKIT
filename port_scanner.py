"""
Port Scanner Module
"""
import socket

class PortScanner:
    def __init__(self, target):
        self.target = target
        self.open_ports = []
    
    def scan(self):
        print(f"\n[*] Scanning {self.target}...")
        
        # Scan common ports
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080]
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((self.target, port))
                sock.close()
                
                if result == 0:
                    print(f"[+] Port {port} is OPEN")
                    self.open_ports.append(port)
            except:
                pass
        
        print(f"\n[*] Scan complete! Found {len(self.open_ports)} open ports")
