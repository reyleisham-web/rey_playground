with open("sweet_little_fulang_pt1_chapter_links_clean.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

print("Count:", len(lines))
print("First:", lines[0])