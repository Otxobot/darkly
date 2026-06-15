import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "http://localhost:8080/.hidden/"

visited = set()

FLAG_PATTERN = re.compile(r'\b[a-fA-F0-9]{64}\b')

def crawl(url):
    if url in visited:
        return
    visited.add(url)
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a'):
            href = link.get('href')
            
            if href == '../':
                continue
                
            full_url = url + href
            
            if href == 'README':
                file_response = requests.get(full_url)
                content = file_response.text.strip()

                match = FLAG_PATTERN.search(content)
                if match:
                    print(f"\n[+] SUCCESS! Flag encontrado en: {full_url}")
                    print(f"[-] Flag: {match.group(0)}\n")
                    sys.exit(0)
            
            elif href.endswith('/'):
                crawl(full_url)
                
    except Exception as e:
        pass

if __name__ == "__main__":
    print("[*] Empezando el bucle")
    crawl(BASE_URL)
    print("[*] Bucle finalizado")