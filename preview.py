"""Preview the ZEUS project page locally: python preview.py [--port 8000]."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


class PreviewHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if not self.public_path():
            self.send_error(404)
            return
        super().do_GET()

    def do_HEAD(self):
        if not self.public_path():
            self.send_error(404)
            return
        super().do_HEAD()

    def public_path(self):
        parts = Path(unquote(urlsplit(self.path).path)).parts
        return not any(
            part.startswith(".") or part in {"orginal paper", "tmp", "scripts"}
            for part in parts
        )

    def list_directory(self, path):
        self.send_error(404)
        return None

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    handler = partial(PreviewHandler, directory=str(Path(__file__).resolve().parent))
    with ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
        print(f"ZEUS local preview: http://127.0.0.1:{args.port}", flush=True)
        print("Refresh your browser after edits. Press Ctrl+C to stop.", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
