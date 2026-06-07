# SenderKit Skills

**Add transactional email, SMS, push, and web-push notifications to any app — straight from your AI coding agent.** Portable AI-agent skills for [SenderKit](https://www.senderkit.com), packaged as a plugin for Claude Code, OpenAI Codex, Cursor, and other Agent Skills-compatible coding assistants.

SenderKit sends email, SMS, push, and web-push directly, and can also route through providers like Resend, SendGrid, Postmark, Mailgun, SES, Twilio, FCM, APNs, and Expo — so your app isn't locked into one vendor. These skills let an agent wire SenderKit into your codebase and operate it at runtime over MCP.

This repository contains one `senderkit` plugin with two related skills:

- `senderkit-integration` - add SenderKit to an app, or replace/route an existing email, SMS, or push provider through it.
- `senderkit-mcp-messaging-operations` - send and inspect messages at runtime through the SenderKit MCP connector.

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

Rule of thumb: **integration** writes SenderKit into your code; **messaging operations** sends and inspects messages at runtime via MCP.

## Install

This repo ships per-platform metadata — Claude Code (`.claude-plugin/`), OpenAI Codex (`.codex-plugin/`), and Cursor (`.cursor-plugin/`) — and the authored skills under `./skills/`. Pick your agent below; each path ends with a quick check so you know it worked.

### Claude Code

From the marketplace (recommended):

```text
/plugin marketplace add senderkit/senderkit-skills
/plugin install senderkit@senderkit-skills
```

From a local checkout (for development):

```bash
claude --plugin-dir .
```

This loads both skills and the SenderKit MCP server from the repo's `.mcp.json` (OAuth, no key stored). Run `/mcp`, sign in, and pick a workspace and test/live mode.

**Check it works:** run `/mcp` — the `senderkit` server should be connected — or ask *"Use senderkit-integration to add a welcome email."*

### OpenAI Codex

> "ChatGPT" support means **Codex**, OpenAI's coding agent (CLI / IDE extension / app). The ChatGPT chat app does not load skills.

Codex discovers skills from `.agents/skills/` directories. Vendor the skills into your user scope (available in every repo) or a single repo's scope:

```bash
git clone https://github.com/senderkit/senderkit-skills.git
mkdir -p ~/.agents/skills
cp -R senderkit-skills/skills/senderkit-integration ~/.agents/skills/
cp -R senderkit-skills/skills/senderkit-mcp-messaging-operations ~/.agents/skills/
# repo-scoped instead? copy into <your-repo>/.agents/skills/
```

Restart Codex so it picks them up. Connect MCP: set `SENDERKIT_API_KEY` (the `sk_live_`/`sk_test_` prefix selects mode), then either rely on the bundled `.codex-plugin/mcp.json` config or run `senderkit mcp install --client codex`.

**Check it works:** run `/skills` (the SenderKit skills should be listed) or invoke one explicitly with `$senderkit-integration`.

Distributing the full plugin (skills + MCP) to a team? Publish this repo as a Codex marketplace and install via `codex` → `/plugins`. See <https://developers.openai.com/codex/plugins/build>.

### Cursor

For an individual install, load this repo as a local plugin:

```bash
git clone https://github.com/senderkit/senderkit-skills.git
ln -s "$(pwd)/senderkit-skills" ~/.cursor/plugins/local/senderkit
```

Reload Cursor (**Developer: Reload Window**). Skills show up under Settings → Rules & Skills and can be invoked with `/senderkit-integration`. Connect MCP: set `SENDERKIT_API_KEY` (the bundled `.cursor-plugin/plugin.json` expands it into the `Authorization: Bearer ${SENDERKIT_API_KEY}` header), or run `senderkit mcp install --client cursor`; toggle the server under Settings → MCP.

For teams, import this GitHub repo as a Team Marketplace (Dashboard → Settings → Plugins; Teams/Enterprise plans). See <https://cursor.com/docs/plugins>.

**Check it works:** type `/senderkit-integration` in chat, or ask *"Send a test email and check its status via SenderKit MCP."*

### Connect the SenderKit MCP server

Installing the plugin/skills gives you the `senderkit_*` MCP tools. Auth differs per client:

- **Claude Code** — OAuth via the repo's `.mcp.json`. Run `/mcp`, sign in, pick a workspace and test/live mode. **No API key is stored in the repo.**
- **Cursor / Codex** — **API key**. Set `SENDERKIT_API_KEY` (the `sk_live_` / `sk_test_` prefix selects mode) before launching.

Other clients (Windsurf, VS Code, Zed, Claude Desktop) and manual config: see [`skills/senderkit-mcp-messaging-operations/README.md`](skills/senderkit-mcp-messaging-operations/README.md#connecting-the-senderkit-mcp-server) and [`https://docs.senderkit.com/mcp/installation`](https://docs.senderkit.com/mcp/installation). The SenderKit CLI can also write the config for you: `senderkit mcp install --client cursor` (or `codex`, `claude-code`, `vscode`, `zed`, `all`).

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
    |-- senderkit-integration/
    `-- senderkit-mcp-messaging-operations/
```

## Official docs

- SenderKit MCP overview: `https://docs.senderkit.com/mcp/overview`
- SenderKit MCP tools: `https://docs.senderkit.com/mcp/tools`
- SenderKit OpenAPI: `https://www.senderkit.com/openapi.yaml`
