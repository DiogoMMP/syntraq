# README structure — canonical sections

The order below is fixed. Each section is **Always**, **If applicable** or **Optional**. Drop what you cannot document from evidence; never leave a stub.

[`template.md`](template.md) is the fill-in skeleton for all of this. This file explains *why* each section looks the way it does and how it adapts per stack.

---

## 0. Title + badge wall + lead — *Always*

```markdown
# <Product name> — <Component>

<badge wall, see badges.md>

<2–4 line paragraph: what this is, and the transition it represents if it is a migration or rebuild.>

<1–3 line paragraph: what it serves — the concrete domains/surfaces, named.>

---
```

The title is the **product**, not the repo slug — take the human name from the ticket prefix, the solution file, `package.json`'s `description`, or the existing docs, and add the component suffix (`Backend`, `Frontend`, `BFF`, `Mobile app`, `CLI`, `SDK`) that matches what the repo actually is.

The lead never says "this is a README" or "this repository contains". It says what the system *is* and what it *serves*, naming real modules.

## 1. Table of contents — *Always*

A flat bullet list of the `##` headings only — never `###`. Anchors are GitHub slugs: lowercase, spaces to hyphens, punctuation dropped, and `&` collapses to nothing — so a heading `Patterns & conventions` becomes `#patterns--conventions`, with the double hyphen. Verify each one against the headings you kept.

## 2. Tech stack — *Always*

A three-column table: `| Concern | Choice | Notes |`.

- One row per concern, in this rough order: Runtime, Language, Framework, Database, ORM/data access, Migrations, Jobs, Cache/queue, Mapping, Validation, API docs, Auth, Files/docs, Mail/notifications, UI/design system, State/data fetching, Local orchestration, Tests, Code quality.
- **Choice** is bolded and carries the real version, plus where it is pinned.
- **Notes** carries the caveat that stops a mistake — who really owns the schema, which older version still works for local development, what the library is *not* used for. Leave the cell blank only when there is genuinely nothing to warn about; prefer to say something.
- Drop concerns the project does not have. Add ones it does (Design system, Charting, Maps, Payments, Realtime, Feature flags, i18n).

## 3. Architecture — *Always*

1. Two or three lines of prose stating the architectural rule that actually **constrains** the code — the dependency direction, the isolation invariant, what may never leak where. Not "we use Clean Architecture" but what that forbids.
2. A `mermaid` `flowchart TD` of the layers/packages. Node labels carry the name plus an `<i>` line of responsibilities. **Every arrow must be a dependency you verified** in project references, imports or workspace config.
3. A table `| Layer | Responsibility | Path |` — one row per layer, path in backticks, real folder.

Typical node sets: layered backend → Presentation, Application, Domain, Persistence, Infrastructure, Contracts, Tests. Frontend → pages/router, components/forms, data hooks, BFF route handlers, external clients, domain types/schemas. Monorepo → the workspace packages, arrows from the declared dependencies. Library → prefer a module graph over a layer graph.

## 4. Solution layout — *Always*

A plain (untagged) fenced block: an ASCII tree of the top two-to-three levels, each line followed by an aligned inline annotation.

Rules: only paths that exist; the annotation says what lives there **and why it matters**, not a restated folder name; collapse noisy siblings with brace notation (`{A,B,C}`); include the root-level files that matter (build config, container files, the engineering rulebook, the dependency manifest).

## 5. Domain modules — *Always* (rename per stack)

How the code is sliced by feature, and the list of slices. **Name every module.** State the organising principle explicitly — that a module is a vertical slice from inner layer to outer layer, or that each app in the workspace owns its own stack, or whatever is true here.

Add real counts only if you counted them. Add a `>` blockquote for a naming rule the reader would otherwise get wrong — a legacy data key that differs from the code name, a route group that differs from its folder, a package name that differs from its directory.

Rename to fit: *Domain modules* (backend), *Apps & packages* (monorepo), *Routes & features* (frontend), *Public API* (library), *Commands* (CLI).

## 6. Patterns & conventions — *Always*

Opens by naming the normative source, if the repo has one: "`<rulebook>` is the normative rulebook; this is the summary."

Then bolded sub-groups, each a tight bullet list. Grouping that works for a layered backend:

- **Domain** — entity purity, construction vs mutation, value objects, base entity, key and numeric types
- **Boundaries** — cross-system reference rules, repository/service contracts, DTO isolation, pre-flight checks before persisting
- **API surface** — the pagination/sorting contract, response completeness, enum wire format, exports
- **Errors & validation** — the exception hierarchy, the error envelope, where validation runs and where it stays fail-fast
- **Cross-cutting** — logging shape, documentation requirements, how external clients degrade

Grouping that works for a frontend: **Components**, **Data fetching**, **Forms & validation**, **BFF boundary**, **Styling & design system**, **State**, **Errors & loading**, **Accessibility**.

Each bullet is one rule, stated as a rule, with the *why* or the trap in the same breath. This is the section that keeps the codebase consistent, so it must be prescriptive, not descriptive.

## 7. Jobs / background work — *If applicable*

Only if there is a scheduler, worker or queue. Cover: how many jobs and what they do; how they are invoked (direct DI, HTTP, queue message — say which, and why); where runners and schedules live; retry configuration; how a failure becomes visible; the dashboard path and its auth.

## 8. Security — *If applicable*

Auth mechanism and session shape; the authorization model with **real** policy/role/guard names; key material persistence and what it guarantees; ingress concerns (forwarded headers, CORS, HTTPS); and any development-only bypass, with an explicit statement of why it cannot reach production. Link the endpoint-to-role mapping doc if one exists.

## 9. Database & migrations — *If applicable*

Lead with the ownership rule in bold if there is a footgun — name the tool that owns the schema and the command that must never be run. Then migration location and naming, what must be kept in sync by hand, immutability of applied migrations, and any special schema the tooling creates.

## 10. Getting started — *Always*

The most important section. Sub-structure:

### Prerequisites
Table `| Tool | Why | Notes |`, with minimum versions and which ones are optional. Add an install snippet for any tool that is genuinely awkward to obtain (not published on the usual package managers, needs a manual download, needs a specific runtime).

### First-time setup
Numbered `####` steps, each with its own fenced command block. State up front that it is done **once** and which shell the examples assume. Give every step a name that says what it achieves. Where a step is commonly skipped and fails loudly, say so in the heading and explain the failure — the literal error — in prose.

Include the local settings / `.env` file as a **structure-only** example: every key the reader must set, every value a `<PLACEHOLDER>`, plus the line saying the file is git-ignored. Where a variables table is clearer than a file dump, use the table. Never reproduce a value from the real file — see [`secrets.md`](secrets.md).

### Run it
The command, then a table `| Surface | URL |` — app, API docs, dashboards, health endpoints — with the real ports, and a note on which environments expose each.

### Troubleshooting
Table `| Symptom | Cause and fix |`. Only real symptoms: errors you hit, or ones the code and config make inevitable — a reserved port range, a missing database role, the wrong protocol, an absent auth session. Quote the literal error text in the Symptom cell.

### Alternative run modes — *If applicable*
Containerised stack, Aspire/Tilt/dev-container, mock or offline mode — one `###` each, with what it gives you that the native run does not.

## 11. Testing — *Always*

A command block first (whole suite, single module, coverage gate), then a table `| Suite | Path | Expectation |`. State the naming convention for test files and methods. Say what runs automatically on push, if anything.

## 12. Code style & quality gates — *Always*

Name the tooling, link its config, give the one-time install command, then a table of what runs at which stage (`git commit` / commit message / `git push`, or `lint` / `typecheck` / `format`). Follow with a bullet list of the rules the config actually enforces that a contributor would otherwise break — including any rule deliberately **disabled**, with the reason.

## 13. Observability & health — *If applicable*

Logging shape and where logs land; metrics, exporter and port; health endpoints with their exact paths and what each one checks.

## 14. Documentation map — *Always*

Table `| Document | What it covers |`, linking every doc in the repo worth opening: the rulebook, per-area READMEs, guides, feature dossiers, code of conduct. Every path verified.

## 15. Contributing — *Always*

### Branching
Table `| Branch type | Pattern | Created from | Targets |` with the **real** ticket-key pattern taken from existing branch names. Then the bullet rules: what each protected branch accepts, concurrency limits, force-push prohibition, automatic sync PRs. A `>` blockquote link to the authoritative external doc if one exists.

### Workflow
A numbered list: branch → commit convention → local gates → PR → merge strategy.

### CI/CD
Two or three lines on what the pipelines cover, linking the shared config.

## 16. Closing line — *Always*

A single `>` blockquote after a `---`: one sentence of engineering ethos plus the link to `CODE_OF_CONDUCT.md` if it exists.

---

## Per-stack cheat sheet

| Project type | Drop | Add / rename |
| :--- | :--- | :--- |
| **Frontend (Next.js/React)** | Database & migrations, Jobs | *Design system*, *Data fetching & caching*, *BFF layer*, *Routes & features* (for Domain modules) |
| **Library / SDK** | Security, Jobs, Observability; Getting started becomes *Installation* + *Usage* | *Public API*, *Versioning & releases*, *Compatibility matrix* |
| **CLI** | Architecture diagram may become a pipeline diagram | *Commands* (for Domain modules), *Configuration file*, *Exit codes* |
| **Monorepo** | — | *Apps & packages* (for Domain modules), *Task graph / caching*, per-package Getting started |
| **Python service** | — | *Environments & dependency management*, *Typing & lint* |
| **Mobile app** | Database & migrations (unless there is a local DB) | *Build & signing*, *Store release*, *Device permissions* |
| **Data / ETL** | — | *Pipelines & schedules*, *Data contracts*, *Lineage* |
