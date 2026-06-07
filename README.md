# SenderKit Skills

Portable AI-agent skills for SenderKit. This repository is packaged as a plugin for Claude Code, OpenAI Codex, Cursor, and other Agent Skills-compatible coding assistants.

This repository contains one `senderkit` plugin with two related skills:

- `senderkit-integration` - add or migrate SenderKit transactional messaging in an application codebase.
- `senderkit-mcp-messaging-operations` - operate SenderKit through the SenderKit MCP connector.

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
|   `-- plugin.json
|-- .cursor-plugin/
|   `-- plugin.json
|-- AGENTS.md
|-- LICENSE
|-- README.md
`-- skills/
    |-- senderkit-integration/
    `-- senderkit-mcp-messaging-operations/
```

## Official docs

- SenderKit MCP overview: `https://docs.senderkit.com/mcp/overview`
- SenderKit MCP tools: `https://docs.senderkit.com/mcp/tools`
- SenderKit OpenAPI: `https://www.senderkit.com/public/openapi.yaml`
