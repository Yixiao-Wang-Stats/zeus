"""Check the public page's assets, metadata, anchors, and scripts without a browser."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ["index.html", "main_ani.html", "main_paper.html"]


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.scripts = []
        self.active_script = None
        self.in_title = False
        self.title = ""
        self.h1_count = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, f"Duplicate ID: {attrs['id']}"
            self.ids.add(attrs["id"])
        assert tag not in {"audio", "video"}, "Unexpected audio/video element"
        if tag == "img":
            assert "alt" in attrs, "Image needs alt text or an empty decorative alt"
        if tag == "iframe":
            assert attrs.get("title"), "Iframe needs a title"
        for key in ["src", "href"]:
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag == "script" and "src" not in attrs:
            self.active_script = ""
        self.in_title = tag == "title" or self.in_title
        if tag == "h1":
            self.h1_count += 1

    def handle_data(self, data):
        if self.active_script is not None:
            self.active_script += data
        if self.in_title:
            self.title += data

    def handle_endtag(self, tag):
        if tag == "script" and self.active_script is not None:
            self.scripts.append(self.active_script)
            self.active_script = None
        if tag == "title":
            self.in_title = False


for name in PUBLIC:
    text = (ROOT / name).read_text(encoding="utf-8")
    page = PageParser()
    page.feed(text)
    assert not re.search(r"coming\s*soon|new\s+Audio\s*\(|<audio", text, re.I)
    assert "zeus-splash" not in page.ids, "Opening splash must not be displayed"
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            continue
        if not url.path:
            assert unquote(url.fragment) in page.ids, f"{name}: broken anchor {link}"
            continue
        target = (ROOT / unquote(url.path)).resolve()
        assert target.is_relative_to(ROOT), f"{name}: path escapes root: {link}"
        assert target.is_file(), f"{name}: missing asset {link}"
        assert "orginal paper" not in target.parts
        assert target.suffix.lower() not in {".mp3", ".wav", ".ogg"}
        if target.suffix == ".js":
            subprocess.run(["node", "--check", str(target)], check=True)
    for script in page.scripts:
        subprocess.run(["node", "--check", "--input-type=commonjs"], input=script, text=True, encoding="utf-8", cwd=ROOT, check=True)
    if name == "index.html":
        expected = "ZEUS: Accelerating Diffusion Models with Only Second-Order Predictor"
        assert page.title == expected
        assert page.h1_count == 1
        assert "https://arxiv.org/pdf/2604.01552" in page.links
        assert not any("ZEUS_ICML2026.pdf" in link or "preset_replay" in link or "frontier_animation" in link for link in page.links)
        fragment = (ROOT / "static/results-tables.html").read_text(encoding="utf-8").strip()
        embedded = text.split("<!-- RESULTS:START -->", 1)[1].split("<!-- RESULTS:END -->", 1)[0].strip()
        assert fragment == embedded, "Run scripts/sync-results.py after changing the fragment"
        source = (ROOT / "orginal paper/main.tex").read_text(encoding="utf-8")
        authors = re.findall(r"\\author\{([^}]+)\}", source)
        visible_authors = text.split('<div class="is-size-5 publication-authors">', 1)[1].split("</div>", 1)[0]
        positions = [visible_authors.index(author) for author in authors]
        assert positions == sorted(positions), "Author order differs from the camera-ready"
        assert len(authors) == 10
    print(f"OK: {name} metadata, references, accessibility labels, and script syntax")

print("Static checks passed. Browser layout and interaction checks require local visual review.")
