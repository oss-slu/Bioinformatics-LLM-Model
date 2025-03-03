import requests
import re
from bs4 import BeautifulSoup
import time
import json
import os

BASE_URL = "https://www.datasciencemeta.com/rpackages"
OUTPUT_JSON_FILE = "r_package_examples.json"
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
        if href.startswith('https://cran.r-project.org/web/packages/'):
            package_links.append(href)
        if len(package_links) >= top_n:
            break

    return package_links


def extract_github_url(package_url):
    """Extract the GitHub URL from the package's CRAN page."""
    response = requests.get(package_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch {package_url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    url_row = soup.find('td', string=re.compile(r'URL:', re.I))

    if url_row:
        next_td = url_row.find_next_sibling('td')
        if next_td:
            links = [a['href'] for a in next_td.find_all('a', href=True)]
            for url in links:
                if 'github.com' in url:
                    return url

    return None


def construct_man_folder_url(github_url):
    """Construct the 'man' folder URL from the GitHub repository URL."""
    if github_url.endswith('/'):
        github_url = github_url[:-1]

    man_url_main = f"{github_url}/tree/main/man"
    man_url_master = f"{github_url}/tree/master/man"

    for man_url in [man_url_main, man_url_master]:
        response = requests.get(man_url, headers=HEADERS)
        if response.status_code == 200:
            return man_url

    return None


def get_rd_files(man_folder_url):
    """Retrieve .Rd file links from the 'man' folder in GitHub UI."""
    response = requests.get(man_folder_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch {man_folder_url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    rd_files = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.endswith(".Rd") and "blob" in href:
            raw_url = "https://raw.githubusercontent.com" + href.replace("/blob", "")
            rd_files.append(raw_url)

    return rd_files


def extract_examples_from_rd(rd_url):
    """Extracts the full \examples{} section while handling nested braces."""
    response = requests.get(rd_url, headers=HEADERS)

    if response.status_code == 429:
        print("Rate limited by GitHub. Sleeping for 60 seconds before retrying...")
        time.sleep(60)
        response = requests.get(rd_url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Failed to fetch {rd_url}")
        return None

    content = response.text

    start_match = re.search(r"\\examples\s*\{", content)
    if not start_match:
        return None

    start_index = start_match.end()
    brace_count = 1
    end_index = start_index

    while end_index < len(content) and brace_count > 0:
        if content[end_index] == "{":
            brace_count += 1
        elif content[end_index] == "}":
            brace_count -= 1
        end_index += 1

    examples_body = content[start_index:end_index - 1].strip()
    return examples_body

def main():
    package_links = get_package_links(BASE_URL)
    extracted_data = {}

    for package_url in package_links:
        print(f"Processing package: {package_url}")
        github_url = extract_github_url(package_url)
        
        if not github_url:
            print(f"No GitHub URL found for {package_url}")
            continue

        print(f"GitHub URL found: {github_url}")

        man_url = construct_man_folder_url(github_url)
        
        if not man_url:
            print(f"No 'man' folder found for {github_url}")
            continue

        print(f"Found 'man' folder: {man_url}")

        rd_files = get_rd_files(man_url)
        
        if not rd_files:
            print(f"No .Rd files found in {man_url}")
            continue

        package_name = github_url.split("/")[-1]
        extracted_data[package_name] = {}

        for rd_file in rd_files:
            function_name = rd_file.split('/')[-1].replace(".Rd", "")
            example_code = extract_examples_from_rd(rd_file)

            if example_code:
                extracted_data[package_name][function_name] = example_code
                print(f"Extracted examples from {function_name}")
            else:
                print(f"No \\examples section found in {function_name}.")

        time.sleep(1)

    with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4)

    print(f"All extracted examples saved to {OUTPUT_JSON_FILE}")


if __name__ == "__main__":
    main()