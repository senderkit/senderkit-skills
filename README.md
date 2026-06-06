# SenderKit Skills

Portable AI-agent skills for SenderKit.

This repository contains two related but distinct skills:

- `integration/` - add or migrate SenderKit transactional messaging in an application codebase.
- `mcp-messaging-operations/` - operate SenderKit through the SenderKit MCP connector.

## Skills

### SenderKit Integration

Use `senderkit-integration` when an agent needs to modify an application: detect the stack, add SenderKit, migrate provider calls, preserve existing notification behavior, and verify the integration before live traffic.

Suggested prompt:

```text
Use $senderkit-integration to add SenderKit transactional messaging to this project.
```

### SenderKit MCP Messaging Operations

Use `senderkit-mcp-messaging-operations` when an agent has access to the SenderKit MCP server and needs to send messages, inspect templates, check message status, or cancel pending sends through MCP tool calls.

Suggested prompt:

```text
Use $senderkit-mcp-messaging-operations to send a test message and verify its status through SenderKit MCP.
```

## Repository layout

```text
senderkit-skills/
|-- LICENSE
|-- README.md
|-- integration/
`-- mcp-messaging-operations/
```

## Official docs

- SenderKit MCP overview: `https://docs.senderkit.com/mcp/overview`
- SenderKit MCP tools: `https://docs.senderkit.com/mcp/tools`
- SenderKit OpenAPI: `https://www.senderkit.com/public/openapi.yaml`
