from __future__ import annotations

import json
import re
from pathlib import Path


SITE = Path(__file__).resolve().parents[1]
BASE_URL = "https://xn--jk1bu21awrcryv.com"


def main() -> None:
    path = SITE / "index.html"
    html = path.read_text(encoding="utf-8")
    pattern = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)

    def update(match: re.Match[str]) -> str:
        data = json.loads(match.group(1))
        graph = data.get("@graph", []) if isinstance(data, dict) else []
        for node in graph:
            if not isinstance(node, dict):
                continue
            if node.get("@id") != f"{BASE_URL}/#main-links":
                continue
            node["itemListElement"] = [
                {"@type": "ListItem", "position": 1, "name": "홈", "url": f"{BASE_URL}/"},
                {"@type": "ListItem", "position": 2, "name": "학습가이드", "url": f"{BASE_URL}/학습가이드/"},
                {"@type": "ListItem", "position": 3, "name": "상담문의", "url": f"{BASE_URL}/상담문의/"},
                {"@type": "ListItem", "position": 4, "name": "과목별학원", "url": f"{BASE_URL}/과목별학원/"},
                {"@type": "ListItem", "position": 5, "name": "전국학원", "url": f"{BASE_URL}/전국학원/"},
            ]
        return '<script type="application/ld+json">' + json.dumps(
            data, ensure_ascii=False, separators=(",", ":")
        ) + "</script>"

    updated, count = pattern.subn(update, html)
    if count == 0:
        raise RuntimeError("root JSON-LD script not found")
    path.write_text(updated, encoding="utf-8")
    print("updated root subject schema")


if __name__ == "__main__":
    main()
