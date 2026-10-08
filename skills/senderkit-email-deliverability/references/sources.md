# Source notes

This skill was built from:

- SenderKit open-source skills repository: `https://github.com/senderkit/senderkit-skills`
  - Reusable email-deliverability skill folder: `skills/senderkit-email-deliverability/`
  - License: MIT.
- SenderKit docs: `https://docs.senderkit.com`
  - Sending-domain registration issues the DKIM selector/key and a domain-verification token; obtain exact values from the dashboard/docs.
- Email authentication standards (the RFCs below define these mechanisms):
  - SPF: RFC 7208 (including the 10-DNS-lookup limit).
  - DKIM: RFC 6376.
  - DMARC: RFC 7489 (policies, alignment, aggregate reporting).
  - BIMI: requires DMARC enforcement (quarantine/reject).
- Standard local tooling: read-only `dig` lookups of public DNS records; no third-party API required.
- Optional public checkers the user can run themselves: mail-tester.com, Google Postmaster Tools, MXToolbox.

If the record values the user copies from the SenderKit dashboard differ from examples here, use the dashboard values for the records and tell the user.
