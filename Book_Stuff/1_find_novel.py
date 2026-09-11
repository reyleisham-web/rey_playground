from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from utils.yaml_loader import NOVEL_CONFIG
import time

START_URL = NOVEL_CONFIG["crawler"]["start_url"]

OUTPUT_FILE = (
    f"created_files/"
    f"{NOVEL_CONFIG['book']['slug']}_all_links.txt"
)

print(
    f"Starting crawl for: "
    f"{NOVEL_CONFIG['book']['title']}"
)

options = Options()

# Run headless
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)


visited_pages = set()
all_links = set()

try:
    current_url = START_URL

    while current_url:

        if current_url in visited_pages:
            break

        visited_pages.add(current_url)

        print(f"\nOpening page {len(visited_pages)}")
        print(current_url)

        driver.get(current_url)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        page_links = 0

        for link in soup.find_all("a", href=True):

            href = link["href"].strip()

            if href not in all_links:
                all_links.add(href)
                page_links += 1

        print(f"Found {page_links} new links")
        print(f"Total links: {len(all_links)}")

        # Find Older Posts link
        next_page = None

        for link in soup.find_all("a", href=True):

            text = link.get_text(" ", strip=True).lower()

            if (
                "postingan lama" in text
                or "older posts" in text
            ):
                next_page = link["href"].strip()
                break

        current_url = next_page

    print(f"\nFinished.")
    print(f"Collected {len(all_links)} unique URLs.")

    # Save everything
    with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
    ) as f:

        for url in sorted(all_links):
            f.write(url + "\n")

    print(f"Saved {OUTPUT_FILE}")

finally:
    driver.quit()