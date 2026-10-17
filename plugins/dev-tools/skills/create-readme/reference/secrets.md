# Secret-safe writing

A README documents *how to configure* the system. It must never carry a credential, and it must never carry a string that a scanner reads as one. Those are two separate failures:

- **A real secret in the README** is an incident — it is public, indexed and in the git history for good.
- **A fake secret that trips the scanner** blocks every commit in the repo until someone either rewrites the line or adds an allowlist entry, and allowlists erode the scanner for everyone.

Assume the repo runs **gitleaks** (in pre-commit, in CI, or both) and write so that it never fires.

---

## Never in a README

Not real, not example, not "obviously fake", not commented out:

- A connection string carrying credentials — a `Host=…;Username=…;Password=…` keyword string, or any URI of the form `scheme://` + user + `:` + password + `@host` (`postgresql`, `mongodb+srv`, `amqp`, `redis`, `jdbc` with `?password=`)
- Any password, passphrase, PIN or seed phrase, including a real local-dev one
- API keys, client secrets, bearer/JWT tokens, personal access tokens, webhook signing secrets
- Private keys and certificate bodies (`-----BEGIN … PRIVATE KEY-----`), `.pfx`/`.pem` contents, cert passwords or thumbprints
- Cloud credentials: access-key ids and secret keys, SAS tokens, service-account JSON
- Real tenant/subscription/account identifiers, and internal IdP metadata URLs
- Session cookies, CSRF tokens, or anything copied out of a browser or a debugger
- The contents of `.env`, `appsettings.Development.json`, `secrets.json`, `*.local.*` — read them for the **shape**, never reproduce their values

If a real secret is already in the repo's tracked files or in the existing README, do **not** copy it forward, and tell the user in your proposal that it is there and needs rotating. That is a finding, not a detail.

---

## How to redact so the scanner stays quiet

The rule: **placeholders must be structurally obvious and low-entropy.** Scanners fire on a `password`/`secret`/`token`/`key` assignment whose value looks random. An ALL-CAPS angle-bracket slot never looks random.

This table is written in the safe direction only — the left column names the shape to avoid, without instantiating it, because a reference file must pass the same scan the README does.

| Instead of | Write |
| :--- | :--- |
| `Password=` followed by a real password | `Password=<POSTGRES_PASSWORD>` |
| A URI with `user:password@host` embedded | `postgresql://<user>:<password>@localhost:5432/<database>` |
| An `"ApiKey"` whose value is a real vendor key (`sk_live_…`, `ghp_…`, `xoxb-…`) | `"ApiKey": "<STRIPE_API_KEY>"` |
| `Authorization: Bearer` followed by a real JWT (`eyJ…`) | `Authorization: Bearer <token>` |
| `ClientSecret=` followed by a real secret | `ClientSecret=<CLIENT_SECRET>` |
| A shell line assigning a real password to a `*_PASSWORD` variable | `$env:PGPASSWORD = '<your postgres password>'` |
| A pasted `.env` | A pointer to `.env.example` plus the table of variables |

Three techniques, in order of preference:

1. **Environment-variable indirection.** Show the variable, never the value. This is the only form that is both safe and correct — it is what the reader should actually do.

   ```bash
   export DATABASE_PASSWORD=<your password>     # or set it in your shell profile / secret manager
   ```

2. **A variables table instead of a file dump.** Often clearer than the file:

   | Variable | Required | What it is |
   | :--- | :--- | :--- |
   | `DATABASE_URL` | yes | Connection string; see `.env.example` for the shape |
   | `AUTH_CLIENT_SECRET` | yes | Issued by the identity team — never commit it |

3. **A shape-only snippet.** When the reader genuinely needs to see the file's structure, reproduce the keys and redact every value. Keep the fence tagged, keep the JSON/YAML valid, and add the one-line warning:

   ```json
   {
     "ConnectionStrings": {
       "Default": "Host=localhost;Port=5432;Database=<database>;Username=<user>;Password=<password>"
     },
     "Auth": {
       "ClientId": "<client-id>",
       "ClientSecret": "<client-secret>"
     }
   }
   ```

   > This file is git-ignored. Never commit it, and never paste real values into the README or a ticket.

---

## Also worth avoiding

Not gitleaks findings, but a public README is the wrong place for them:

- Internal hostnames, private IP ranges, VPN endpoints, database server names, jump-host addresses
- Direct links to internal admin consoles, log dashboards or CI runners — name the tool instead
- Employee names, emails and phone numbers — name the *team* or the ticket queue
- Production URLs when the repo is public or may become public

`localhost`, `127.0.0.1` and loopback ports are fine — they are the point of the getting-started section.

---

## Verify before proposing

Scan your own draft. Grep it for the obvious shapes:

```bash
grep -nEi 'password[[:space:]]*[=:]|pwd=|secret[[:space:]]*[=:]|api[_-]?key|token[[:space:]]*[=:]|BEGIN [A-Z ]*PRIVATE KEY|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{10,}|://[^/[:space:]]+:[^@/[:space:]]+@' <draft>
```

Every hit must resolve to a `<PLACEHOLDER>`, an environment-variable name, or a table row — never a value.

If the repo actually runs gitleaks, run it against the draft rather than trusting the grep:

```bash
pre-commit run gitleaks --files <draft>
```

```bash
gitleaks detect --no-git --source <draft>
```

If it fires, **rewrite the line.** Adding a `gitleaks:allow` comment or an entry to `.gitleaksignore` is not the fix here — a README never needs one, and the allowlist you add outlives the line you added it for. Say so if the user asks for the allowlist instead.
