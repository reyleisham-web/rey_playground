from pathlib import Path
from ebooklib import epub

BASE_DIR = Path(__file__).parent

EDITED_DIR = BASE_DIR / "edited"

OUTPUT_EPUB = (
    BASE_DIR /
    "The_Sweet_Little_Fulang_Edited.epub"
)

# --------------------------
# CREATE BOOK
# --------------------------

book = epub.EpubBook()

book.set_identifier(
    "sweet_little_fulang_edited"
)

book.set_title(
    "The Sweet Little Fulang"
)

book.set_language("en")

book.add_author("Edited Translation")

chapters = []

# --------------------------
# ADD CHAPTERS
# --------------------------

chapter_files = sorted(
    EDITED_DIR.glob("*_edited.txt")
)

for index, chapter_file in enumerate(
    chapter_files,
    start=1
):

    text = chapter_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    chapter = epub.EpubHtml(
        title=f"Chapter {index}",
        file_name=f"chapter_{index:03d}.xhtml",
        lang="en"
    )

    paragraphs = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        paragraphs.append(
            f"<p>{line}</p>"
        )

    chapter.content = f"""
    <h1>Chapter {index}</h1>
    {''.join(paragraphs)}
    """

    book.add_item(chapter)

    chapters.append(chapter)

    print(
        f"Added Chapter {index}"
    )

# --------------------------
# TOC
# --------------------------

book.toc = chapters

# --------------------------
# SPINE
# --------------------------

book.spine = ["nav"] + chapters

# --------------------------
# EPUB NAV FILES
# --------------------------

book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# --------------------------
# CSS
# --------------------------

style = """
body {
    font-family: Georgia, serif;
    line-height: 1.5;
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
    uid="style_nav",
    file_name="style/style.css",
    media_type="text/css",
    content=style
)

book.add_item(css)

for chapter in chapters:
    chapter.add_item(css)

# --------------------------
# WRITE EPUB
# --------------------------

epub.write_epub(
    str(OUTPUT_EPUB),
    book
)

print()
print("EPUB CREATED:")
print(OUTPUT_EPUB)