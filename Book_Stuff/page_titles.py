from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time

driver = webdriver.Chrome()

with open("sweet_little_fulang_pt1_chapter_links_clean.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

results = []

try:
    for i, url in enumerate(urls, start=1):

        print(f"[{i}/{len(urls)}] {url}")

        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        title = soup.title.get_text(strip=True) if soup.title else "NO TITLE"

        results.append((title, url))

finally:
    driver.quit()

with open("created_files/chapter_titles.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)

    writer.writerow(["Title", "URL"])

    for row in results:
        writer.writerow(row)

print(f"Saved {len(results)} rows to chapter_titles.csv")