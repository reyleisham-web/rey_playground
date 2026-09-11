from pathlib import Path
import shutil

PT1_DIR = Path(
    "chapters/sweet_little_fulang_pt1"
)

PT2_DIR = Path(
    "chapters/sweet_little_fulang_pt2"
)

OUTPUT_DIR = Path(
    "chapters/sweet_little_fulang"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

counter = 1

# PT1 first
for file in sorted(
    PT1_DIR.glob("*.txt")
):

    new_name = (
        f"The Sweet Little Fulang Chapter "
        f"{counter}.txt"
    )

    shutil.copy2(
        file,
        OUTPUT_DIR / new_name
    )

    print(
        f"{file.name} -> {new_name}"
    )

    counter += 1

# PT2 second
for file in sorted(
    PT2_DIR.glob("*.txt")
):

    new_name = (
        f"The Sweet Little Fulang Chapter "
        f"{counter}.txt"
    )

    shutil.copy2(
        file,
        OUTPUT_DIR / new_name
    )

    print(
        f"{file.name} -> {new_name}"
    )

    counter += 1

print()
print(
    f"Merged {counter - 1} chapters"
)