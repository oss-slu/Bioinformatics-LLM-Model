import requests
import re
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.datasciencemeta.com/rpackages"
OUTPUT_JSON_FILE = "r_package_descriptions.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

def get_package_links(base_url, top_n=100):
    """Fetch the package links from the base URL."""
    response = requests.get(base_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch {base_url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    package_links = []

    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('https://cran.r-project.org/web/packages/') and href.endswith('/index.html'):
            package_links.append(href)
        if len(package_links) >= top_n:
            break

    return package_links

def extract_package_description(package_url):
    """Extracts the description of the package from its CRAN page."""
    response = requests.get(package_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch {package_url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    description_tag = soup.find('p')
    if description_tag:
        return description_tag.text.strip()
    
    return None

def main():
    package_links = get_package_links(BASE_URL)
    extracted_data = {}

    for package_url in package_links:
        print(f"Processing package: {package_url}")
        package_name = package_url.split("/")[-2]
        description = extract_package_description(package_url)
        
        if description:
            extracted_data[package_name] = description
            print(f"Extracted description for {package_name}")
        else:
            print(f"No description found for {package_name}")
        
        time.sleep(1)
    
    with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4)

    print(f"All extracted descriptions saved to {OUTPUT_JSON_FILE}")

if __name__ == "__main__":
    main()
