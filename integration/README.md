# SenderKit Integration Skill

Portable AI-agent instructions for adding or migrating SenderKit transactional messaging in real applications.

This open-source skill lives in the [`senderkit/senderkit-skills`](https://github.com/senderkit/senderkit-skills) GitHub repository under `integration/`. It helps coding assistants integrate SenderKit into new projects and existing codebases that already use providers such as Resend, SendGrid, Postmark, Mailgun, SES, SMTP, Twilio, FCM, APNs, or Expo. It is designed to work with Codex, Claude, Cursor-style agents, and generic LLM coding assistants that can read local files.

## What it does

- Detects the project language, framework, package manager, and existing notification provider.
- Fetches the current SenderKit OpenAPI spec from `https://www.senderkit.com/public/openapi.yaml`.
- Chooses an official SDK when available, or falls back to REST for any language.
- Preserves existing send semantics while migrating templates, variables, metadata, scheduling, attachments, and delivery status handling.
- Encourages safe rollout with test-mode sends, render checks, idempotency, and message reconciliation.

## Contents

```text
senderkit-skills/
|-- LICENSE
`-- integration/
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

## Use with coding agents

Reuse from GitHub:

```bash
git clone https://github.com/senderkit/senderkit-skills.git
```

Codex / OpenAI-compatible skill loaders:

```bash
mkdir -p ~/.codex/skills
cp -R senderkit-skills/integration ~/.codex/skills/senderkit-integration
```

Prompt:

```text
Use $senderkit-integration to add SenderKit transactional messaging to this project.
```

Claude / Anthropic-style skills:

Package or install the `integration/` folder as a skill. `SKILL.md` is the canonical instruction file, and the skill name declared there is `senderkit-integration`.

Cursor, Windsurf, Aider, Continue, and generic coding agents:

Add `senderkit-skills/integration/` to your repository or agent context and ask the assistant to read `AGENTS.md` or `SKILL.md` before making changes.

Generic LLMs:

Attach or paste `SKILL.md` first. Add only the relevant reference files for the user's stack or task.

## Keep the API current

The skill does not bundle a frozen SenderKit API schema. It fetches the official OpenAPI spec:

From inside `integration/`:

```bash
python3 scripts/fetch_openapi.py
```

To compare a local app repo copy:

```bash
python3 scripts/fetch_openapi.py --compare public/openapi.yaml
```

From the GitHub repository root:

```bash
python3 integration/scripts/fetch_openapi.py
```

## Reuse and distribution

This repository is open source under the MIT license. Reuse the `integration/` directory as the portable skill package, or vendor that directory into an agent-specific skills folder.

When redistributing or vendoring the skill:

- Keep `SKILL.md`, `AGENTS.md`, `llms.txt`, `agents/openai.yaml`, `references/`, and `scripts/` together.
- Preserve the MIT license from the repository.
- Run the skill validator for your target agent and the OpenAPI fetch helper after changes.

Suggested skill description:

```text
Add or migrate SenderKit transactional messaging in new or existing codebases across languages and frameworks.
```
