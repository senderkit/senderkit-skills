# SenderKit Skills

**Add transactional email, SMS, push, and web-push notifications to any app — straight from your AI coding agent.** Portable AI-agent skills for [SenderKit](https://www.senderkit.com), packaged as a plugin for Claude Code, OpenAI Codex, Cursor, and other Agent Skills-compatible coding assistants.

SenderKit sends email, SMS, push, and web-push directly, and can also route through providers like Resend, SendGrid, Postmark, Mailgun, SES, Twilio, FCM, APNs, and Expo — so your app isn't locked into one vendor. These skills let an agent wire SenderKit into your codebase and operate it at runtime over MCP.

This repository contains one `senderkit` plugin with three related skills:

- `senderkit-integration` - add SenderKit to an app, or replace/route an existing email, SMS, or push provider through it.
- `senderkit-mcp-messaging-operations` - send and inspect messages at runtime through the SenderKit MCP connector.
- `senderkit-email-deliverability` - authenticate a sending domain (SPF/DKIM/DMARC) so email reaches the inbox.

## What can I ask?

You don't need to name SenderKit — these skills activate on everyday messaging requests. Examples:

| You ask | Skill that helps |
| --- | --- |
| "Add a welcome email when a user signs up" | `senderkit-integration` |
| "Set up SMS OTP / verification codes" | `senderkit-integration` |
| "Add push notifications to this project" | `senderkit-integration` |
| "Send password-reset and receipt emails" | `senderkit-integration` |
| "Switch my email provider to SenderKit (or route through it, no lock-in)" | `senderkit-integration` |
| "Send a test email and check its delivery status" | `senderkit-mcp-messaging-operations` |
| "Why did this message fail? Cancel that scheduled send" | `senderkit-mcp-messaging-operations` |
| "Why are my emails going to spam? Set up DKIM/SPF/DMARC" | `senderkit-email-deliverability` |

Rule of thumb: **integration** writes SenderKit into your code; **messaging operations** sends and inspects messages at runtime via MCP.

## Plugins

This repo includes metadata for multiple platforms:

- Claude Code: `.claude-plugin/`
- OpenAI Codex: `.codex-plugin/`
- Cursor: `.cursor-plugin/`

For Claude Code marketplace installation from GitHub:

```text
/plugin marketplace add senderkit/senderkit-skills
/plugin install senderkit@senderkit-skills
```

For local Claude Code development:

```bash
claude --plugin-dir .
```

For Codex or Cursor, install this repository using the platform's plugin flow. The authored skills live under `./skills/`.

### Connect the SenderKit MCP server

Installing the plugin auto-configures the SenderKit MCP server so the `senderkit_*` tools work right away. The auth path depends on the client:

- **Claude Code** — uses this repo's `.mcp.json`. Run `/mcp`, sign in, and pick a workspace and test/live mode. **OAuth by default; no API key is stored in the repo.**
- **Cursor / Codex** — bundled with an **API key**. Set `SENDERKIT_API_KEY` in your environment (the `sk_live_` / `sk_test_` prefix selects mode) before launching.

Details and other clients (Windsurf, VS Code, Zed, Claude Desktop): see [`skills/senderkit-mcp-messaging-operations/README.md`](skills/senderkit-mcp-messaging-operations/README.md#connecting-the-senderkit-mcp-server) and [`https://docs.senderkit.com/mcp/installation`](https://docs.senderkit.com/mcp/installation). The SenderKit CLI can also write the config for you: `senderkit mcp install --client cursor` (or `codex`, `claude-code`, `vscode`, `zed`, `all`).

## Skills

### SenderKit Integration

Use `senderkit-integration` when an agent needs to modify an application: detect the stack, add SenderKit, migrate provider calls, preserve existing notification behavior, and verify the integration before live traffic.

Suggested prompt:

```text
Use $senderkit-integration to add SenderKit transactional messaging to this project.
```

Claude Code plugin command:

```text
/senderkit:senderkit-integration
```

### SenderKit MCP Messaging Operations

Use `senderkit-mcp-messaging-operations` when an agent has access to the SenderKit MCP server and needs to send messages, inspect templates, check message status, or cancel pending sends through MCP tool calls.

Suggested prompt:

```text
Use $senderkit-mcp-messaging-operations to send a test message and verify its status through SenderKit MCP.
```

Claude Code plugin command:

```text
/senderkit:senderkit-mcp-messaging-operations
```

### SenderKit Email Deliverability

Use `senderkit-email-deliverability` when transactional email needs to be authenticated to reach the inbox: diagnose current SPF/DKIM/DMARC with `dig`, generate the exact records to add, point to the SenderKit dashboard for issued values, and verify publication.

Suggested prompt:

```text
Use $senderkit-email-deliverability to diagnose and fix SPF, DKIM, and DMARC for my sending domain.
```

Claude Code plugin command:

```text
/senderkit:senderkit-email-deliverability
```

## Repository layout

```text
senderkit-skills/
|-- .claude-plugin/
|   |-- marketplace.json
|   `-- plugin.json
|-- .codex-plugin/
|   |-- mcp.json
|   `-- plugin.json
|-- .cursor-plugin/
|   |-- marketplace.json
|   `-- plugin.json
|-- .mcp.json
|-- AGENTS.md
|-- LICENSE
|-- README.md
|-- llms.txt
`-- skills/
    |-- senderkit-email-deliverability/
    |-- senderkit-integration/
    `-- senderkit-mcp-messaging-operations/
```

## Official docs

- SenderKit MCP overview: `https://docs.senderkit.com/mcp/overview`
- SenderKit MCP tools: `https://docs.senderkit.com/mcp/tools`
- SenderKit OpenAPI: `https://www.senderkit.com/openapi.yaml`
