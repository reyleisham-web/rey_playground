from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from utils.yaml_loader import NOVEL_CONFIG
import time
import re

# --------------------------
# CONFIG
# --------------------------

SLUG = NOVEL_CONFIG["book"]["slug"]

CHAPTER_CONTAINER = (
    NOVEL_CONFIG["scraper"]["chapter_container"]
)

# --------------------------
# PATHS
# --------------------------

BASE_DIR = Path(__file__).parent

URL_FILE = (
    BASE_DIR
    / "created_files"
    / f"{SLUG}_chapter_links_clean.txt"
)

CHAPTERS_DIR = (
    BASE_DIR
    / "chapters"
    / SLUG
)

CHAPTERS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# --------------------------
# LOAD URLS
# --------------------------

with open(
    URL_FILE,
    "r",
    encoding="utf-8"
) as f:

    urls = [
        line.strip()
        for line in f
        if line.strip()
    ]

# TEST MODE
# urls = urls[:1]

print(f"Found {len(urls)} URLs")

# --------------------------
# BROWSER
# --------------------------

options = Options()

options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    options=options
)

# --------------------------
# SCRAPE
# --------------------------

try:

    for index, url in enumerate(
        urls,
        start=1
    ):

        print(
            f"[{index}/{len(urls)}] {url}"
        )

        output_file = (
            CHAPTERS_DIR /
            f"chapter_{index:04d}.txt"
        )

        if output_file.exists():

            print(
                f"Skipping {output_file.name}"
            )

            continue

        driver.get(url)

        time.sleep(2)

        soup = BeautifulSoup(
            driver.page_source,
            "html.parser"
        )

        content = soup.select_one(
            CHAPTER_CONTAINER
        )

        if not content:

            print(
                f"Could not find content using "
                f"'{CHAPTER_CONTAINER}'"
            )

            continue

        # --------------------------
        # CHAPTER TITLE
        # --------------------------

        page_title = (
            soup.title.get_text(strip=True)
            if soup.title
            else ""
        )

        match = re.search(
            r"chapter-(.+?)\.html",
            url,
            re.IGNORECASE
        )

        if match:

            chapter_name = (
                match.group(1)
                .replace("-", "_")
            )

            filename = (
                f"chapter_{chapter_name}.txt"
            )

            chapter_title = (
                chapter_name
                .replace("_", " ")
                .title()
            )

        else:

            filename = (
                f"chapter_{index:04d}.txt"
            )

            chapter_title = (
                f"Chapter {index}"
            )

        output_file = (
                CHAPTERS_DIR /
                filename
        )

        # --------------------------
        # CHAPTER TEXT
        # --------------------------

        chapter_text = content.get_text(
            "\n",
            strip=True
        )

        full_text = (
            f"{chapter_title}\n\n"
            f"{chapter_text}"
        )

        output_file.write_text(
            full_text,
            encoding="utf-8"
        )

        print(
            f"Saved {output_file.name}"
        )

finally:

    driver.quit()

print()
print("Finished.")