from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"

print("Looking for:")
print(env_path)

print()
print("Exists?")
print(env_path.exists())

if env_path.exists():
    print()
    print("Contents:")
    print(env_path.read_text())
