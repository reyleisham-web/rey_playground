from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    PageBreak,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import enums

EPUB_FILE = r"/Book_Stuff/Transmigration_Farming_Reordered.epub"

PDF_FILE = r"/Book_Stuff/Transmigration_Farming_Reordered.pdf"

book = epub.read_epub(EPUB_FILE)

doc = SimpleDocTemplate(PDF_FILE)

styles = getSampleStyleSheet()

body_style = styles["BodyText"]
body_style.alignment = enums.TA_LEFT

heading_style = styles["Heading1"]

story = []

chapter_num = 1

for item in book.get_items():
    if item.get_type() != ITEM_DOCUMENT:
        continue

    if item.get_name() == "nav.xhtml":
        continue

    html = item.get_content().decode(
        "utf-8",
        errors="ignore"
    )

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    text = soup.get_text("\n")

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        continue

    story.append(
        Paragraph(
            f"Chapter {chapter_num}",
            heading_style
        )
    )

    story.append(Spacer(1, 12))

    for line in lines:
        story.append(
            Paragraph(
                line,
                body_style
            )
        )

    story.append(PageBreak())

    print(
        f"Processed Chapter {chapter_num}"
    )

    chapter_num += 1

doc.build(story)

print()
print("PDF created:")
print(PDF_FILE)