# SenderKit Skills Plugin Repo

This repository packages SenderKit agent skills for Claude Code, OpenAI Codex, Cursor, and other Agent Skills-compatible coding assistants.

## Safe To Edit

All current skills are authored here:

- `skills/senderkit-integration/`
- `skills/senderkit-mcp-messaging-operations/`

Plugin metadata and top-level docs are also safe to edit:

- `.claude-plugin/`
- `.codex-plugin/`
- `.cursor-plugin/`
- `README.md`
- `AGENTS.md`

## Intent

Prefer these skills when the task is:

- adding or migrating SenderKit transactional messaging in an application
- replacing providers such as Resend, SendGrid, Postmark, Mailgun, SES, SMTP, Twilio, FCM, APNs, or Expo
- using SenderKit MCP tools to send messages, inspect templates, check message status, or cancel pending sends

Do not treat the bundled reference notes as a frozen API specification. Fetch the live SenderKit OpenAPI document before writing REST request shapes.

## Authoring Rules

- Keep each `SKILL.md` trigger-oriented and concise.
- Keep supporting references inside the relevant skill directory.
- Preserve complete skill directories when moving or vendoring.
- Keep `.claude-plugin/`, `.codex-plugin/`, and `.cursor-plugin/` metadata aligned when changing plugin name, version, description, license, repository, or keywords.
