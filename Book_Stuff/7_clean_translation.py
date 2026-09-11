from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from utils.yaml_loader import NOVEL_CONFIG
import os
import time
import re

# --------------------------
# CONFIG
# --------------------------

SLUG = NOVEL_CONFIG["book"]["slug"]

CHINESE_TITLE = (
    NOVEL_CONFIG["book"]["chinese_title"]
)

MODEL = (
    NOVEL_CONFIG["translation"]["model"]
)

# --------------------------
# OPENAI
# --------------------------

load_dotenv()

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)

# --------------------------
# PATHS
# --------------------------

BASE_DIR = Path(__file__).parent

CHAPTERS_DIR = (
    BASE_DIR
    / "chapters"
    / SLUG
)

EPUB_NAME = (
    NOVEL_CONFIG["epub"]["filename"]
)

CORRECTED_DIR = (
    BASE_DIR
    / "corrected_translations"
    / f"{EPUB_NAME}_corrected"
)

CORRECTED_DIR.mkdir(
    parents=True,
    exist_ok=True
)
# --------------------------
# PROMPT
# --------------------------

PROMPT_TEMPLATE = f"""
You are a professional Chinese-to-English novel editor.

The following text is a machine-translated chapter from:

《{CHINESE_TITLE}》

Your task is to transform the chapter into
natural, publication-quality English.

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

{{chapter_text}}
"""

# --------------------------
# LOAD CHAPTERS
# --------------------------

def chapter_key(file):

    stem = file.stem.lower()

    numbers = [
        int(n)
        for n in re.findall(
            r"\d+",
            stem
        )
    ]

    return numbers

def chapter_key(file):
    return [
        int(n)
        for n in re.findall(r"\d+", file.stem)
    ]

chapter_files = sorted(
    CHAPTERS_DIR.glob("*.txt"),
    key=chapter_key
)

chapter_files = sorted(
    CHAPTERS_DIR.glob("*.txt"),
    key=chapter_key
)
chapter_files = sorted(
    CHAPTERS_DIR.glob("*.txt"),
    key=lambda f: int(
        re.search(r"(\d+)", f.stem).group(1)
    )
)

print(
    f"Found {len(chapter_files)} chapters"
)

# --------------------------
# PROCESS
# --------------------------

for chapter_file in chapter_files:

    output_file = (
        CORRECTED_DIR /
        f"{chapter_file.stem}_corrected.txt"
    )

    if output_file.exists():

        print(
            f"Skipping {chapter_file.name}"
        )

        continue

    print(
        f"Processing {chapter_file.name}"
    )

    chapter_text = (
        chapter_file.read_text(
            encoding="utf-8",
            errors="ignore"
        )
    )

    prompt = (
        PROMPT_TEMPLATE.format(
            chapter_text=chapter_text
        )
    )

    response = client.responses.create(
        model=MODEL,
        input=prompt
    )

    edited_text = response.output_text

    output_file.write_text(
        edited_text,
        encoding="utf-8"
    )

    print(
        f"Saved {output_file.name}"
    )

    time.sleep(1)

print()
print("All chapters processed.")
