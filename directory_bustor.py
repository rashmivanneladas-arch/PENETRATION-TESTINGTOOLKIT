1
"""
Directory Buster Module
"""
import requests

class DirectoryBuster:
    def __init__(self, url):
        self.url = url.rstrip('/')
    
    def scan(self):
        print(f"\n[*] Searching for hidden directories on {self.url}")
        
        common_dirs = ['admin', 'login', 'dashboard', 'wp-admin', 'config', 'backup', 'test']
        
        for directory in common_dirs:
            test_url = f"{self.url}/{directory}"
            try:
                response = requests.get(test_url, timeout=3)
                if response.status_code == 200:
                    print(f"[+] Found: /{directory}")
            except:
                pass
        
        print("\n[*] Directory scan complete")
