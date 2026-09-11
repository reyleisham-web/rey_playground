import re
from utils.yaml_loader import NOVEL_CONFIG

SLUG = NOVEL_CONFIG["book"]["slug"]

INPUT_FILE = (
    f"created_files/{SLUG}_chapter_links.txt"
)

OUTPUT_FILE = (
    f"created_files/{SLUG}_chapter_links_clean.txt"
)

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:
    content = f.read()

# Extract URLs
urls = set(
    re.findall(
        r'https://[^\s"<]+',
        content
    )
)


def chapter_key(url):
    match = re.search(
        r'chapter-(\d+)',
        url,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return 999999


urls = sorted(
    urls,
    key=chapter_key
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    for url in urls:
        f.write(url + "\n")

print(f"Saved {len(urls)} clean URLs")
print(f"Output: {OUTPUT_FILE}")

print(urls[0])
print(urls[1])
print(urls[2])