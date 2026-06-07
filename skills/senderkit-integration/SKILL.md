---
name: senderkit-integration
description: Add or migrate SenderKit transactional messaging in new or existing codebases across languages and frameworks. Use when a user asks to integrate SenderKit, replace or migrate from an existing email or notification provider, wire template sends, raw sends, API keys, idempotency, delivery status checks, webhooks, or use docs.senderkit.com / SenderKit OpenAPI guidance in an application.
---

# SenderKit integration

Use this open-source skill to add SenderKit to an application with minimal disruption. The reusable source lives at `https://github.com/senderkit/senderkit-skills` in the `skills/senderkit-integration/` directory, while the skill name remains `senderkit-integration`. Favor codebase-aware integration over generic snippets: detect the stack, find existing notification flows, preserve behavior, and add SenderKit behind a small local wrapper.

## Workflow

1. Discover the project shape.
   - Identify the language, framework, package manager, runtime, and existing mail/SMS/push provider.
   - Search for send call sites, templates, webhook handlers, provider SDKs, SMTP config, environment variables, retry logic, and tests.
   - Read `references/language-detection.md` when the stack or provider is not obvious.

2. Load the current API contract.
   - Fetch `https://www.senderkit.com/public/openapi.yaml` before writing API request shapes.
   - If working inside the SenderKit repo, compare it with `public/openapi.yaml` by running `python3 references/../scripts/fetch_openapi.py --compare public/openapi.yaml`.
   - If network access is unavailable, use the repo's `public/openapi.yaml` when present and clearly note that the live contract was not checked.

3. Choose the integration path.
   - Use an official SenderKit SDK when the current docs or package manifests confirm one for the stack.
   - For JavaScript/TypeScript, verify the current package name before installing. Local SenderKit docs may show `@senderkit/sdk`; public examples may show `@senderkit/node`.
   - For any other language, or when SDK availability is uncertain, use the REST API directly.
   - Keep the old provider until parity is verified; do not remove working delivery code as the first step.

4. Implement a local SenderKit boundary.
   - Store `SENDERKIT_API_KEY` in environment/config only. Never hardcode keys.
   - Add one small module/service such as `senderkitClient`, `notifications`, or `mailProvider` instead of scattering HTTP calls.
   - Use template sends for long-lived product messaging. Use raw sends only for bootstrapping, migration staging, or genuinely dynamic content.
   - Add `Idempotency-Key` for every send that can be retried. Prefer stable keys like `<event>/<entity-id>/<recipient-id>`.
   - Attach safe metadata for traceability, such as internal user IDs, order IDs, or flow names. Avoid raw PII and message bodies in metadata.

5. Migrate existing behavior carefully.
   - Read `references/migration-playbook.md` before replacing Resend, SendGrid, Postmark, Mailgun, SES, SMTP, Twilio, APNs, FCM, Expo, or another provider.
   - Preserve recipient selection, unsubscribe/suppression checks, attachments, reply-to/cc/bcc, scheduling, locale, and audit logging.
   - Move content into SenderKit templates when possible, and pass only variables from code.

6. Verify before live traffic.
   - Read `references/api-reference.md` for current OpenAPI usage and request-shape lookup.
   - Read `references/verification.md` before finalizing.
   - Confirm the API key context, render templates with representative variables, send through test mode first, and inspect message status.

## SenderKit basics

- Open-source skill repository: `https://github.com/senderkit/senderkit-skills`
- Reusable skill folder in that repository: `skills/senderkit-integration/`
- Official OpenAPI: `https://www.senderkit.com/public/openapi.yaml`
- Treat the OpenAPI file as source of truth for endpoints, schemas, request examples, and error responses.
- Use static notes in this skill only as integration guidance, not as a replacement for the current spec.

## Folder structure

When reused from GitHub, keep the complete `skills/senderkit-integration/` directory together:

```text
skills/senderkit-integration/
|-- AGENTS.md
|-- README.md
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- llms.txt
|-- references/
|   |-- api-reference.md
|   |-- language-detection.md
|   |-- migration-playbook.md
|   |-- sources.md
|   `-- verification.md
`-- scripts/
    `-- fetch_openapi.py
```

## Reference files

- `references/language-detection.md` - Detect project language, framework, package manager, and existing providers.
- `references/api-reference.md` - How to fetch/read the current OpenAPI contract and apply it safely.
- `references/migration-playbook.md` - Provider migration strategy and mapping from common email/SMS/push systems.
- `references/verification.md` - Test, rollout, and production-safety checklist.
- `references/sources.md` - Source notes used to build this skill.

## Implementation standards

- Prefer server-side sends. Do not expose SenderKit API keys to browsers, mobile apps, or public clients.
- Add timeouts, retry handling for transient errors, and explicit handling for rate-limit responses defined in the current OpenAPI.
- Do not assume an accepted send was delivered. Store the SenderKit message ID where the app needs later reconciliation.
- Do not silently change transactional semantics. If the old code sends one email per recipient, keep that shape unless SenderKit docs and app requirements support batching.
- Do not invent webhook payloads or signature schemes. Use current SenderKit dashboard/docs examples when adding webhooks.
- Update tests around every changed send path. Mock the local SenderKit boundary, not unrelated application code.
