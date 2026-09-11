from pathlib import Path

CHAPTERS_DIR = Path(
    "../chapters/sweet_little_fulang_pt1"
)

files = sorted(
    CHAPTERS_DIR.glob("*.txt")
)

for index, file in enumerate(
    files,
    start=1
):

    new_name = (
        f"The Sweet Little Fulang "
        f"Chapter {index}.txt"
    )

    new_file = (
        CHAPTERS_DIR /
        new_name
    )

    print(
        f"{file.name} -> {new_name}"
    )

    file.rename(new_file)

print("Finished.")