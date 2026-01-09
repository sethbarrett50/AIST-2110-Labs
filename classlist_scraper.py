"""
Extract student names from a saved HTML class list from D2L.

Finds <a> tags whose "title" attribute contains "Compose email to ",
then reads the anchor text (e.g., "Smith, Mike") and rewrites it as
"Collin Smith" in an output text file (one name per line).
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


INPUT_HTML = Path("classlist.html")
OUTPUT_TXT = Path("names.txt")
TITLE_NEEDLE = "Compose email to "


def reverse_name(name: str) -> str:
    """
    Convert "Last, First Middle" -> "First Middle Last".
    If there's no comma, returns the cleaned original.
    """
    cleaned = " ".join(name.split())
    if "," not in cleaned:
        return cleaned

    last, rest = cleaned.split(",", 1)
    last = last.strip()
    rest = rest.strip()

    if not rest:
        return last

    return f"{rest} {last}"


def iter_names_from_html(html_text: str) -> Iterable[str]:
    from bs4 import BeautifulSoup  
    soup = BeautifulSoup(html_text, "html.parser")

    for a in soup.find_all("a"):
        title = a.get("title", "")
        if title and TITLE_NEEDLE in title:
            text = a.get_text(strip=True)
            if text:
                yield reverse_name(text)


def main() -> int:
    if not INPUT_HTML.exists():
        print(f"Error: input file not found: {INPUT_HTML.resolve()}")
        return 1

    html_text = INPUT_HTML.read_text(encoding="utf-8", errors="replace")

    names = sorted({n for n in iter_names_from_html(html_text) if n})

    if not names:
        print("No matching names found.")
        return 2

    OUTPUT_TXT.write_text("\n".join(names) + "\n", encoding="utf-8")
    print(f"Wrote {len(names)} names to {OUTPUT_TXT.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
