---
name: senderkit-mcp-messaging-operations
description: Safely operate SenderKit through its MCP connector. Use when a user asks Claude or another MCP-capable agent to use SenderKit MCP tools for test/live mode checks, templated sends, raw sends, template lookup, message status or delivery debugging, recent message filtering, scheduled send checks, or canceling scheduled or queued messages.
---

# SenderKit MCP messaging operations

Use this skill when SenderKit is connected as an MCP server and the user wants you to operate SenderKit through tool calls. The documented MCP surface is intentionally small: tools only, prefixed with `senderkit_`.

## Source of truth and drift

The connected MCP server's advertised tool list is the runtime source of truth, not this document.

- The tool map below mirrors the published surface at `https://docs.senderkit.com/mcp/tools` (eight tools). Treat that page as canonical when the two disagree, and prefer the live tool list over both.
- If the connected server advertises an additional `senderkit_*` tool that is not listed here, you may use it after reading its tool schema. Do not assume a tool exists because it appears here; if a listed tool is absent at runtime, skip it and tell the user.
- Newer or preview servers may expose template-mutation tools (for example `senderkit_templates_create` or `senderkit_templates_regenerate`) that are not part of the documented public surface. Use them only when the connected server actually advertises them and the user's request authorizes the change.

## Required workflow

1. Check context before acting.
   - Call `senderkit_context` before any send or cancellation.
   - Tell the user whether the active connection is `test` or `live`.
   - In `live` mode, do not send or cancel unless the user's request clearly authorizes that real-world action.

2. Prefer template sends.
   - Use `senderkit_send` when the user names or implies an existing template.
   - If the template slug is uncertain, call `senderkit_templates_list`.
   - Before sending with an unfamiliar slug, call `senderkit_templates_get` to inspect the template's channel, status, and published version.
   - Pass template variables in `vars` as a JSON object.
   - Use `version` only when the user asks to pin a specific template version or the workflow requires a known version.

3. Use raw sends narrowly.
   - Use `senderkit_send_raw` only for explicit one-off inline content.
   - For email raw sends, provide `subject` and `html`; include `text` when practical.
   - For SMS, push, and web-push raw sends, provide the channel-specific required body/title fields.
   - Set `interpolate: true` only when the user wants server-side variable substitution over the inline content.

4. Make sends traceable and retry-safe.
   - Include `idempotencyKey` for retryable sends, scheduled sends, or any send that might be repeated by an agent or job.
   - Use stable keys such as `<flow>/<entity-id>/<recipient-id>`.
   - Include scalar `metadata` values for later filtering, such as flow, internal entity ID, tenant/workspace ID, or reason.
   - Do not put secrets, message bodies, or unnecessary PII in metadata.

5. Inspect messages for status and debugging.
   - Use `senderkit_messages_list` for recent sends, filtered searches, failures, template-specific history, channel-specific history, or metadata lookups.
   - Use `senderkit_messages_get` when the user provides a message ID or when a list result needs full detail.
   - Explain that accepted sends are asynchronous; a returned message ID is not proof of delivery.
   - When reporting failures, include the status, relevant provider response or event timeline if returned, and the next concrete check.

6. Cancel only pending messages.
   - Call `senderkit_context` first.
   - Use `senderkit_messages_get` if the current status is unknown.
   - Use `senderkit_cancel_message` only for messages that are `scheduled` or `queued`.
   - If the status is later than queued, explain that delivery has already started or reached a terminal state and is not reversible through MCP.

## Tool map

- `senderkit_context` - confirm workspace and `test` or `live` mode.
- `senderkit_send` - send a registered template to one recipient.
- `senderkit_send_raw` - send inline email, SMS, push, or web-push content to one recipient.
- `senderkit_templates_list` - discover available templates.
- `senderkit_templates_get` - inspect one template by slug.
- `senderkit_messages_list` - list and filter message history.
- `senderkit_messages_get` - inspect one message by ID.
- `senderkit_cancel_message` - cancel a still-pending scheduled or queued message.

## Boundaries

The documented surface is read-and-send only: it cannot create, edit, render, or publish templates. Do not claim those capabilities unless the connected server actually advertises a matching tool (see "Source of truth and drift"). Do not claim MCP support for webhooks, suppressions, contacts, campaigns, analytics, provider setup, or domain configuration unless the active MCP server exposes tools for those operations.

When a user asks for an unsupported operation, explain the supported MCP alternatives: inspect templates, send templated or raw messages, inspect message history, or cancel pending messages.

## Reference

Read `references/sources.md` when you need the canonical SenderKit MCP documentation links used to build this skill.
