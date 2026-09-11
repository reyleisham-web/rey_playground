import re

html_or_url = input(
    "https://thenightwithoutthedawn.blogspot.com/search/label/The%20sweet%20little%20Fulang?m=1':\n"
)

# Try to extract href
match = re.search(
    r'href="([^"]+)"',
    html_or_url
)

if match:

    print("\nExtracted URL:")
    print(match.group(1))

else:

    # Fallback: assume it's already a URL
    match = re.search(
        r'https?://[^\s"<]+',
        html_or_url
    )

    if match:

        print("\nExtracted URL:")
        print(match.group(0))

    else:

        print("No URL found.")