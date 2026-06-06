# SenderKit MCP Messaging Operations Skill

Portable AI-agent instructions for using the SenderKit MCP connector safely.

This open-source skill lives in the [`senderkit/senderkit-skills`](https://github.com/senderkit/senderkit-skills) GitHub repository under `mcp-messaging-operations/`. It helps Claude, Codex, Cursor-style agents, and other MCP-capable assistants use SenderKit MCP tools for messaging operations without overclaiming unsupported connector behavior.

## What it does

- Confirms whether the SenderKit MCP connection is in test or live mode.
- Sends registered SenderKit templates with variables, metadata, scheduling, idempotency, and email-only options.
- Sends raw one-off email, SMS, push, or web-push content when explicitly requested.
- Lists and inspects templates before using uncertain slugs.
- Lists, filters, and inspects messages for status or delivery debugging.
- Cancels messages only when they are still scheduled or queued.

## Contents

```text
mcp-messaging-operations/
|-- AGENTS.md
|-- README.md
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- llms.txt
`-- references/
    `-- sources.md
```

## Use with coding agents

Reuse from GitHub:

```bash
git clone https://github.com/senderkit/senderkit-skills.git
```

Codex / OpenAI-compatible skill loaders:

```bash
mkdir -p ~/.codex/skills
cp -R senderkit-skills/mcp-messaging-operations ~/.codex/skills/senderkit-mcp-messaging-operations
```

Prompt:

```text
Use $senderkit-mcp-messaging-operations to send a test message and verify its status through SenderKit MCP.
```

Claude / Anthropic-style skills:

Package or install the `mcp-messaging-operations/` folder as a skill. `SKILL.md` is the canonical instruction file, and the skill name declared there is `senderkit-mcp-messaging-operations`.

## MCP scope

This skill is based on the documented SenderKit MCP tools:

- `senderkit_context`
- `senderkit_send`
- `senderkit_send_raw`
- `senderkit_templates_list`
- `senderkit_templates_get`
- `senderkit_messages_list`
- `senderkit_messages_get`
- `senderkit_cancel_message`

It does not assume MCP support for template mutation, webhook management, suppressions, contacts, campaigns, analytics, provider setup, or domain configuration.

Suggested skill description:

```text
Safely operate SenderKit through its MCP connector for sends, template lookup, message inspection, and pending-message cancellation.
```
