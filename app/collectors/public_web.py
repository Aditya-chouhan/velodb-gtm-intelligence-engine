from __future__ import annotations

import html
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from typing import Iterable

USER_AGENT = "velodb-commercial-intelligence-os/1.0 (+https://github.com/Aditya-chouhan/velodb-gtm-intelligence-engine)"


def html_to_text(raw_html: str) -> str:
    """Convert HTML to compact plain text without pretending to be a full DOM parser."""
    no_scripts = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", raw_html)
    no_tags = re.sub(r"(?s)<[^>]+>", " ", no_scripts)
    return re.sub(r"\s+", " ", html.unescape(no_tags)).strip()


def extract_keyword_hits(text: str, keywords: Iterable[str]) -> list[str]:
    lowered = text.casefold()
    return sorted({keyword for keyword in keywords if keyword.casefold() in lowered})


def fetch_public_page(url: str, keywords: Iterable[str], timeout: int = 15) -> dict:
    """Fetch a public page and return an auditable receipt.

    A keyword hit means only that the term appeared on the retrieved page. It does not
    prove production usage, pain, purchase intent, or commercial readiness.
    """
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    retrieved_at = datetime.now(timezone.utc).isoformat()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            body = response.read().decode(charset, errors="replace")
            text = html_to_text(body)
            return {
                "url": url,
                "retrieved_at": retrieved_at,
                "status": getattr(response, "status", 200),
                "keyword_hits": extract_keyword_hits(text, keywords),
                "text_chars": len(text),
                "error": None,
            }
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as exc:
        return {
            "url": url,
            "retrieved_at": retrieved_at,
            "status": None,
            "keyword_hits": [],
            "text_chars": 0,
            "error": f"{type(exc).__name__}: {exc}",
        }
