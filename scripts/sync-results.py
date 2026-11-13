"""Embed the editable quantitative results fragment into the static project page."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
page = root / "index.html"
start = "<!-- RESULTS:START -->"
end = "<!-- RESULTS:END -->"
before, rest = page.read_text(encoding="utf-8").split(start, 1)
_, after = rest.split(end, 1)
fragment = (root / "static/results-tables.html").read_text(encoding="utf-8").strip()
page.write_text(before + start + "\n" + fragment + "\n" + end + after, encoding="utf-8")
print("Updated index.html from static/results-tables.html")
