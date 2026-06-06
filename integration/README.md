# SenderKit Integration Skill

Portable AI-agent instructions for adding or migrating SenderKit transactional messaging in real applications.

This skill helps coding assistants integrate SenderKit into new projects and existing codebases that already use providers such as Resend, SendGrid, Postmark, Mailgun, SES, SMTP, Twilio, FCM, APNs, or Expo. It is designed to work with Codex, Claude, Cursor-style agents, and generic LLM coding assistants that can read local files.

## What it does

- Detects the project language, framework, package manager, and existing notification provider.
- Fetches the current SenderKit OpenAPI spec from `https://www.senderkit.com/public/openapi.yaml`.
- Chooses an official SDK when available, or falls back to REST for any language.
- Preserves existing send semantics while migrating templates, variables, metadata, scheduling, attachments, and delivery status handling.
- Encourages safe rollout with test-mode sends, render checks, idempotency, and message reconciliation.

## Contents

```text
senderkit-integration/
|-- README.md
|-- SKILL.md
|-- AGENTS.md
|-- llms.txt
|-- agents/openai.yaml
|-- references/
|   |-- api-reference.md
|   |-- language-detection.md
|   |-- migration-playbook.md
|   |-- sources.md
|   `-- verification.md
`-- scripts/
    `-- fetch_openapi.py
```

## Use with coding agents

Codex / OpenAI-compatible skill loaders:

```bash
mkdir -p ~/.codex/skills
cp -R senderkit-integration ~/.codex/skills/
```

Prompt:

```text
Use $senderkit-integration to add SenderKit transactional messaging to this project.
```

Claude / Anthropic-style skills:

Package or install the `senderkit-integration` folder as a skill. `SKILL.md` is the canonical instruction file.

Cursor, Windsurf, Aider, Continue, and generic coding agents:

Add the folder to your repository or agent context and ask the assistant to read `AGENTS.md` or `SKILL.md` before making changes.

Generic LLMs:

Attach or paste `SKILL.md` first. Add only the relevant reference files for the user's stack or task.

## Keep the API current

The skill does not bundle a frozen SenderKit API schema. It fetches the official OpenAPI spec:

```bash
python3 scripts/fetch_openapi.py
```

To compare a local app repo copy:

```bash
python3 scripts/fetch_openapi.py --compare public/openapi.yaml
```

Use this in CI or a scheduled check if the skill is published separately from the SenderKit app.

## Publishing

Before publishing:

- Choose an open-source license. MIT is simple and permissive; Apache-2.0 adds an explicit patent grant.
- Keep `SKILL.md`, `AGENTS.md`, `llms.txt`, `references/`, and `scripts/` in the repo.
- Run the skill validator and OpenAPI fetch helper.

Suggested skill description:

```text
Add or migrate SenderKit transactional messaging in new or existing codebases across languages and frameworks.
```
