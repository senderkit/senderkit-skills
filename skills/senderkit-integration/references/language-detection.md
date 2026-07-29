# Language and provider detection

Use this reference when the project stack, framework, or existing notification provider is not obvious.

## Stack detection

Check these files first:

| Ecosystem | Signals |
| --- | --- |
| Node.js / TypeScript | `package.json`, `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `bun.lock`, `tsconfig.json`, `next.config.*`, `vite.config.*` |
| Python | `pyproject.toml`, `requirements.txt`, `Pipfile`, `poetry.lock`, `manage.py`, `app/main.py` |
| Go | `go.mod`, `go.sum`, `cmd/`, `internal/` |
| Ruby | `Gemfile`, `Gemfile.lock`, `config/routes.rb` |
| PHP | `composer.json`, `artisan`, `symfony.lock` |
| Java / Kotlin | `pom.xml`, `build.gradle`, `build.gradle.kts`, `src/main/java`, `src/main/kotlin` |
| .NET | `*.csproj`, `*.sln`, `Program.cs`, `appsettings*.json` |
| Rust | `Cargo.toml`, `Cargo.lock`, `src/main.rs` |

Search for existing sends with terms like:

```text
sendEmail|send_email|mailer|mail|smtp|nodemailer|resend|sendgrid|postmark|mailgun|ses|twilio|sns|apns|fcm|expo|webpush|notification|template|webhook
```

## Existing provider signals

- Resend: `resend`, `RESEND_API_KEY`, `emails.send`, React Email examples.
- SendGrid: `@sendgrid/mail`, `SENDGRID_API_KEY`, `custom_args`, `dynamic_template_data`.
- Postmark: `postmark`, `POSTMARK_SERVER_TOKEN`, `Metadata`, message streams.
- Mailgun: `mailgun.js`, `MAILGUN_API_KEY`, `v:` custom variables, domain config.
- AWS SES/SNS: `@aws-sdk/client-sesv2`, `boto3`, `SendEmailCommand`, `EmailTags`, `MessageAttributes`.
- SMTP/Nodemailer: `SMTP_URL`, `nodemailer.createTransport`, host/port/user/pass config.
- Twilio/SNS SMS: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `PublishCommand`.
- Push: APNs, FCM/Firebase Admin, Expo push tokens, web push subscriptions.

## Integration path by ecosystem

Which SDK (or REST) to use is owned by `sdk-discovery.md` — read it once the stack is known; it resolves the package from the live index, falls back to a package-registry check, then REST. Do **not** hardcode package choices here. The notes below are about *where the send belongs* in each ecosystem, not which package to install.

### Node.js / TypeScript

- If the app is Next.js, Remix, Nuxt, SvelteKit, Astro, Express, Hono, or another server-capable framework, send only from server routes/actions/jobs.
- Add a local wrapper that accepts app-domain inputs and calls SenderKit. Keep framework handlers thin.
- On edge runtimes, or when deliberately avoiding a dependency, use the `fetch` REST form instead of the SDK.

### Python

- Place the client in an infrastructure/service module and inject settings from environment.
- Django, FastAPI, Flask, and Celery each have a first-class integration in the Python SDK (`sdk-discovery.md` has the package and its extras) — prefer it over a hand-rolled client.
- Use short request timeouts and preserve background-job retry behavior.

### PHP

- A framework-agnostic core plus Laravel and Symfony integrations exist; `sdk-discovery.md` resolves the exact package. Framework signals: Laravel → `artisan`, `laravel/framework`; Symfony → `symfony.lock`.
- Prefer the framework integration when present, so sends flow through the app's normal Mail/Notification plumbing instead of a hand-rolled HTTP call.
- Keep `SENDERKIT_API_KEY` in the framework's config/secret system, not source code.

### Go

- Keep the client behind an interface so tests can fake it. If `sdk-discovery.md` resolves no SDK, use `net/http` with `context.Context`, explicit timeout, typed request/response structs, and stable idempotency keys.

### Ruby / Java / .NET / Rust / other

- Follow `sdk-discovery.md`; if it yields no official SDK, use the REST API with the platform's normal HTTP client, config, logging, and test patterns.
- Keep credentials in the framework's secret/config system, not source code.

## What to produce

For a normal integration, produce:

- Environment/config additions for `SENDERKIT_API_KEY`.
- A local SenderKit client or provider module.
- One migrated send flow with tests, then apply the same pattern to remaining flows.
- A render or test-send verification path.
- Notes for any old-provider behavior intentionally left in place during rollout.
