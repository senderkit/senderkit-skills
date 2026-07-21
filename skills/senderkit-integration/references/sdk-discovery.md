# SDK discovery

The set of official SenderKit SDKs changes over time. **Never assume it from a static list** — resolve it at integration time from the live index, then confirm against the package registry. This file is the single place that owns the SDK-vs-REST decision; the other references defer to it.

**Source of truth:** the docs index at `https://docs.senderkit.com/llms.txt`. It lists every documented SDK as a link whose URL contains `/sdks/`. A new SDK appears here automatically once it has a docs page — so discovery keeps working without editing this skill.

## Procedure

1. Detect the language and framework (see `language-detection.md`).

2. List the SDKs the index currently advertises:
   - Run `python3 <skill-dir>/scripts/list_sdks.py` (from the GitHub checkout: `python3 skills/senderkit-integration/scripts/list_sdks.py`), **or**
   - Fetch `https://docs.senderkit.com/llms.txt` and take every link whose URL contains `/sdks/`.

3. Match the detected stack to an entry (e.g. `python` → `/sdks/python`, Laravel → `/sdks/laravel`). Open that page as markdown — `https://docs.senderkit.com/sdks/<name>.md` — for the exact package, registry, install command, and usage. Install it.

4. **Index miss → registry backstop.** If the index lists no SDK for the detected language, an SDK may still exist that shipped ahead of its docs page. Check the language's package registry for an *official* SenderKit package before falling back to REST:

   | Language | Registry lookup | Official marker |
   | --- | --- | --- |
   | JS / TS | npm `@senderkit/*` | published by the SenderKit org |
   | PHP | Packagist `senderkit/*` | vendor `senderkit`, repo `github.com/senderkit/*` |
   | Python | PyPI `senderkit` | author SenderKit, source `github.com/senderkit/*` |
   | Ruby | RubyGems `senderkit` | owner SenderKit |
   | Go | `github.com/senderkit/*` | org `senderkit` |

   Treat a package as official **only** when it is published under the SenderKit org/account (repo under `github.com/senderkit/…`). If ownership is unclear, do not install it — use REST.

5. **No official SDK anywhere** — or you are deliberately avoiding a dependency (e.g. an edge runtime) — use the REST API (`examples.md`). Note in the implementation summary that no SDK was used and why.

Do not drop to REST just because a live lookup was unavailable. If you cannot reach the index or the registry, install the SDK named in the cache below and note the version was not live-checked. Reserve REST for "no SDK exists," "avoiding a dependency," or a lookup that actively shows the package was renamed or yanked.

## Known SDKs at authoring

A cache to orient from — **not** the source of truth. Confirm the current package/version from the index or registry before installing; the list grows.

| Language / framework | Package (registry) | Entry point | Docs |
| --- | --- | --- | --- |
| JavaScript / TypeScript | `@senderkit/sdk` (npm) | `import { SenderKit } from "@senderkit/sdk"` | `/sdks/typescript` |
| PHP · core | `senderkit/senderkit-php` (Packagist) | `SenderKit\Client` | `/sdks/php` |
| PHP · Laravel | `senderkit/senderkit-laravel` (Packagist) | mail transport + notification channel | `/sdks/laravel` |
| PHP · Symfony | `senderkit/senderkit-symfony` (Packagist) | bundle + webhook verifier | `/sdks/symfony` |
| Python | `senderkit` (PyPI) | `from senderkit import SenderKit` (also `AsyncSenderKit`); extras `[django]`, `[fastapi]`, `[flask]`, `[celery]` | docs page pending — found via PyPI, not the index |

Python is the live proof of step 4: it is published on PyPI but not yet listed in the docs index, so index-only discovery would miss it. The registry backstop catches it — and once its docs page ships, `list_sdks.py` will surface it automatically.
