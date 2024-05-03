import requests
from bs4 import BeautifulSoup
import re
import sys

def extract_links(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []

            # Extract links from 'href' attributes
            href_links = soup.find_all(href=True)
            for link in href_links:
                links.append(link.get('href'))

            # Extract links from 'src' attributes
            src_links = soup.find_all(src=True)
            for link in src_links:
                links.append(link.get('src'))

            # Extract links containing 'http' or 'https'
            http_links = re.findall(r'(http://|https://)\S+', response.text)
            links.extend(http_links)

            filtered_links = [link for link in links if not (link == 'http://' or link == 'https://')]
            
            return filtered_links
        else:
            print("Failed to fetch page:", response.status_code)
            return []
    except requests.RequestException as e:
        print("An error occurred:", e)
        return []


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 script.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    links = extract_links(url)

    print("\nLinks and paths found on [", url, "] :\n")
    for link in links:
        print(link)
    print("\n")
