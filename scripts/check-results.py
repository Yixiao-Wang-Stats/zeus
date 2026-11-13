"""Compare published table values with uncommented camera-ready LaTeX.

Run from the checkout: python scripts/check-results.py [index.html]
The local, gitignored `orginal paper` folder is required for this audit only.
"""

from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
NUMBER = re.compile(r"[+-]?\d+(?:\.\d+)?")


class ResultsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.table = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "table" and "data-source" in attrs:
            self.table = {"source": attrs["data-source"], "index": int(attrs.get("data-source-table", "0")), "values": []}
            self.tables.append(self.table)
        elif tag == "td" and self.table is not None:
            self.cell = ""

    def handle_data(self, data):
        if self.cell is not None:
            self.cell += data

    def handle_endtag(self, tag):
        if tag == "td" and self.cell is not None:
            text = self.cell.strip().replace("−", "-").removesuffix("×")
            if NUMBER.fullmatch(text):
                self.table["values"].append(text)
            self.cell = None
        elif tag == "table":
            self.table = None


def source_values(relative, index):
    source = (ROOT / "orginal paper" / relative).read_text(encoding="utf-8")
    source = re.sub(r"(?m)(?<!\\)%.*$", "", source)
    tables = re.findall(r"\\begin\{tabular\*?\}.*?\\end\{tabular\*?\}", source, re.S)
    values = []
    for row in re.split(r"\\\\", tables[index]):
        if "&" not in row:
            continue
        numbers = []
        for cell in row.split("&")[1:]:
            # Remove presentation commands, preserving the number and its precision.
            cell = re.sub(r"\\[a-zA-Z]+(?:\[[^\]]*\])?", "", cell)
            cell = re.sub(r"[{}$\\()\s]", "", cell)
            if NUMBER.fullmatch(cell):
                numbers.append(cell)
        if len(numbers) >= 3:
            values.extend(numbers)
    return values


filename = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "static/results-tables.html")
parser = ResultsParser()
parser.feed(filename.read_text(encoding="utf-8"))
if len(parser.tables) != 7:
    raise SystemExit(f"Expected 7 source-linked tables; found {len(parser.tables)} in {filename.name}")
count = 0
for table in parser.tables:
    expected = source_values(table["source"], table["index"])
    actual = table["values"]
    if actual != expected:
        raise SystemExit(f"Mismatch in {table['source']} table {table['index']}:\nExpected {expected}\nActual   {actual}")
    count += len(actual)
    print(f"OK: {table['source']} table {table['index']} ({len(actual)} values)")
print(f"Verified {count} numeric result values across all 7 tables in {filename.name}.")
