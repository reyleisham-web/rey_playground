from pathlib import Path
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

EPUB_FILE = r"C:\Users\rmoodley\PycharmProjects\Personal Project - Rey\Book_Stuff\The Sweet Little Fulang .epub"

BASE_DIR = Path(__file__).parent

EDITED_DIR = BASE_DIR / "edited"

EDITED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# --------------------------------------------------
# PROMPT
# --------------------------------------------------

PROMPT_TEMPLATE = """
You are a professional Chinese-to-English novel editor.

The following text is a machine-translated chapter from:

《乖乖小夫郎》

Your task is to transform the chapter into natural, publication-quality English.

RULES:

- Preserve every plot detail.
- Preserve every scene.
- Preserve all character names exactly.
- Keep the term "ger".
- Preserve Chinese cultural concepts.
- Do not summarize.
- Do not omit information.
- Do not censor.
- Do not add plot elements.
- Rewrite awkward machine translation.
- Improve grammar.
- Improve dialogue.
- Improve narration.
- Improve readability.
- Replace literal Chinese idioms with natural English equivalents.
- Return ONLY the rewritten chapter.

CHAPTER:

{chapter_text}
"""

# --------------------------------------------------
# LOAD EPUB
# --------------------------------------------------

print("Loading EPUB...")

source_book = epub.read_epub(EPUB_FILE)

# --------------------------------------------------
# CREATE NEW EPUB
# --------------------------------------------------

new_book = epub.EpubBook()

new_book.set_identifier(
    "sweet-little-fulang-edited"
)

new_book.set_title(
    "The Sweet Little Fulang (Edited)"
)

new_book.set_language("en")

chapters = []

chapter_number = 1

# --------------------------------------------------
# PROCESS CHAPTERS
# --------------------------------------------------

for item in source_book.get_items():

    if item.get_type() != ITEM_DOCUMENT:
        continue

    filename = item.get_name().lower()

    if "nav" in filename:
        continue

    html = item.get_content().decode(
        "utf-8",
        errors="ignore"
    )

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    chapter_text = soup.get_text("\n")

    chapter_text = "\n".join(
        line.strip()
        for line in chapter_text.splitlines()
        if line.strip()
    )

    if len(chapter_text) < 300:
        continue

    print(
        f"Processing Chapter {chapter_number}"
    )

    prompt = PROMPT_TEMPLATE.format(
        chapter_text=chapter_text
    )

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )

    edited_text = (
        response
        if isinstance(response, str)
        else str(response)
    )

    # Save TXT copy

    txt_file = (
        EDITED_DIR
        / f"chapter_{chapter_number:03d}_edited.txt"
    )

    txt_file.write_text(
        edited_text,
        encoding="utf-8"
    )

    # Create EPUB chapter

    epub_chapter = epub.EpubHtml(
        title=f"Chapter {chapter_number}",
        file_name=f"chapter_{chapter_number:03d}.xhtml",
        lang="en"
    )

    paragraphs = []

    for line in edited_text.splitlines():

        line = line.strip()

        if not line:
            continue

        paragraphs.append(
            f"<p>{line}</p>"
        )

    epub_chapter.content = f"""
    <h1>Chapter {chapter_number}</h1>
    {''.join(paragraphs)}
    """

    new_book.add_item(
        epub_chapter
    )

    chapters.append(
        epub_chapter
    )

    chapter_number += 1

    time.sleep(1)

# --------------------------------------------------
# EPUB STRUCTURE
# --------------------------------------------------

new_book.toc = chapters

new_book.spine = ["nav"] + chapters

new_book.add_item(
    epub.EpubNcx()
)

new_book.add_item(
    epub.EpubNav()
)

# --------------------------------------------------
# STYLING
# --------------------------------------------------

style = """
body {
    font-family: Georgia, serif;
    line-height: 1.6;
    margin-left: 5%;
    margin-right: 5%;
}

h1 {
    text-align: center;
}

p {
    margin-bottom: 1em;
}
"""

css = epub.EpubItem(
    uid="style",
    file_name="style/style.css",
    media_type="text/css",
    content=style
)

new_book.add_item(css)

# --------------------------------------------------
# WRITE EPUB
# --------------------------------------------------

output_epub = (
    EDITED_DIR
    / "The_Sweet_Little_Fulang_Edited.epub"
)

epub.write_epub(
    str(output_epub),
    new_book
)

print()
print("DONE")
print(output_epub)