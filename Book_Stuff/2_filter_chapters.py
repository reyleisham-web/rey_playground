from utils.yaml_loader import NOVEL_CONFIG

SLUG = NOVEL_CONFIG["book"]["slug"]
URL_KEYWORD = NOVEL_CONFIG["scraper"]["url_keyword"]

INPUT_FILE = (
    f"created_files/{SLUG}_all_links.txt"
)

OUTPUT_FILE = (
    f"created_files/{SLUG}_chapter_links.txt"
)

chapter_links = []

with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        url = line.strip()

        if (
            URL_KEYWORD in url.lower()
            and "#more" not in url
            and "#comment-form" not in url
            and "/search/label/" not in url
        ):
            chapter_links.append(url)

# Remove duplicates
chapter_links = sorted(set(chapter_links))

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write("\n".join(chapter_links))

print(
    f"Found {len(chapter_links)} chapter URLs"
)

print(
    f"Saved to {OUTPUT_FILE}"
)