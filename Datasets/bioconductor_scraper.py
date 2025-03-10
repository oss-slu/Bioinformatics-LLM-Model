import requests
import json
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (no GUI)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

GITHUB_API_BASE = "https://api.github.com/repos/Bioconductor"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Mozilla/5.0"
}

# OPTIONAL: Add a GitHub token to increase API limits
GITHUB_TOKEN = ""  # Add your token here
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

package_r_code = {}
scraped_count = 0  # Counter for successfully scraped packages
max_scrapes = 100  # Stop after 100 packages
output_file = "bioconductor_r_code.json"


def save_progress(retries=3, delay=2):
    """Save current progress to a file with error handling (without using a temp file)."""
    for attempt in range(retries):
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(package_r_code, f, indent=4, ensure_ascii=False)
            
            print(f"Progress successfully saved to {output_file}")
            return
        except (OSError, IOError, json.JSONDecodeError) as e:
            print(f"Error saving progress (Attempt {attempt + 1}/{retries}): {e}")
            time.sleep(delay)  # Wait before retrying

    print("Failed to save progress after multiple attempts. Data may be lost.")

    print("Failed to save progress after multiple attempts. Data may be lost.")

def get_bioconductor_packages():
    """Scrape Bioconductor package names using Selenium."""
    url = "https://bioconductor.org/packages/release/BiocViews.html#___Software"
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "biocViews_package_table"))
        )
    except Exception as e:
        print("Failed to load package table:", e)
        driver.quit()
        return []

    package_elements = driver.find_elements(By.CSS_SELECTOR, "#biocViews_package_table tbody tr")
    package_names = [pkg.get_attribute("id").replace("pkg_", "").strip() for pkg in package_elements]

    driver.quit()
    return package_names

package_names = get_bioconductor_packages()

def check_rate_limit():
    """Check remaining GitHub API rate limit."""
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        rate_info = response.json()
        remaining = rate_info["rate"]["remaining"]
        reset_time = rate_info["rate"]["reset"]
        return remaining, reset_time
    return None, None

def wait_for_rate_limit():
    """Wait until rate limit resets."""
    remaining, reset_time = check_rate_limit()
    if remaining is not None and remaining == 0:
        reset_timestamp = datetime.datetime.fromtimestamp(reset_time)
        wait_seconds = (reset_timestamp - datetime.datetime.now()).total_seconds()
        print(f"Rate limit reached. Waiting for {wait_seconds} seconds...")
        time.sleep(wait_seconds + 1)  # Add a buffer to ensure rate limit is reset

def get_r_files_from_github(package_name):
    """Fetch all R files in the package's GitHub 'R/' directory."""
    api_url = f"{GITHUB_API_BASE}/{package_name}/contents/R?ref=devel"
    r_code = {}

    for _ in range(3):  # Retry up to 3 times in case of failure
        try:
            wait_for_rate_limit()
            response = requests.get(api_url, headers=HEADERS)
            if response.status_code == 403:
                print(f"Rate limited while fetching {package_name}. Retrying...")
                time.sleep(10)
                continue
            if response.status_code != 200:
                print(f"Could not access {package_name}/R directory (Status: {response.status_code})")
                return None

            files = response.json()
            for file in files:
                if file["type"] == "file" and file["name"].endswith(".R"):
                    file_url = file["download_url"]
                    file_content = download_file(file["name"], file_url)
                    if file_content:
                        r_code[file["name"]] = file_content
            return r_code if r_code else None

        except Exception as e:
            print(f"Error processing {package_name}: {e}")
            time.sleep(1)  # Wait before retrying
    return None

def download_file(file_name, file_url):
    """Download and return the content of an R file."""
    response = requests.get(file_url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Could not fetch {file_url}")
        return None

# Iterate through the packages and fetch R files
try:
    for package in package_names:
        if scraped_count >= max_scrapes:
            break  # Stop when 100 packages are scraped

        print(f"Fetching R files for {package}...")
        r_code = get_r_files_from_github(package)

        if r_code:
            package_r_code[package] = r_code
            scraped_count += 1
            print(f"Successfully scraped {package} ({scraped_count}/{max_scrapes})")

            # Save after every package
            save_progress()

            # Save a backup every 10 packages


except Exception as e:
    print(f"Script encountered an error: {e}")
    save_progress()

# Final save
if package_r_code:
    save_progress()
    print(f"\n Scraping complete! {scraped_count} packages successfully scraped.")
else:
    print("\n No R files were successfully scraped.")
