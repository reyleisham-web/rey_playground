from ebooklib import epub, ITEM_DOCUMENT

book = epub.read_epub("Transmigration_Farming.epub")

for item in book.get_items():

    if item.get_type() != ITEM_DOCUMENT:
        continue

    if item.get_name() == "nav.xhtml":
        continue

    content = item.get_content().decode(
        "utf-8",
        errors="ignore"
    )

    print("=" * 80)
    print(item.get_name())
    print(content[:1000])
    break