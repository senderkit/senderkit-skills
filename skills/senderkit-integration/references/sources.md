# Source notes

This skill was built from:

- SenderKit open-source skills repository: `https://github.com/senderkit/senderkit-skills`
  - Reusable integration skill folder: `skills/senderkit-integration/`
  - License: MIT.
- SenderKit public site: `https://www.senderkit.com/`
  - Describes SenderKit as a CMS for transactional notifications.
  - Shows template-slug sends with variables.
  - Mentions multi-channel templates, versioning, locales, SDKs, CLI, and webhooks.
- SenderKit OpenAPI contract:
  - Official published URL: `https://www.senderkit.com/openapi.yaml`
  - Local app repo copy: `public/openapi.yaml`
  - Treat the published URL as source of truth and compare the local copy when working in the SenderKit repo.
- SenderKit README from this repo: `README.md`
  - Documents the TypeScript quickstart, `@senderkit/sdk`, `@senderkit/cli`, `@senderkit/react-email`, and OpenAPI source of truth.
- SenderKit SDK index — source of truth for SDK coverage: `https://docs.senderkit.com/llms.txt`
  - Machine-readable docs index; every documented SDK appears as a link under `/sdks/`. `scripts/list_sdks.py` parses it, and `sdk-discovery.md` drives selection from it. Grows over time — prefer it over any static list in this skill. Note `https://docs.senderkit.com/sdks` redirects to the TypeScript page, so it is not a usable index; use `llms.txt`.
  - Verified official SDKs at authoring:
    - TypeScript / JavaScript — `@senderkit/sdk` (npm); docs `/sdks/typescript`.
    - PHP — `senderkit/senderkit-php` (Packagist; `SenderKit\Client`, `SenderKit\Request\TemplateSend`), plus `senderkit/senderkit-laravel` and `senderkit/senderkit-symfony`; docs `/sdks/php`, `/sdks/laravel`, `/sdks/symfony`.
    - Python — `senderkit` (PyPI; `from senderkit import SenderKit`, Python 3.10+, extras `[django]`/`[fastapi]`/`[flask]`/`[celery]`, source `github.com/senderkit/senderkit-sdk-python`). Published but not yet in the docs index — discovered via PyPI; illustrates why `sdk-discovery.md` adds a package-registry backstop.
- Resend docs and skill examples:
  - Multi-language quickstarts and examples are useful as a pattern for broad framework coverage.
  - The public Resend skill highlights idempotency keys, webhook verification, language detection, and common mistakes.
- Postmark webhook docs:
  - Useful webhook reliability pattern: protect webhook endpoints, acknowledge correctly, and account for provider retries.

Prefer the current published OpenAPI and SenderKit docs over this source note when they differ.
