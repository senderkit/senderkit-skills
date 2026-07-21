#!/usr/bin/env python3
"""List SenderKit's official SDKs from the published docs index (llms.txt).

The docs index is the source of truth for which languages/frameworks have an
official SDK. It is machine-generated, so a new SDK shows up here as soon as it
has a docs page — no edit to the skill required.

Caveat: an SDK can ship to a package registry (npm / PyPI / Packagist) before its
docs page exists, so an empty match for a language is not proof there is no SDK.
See references/sdk-discovery.md step 4 for the registry backstop.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request


DEFAULT_URL = "https://docs.senderkit.com/llms.txt"
# Markdown links whose target is a docs page under /sdks/.
SDK_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)]*/sdks/[^)]+)\)")


def read_url(url: str, timeout: float) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "senderkit-skill-sdk-index"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", "replace")


def main() -> int:
    parser = argparse.ArgumentParser(description="List SenderKit SDKs from the docs index.")
    parser.add_argument("--url", default=DEFAULT_URL, help=f"Docs index URL. Default: {DEFAULT_URL}")
    parser.add_argument("--timeout", type=float, default=15.0, help="HTTP timeout in seconds")
    args = parser.parse_args()

    try:
        text = read_url(args.url, args.timeout)
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"ERROR: failed to fetch {args.url}: {exc}", file=sys.stderr)
        return 2

    # Dedupe on the browsable page URL (strip a trailing .md), keeping the first label.
    seen: dict[str, str] = {}
    for label, url in SDK_LINK.findall(text):
        page = url[:-3] if url.endswith(".md") else url
        seen.setdefault(page, label.strip())

    if not seen:
        print(f"No SDK entries found at {args.url}", file=sys.stderr)
        print("The index may have moved; confirm the URL and the /sdks/ path.", file=sys.stderr)
        return 1

    print(f"source: {args.url}")
    print(f"count: {len(seen)}")
    for page, label in sorted(seen.items()):
        print(f"{label}\t{page}")
    print(
        "\nNote: reflects SDKs with a docs page. An SDK can reach a package registry "
        "before its docs page exists — see references/sdk-discovery.md step 4 for the "
        "registry backstop.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
