"""Static checks for the Drinking Observatory pages. No network access.

Fails if an HTML page does not parse, a local href/src points at a missing
file, an in-page or cross-page #anchor has no matching id, or a page is
missing its title, lang or viewport.
"""
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.refs, self.meta = set(), [], set()
        self.has_title = self.has_lang = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "html" and a.get("lang"):
            self.has_lang = True
        if tag == "title":
            self.has_title = True
        if tag == "meta" and a.get("name"):
            self.meta.add(a["name"])
        for key in ("href", "src", "action"):
            if a.get(key):
                self.refs.append(a[key])


def main() -> int:
    pages = {p.name: p for p in sorted(ROOT.glob("*.html"))}
    parsed = {}
    errors = []
    for name, path in pages.items():
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        page.close()
        parsed[name] = page
        if not page.has_title:
            errors.append(f"{name}: missing <title>")
        if not page.has_lang:
            errors.append(f"{name}: <html> has no lang")
        if "viewport" not in page.meta:
            errors.append(f"{name}: missing viewport meta")
    checked = 0
    for name, page in parsed.items():
        for ref in page.refs:
            if ref.startswith(("http://", "https://", "mailto:", "tel:", "data:", "//")):
                continue
            checked += 1
            target, _, anchor = ref.partition("#")
            target_page = target or name
            if target and not (ROOT / target).is_file():
                errors.append(f"{name}: missing file {target}")
                continue
            if anchor and target_page in parsed and anchor not in parsed[target_page].ids:
                errors.append(f"{name}: #{anchor} not found in {target_page}")
    for e in errors:
        print("FAIL", e)
    print(f"{len(pages)} pages, {checked} local links checked, {len(errors)} problems")
    return 1 if errors or not pages else 0


if __name__ == "__main__":
    sys.exit(main())
