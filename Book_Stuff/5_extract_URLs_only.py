import re
from pathlib import Path

INPUT_FILE = Path(
    "created_files/sweet_little_fulang_pt2_chapter_links_clean.txt"
)

OUTPUT_FILE = Path(
    "created_files/sweet_little_fulang_pt2_urls_only.txt"
)

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:
    content = f.read()

urls = re.findall(
    r'https://[^"\s<]+',
    content
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    for url in urls:
        f.write(url + "\n")

print(f"Extracted {len(urls)} URLs")
print(f"Saved to {OUTPUT_FILE}")

print(urls[0])
print(urls[1])
print(urls[2])