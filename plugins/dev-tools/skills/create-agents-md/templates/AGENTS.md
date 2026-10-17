# AGENTS.md

Guidance for AI coding agents (Claude Code, Codex, Cursor, Copilot, …) working in this repository. Humans: see `README.md`.

<!-- Every line below must pass one test: without it, an agent would get something wrong in this repo. Delete any section the project has no answer for. -->

## Project

<2–3 sentences: what it is, the stack, how it's split (monorepo? backend/frontend?).> <Language of the UI, domain terms and code; domain names that are not translations to fix.>

## Commands

### <subproject or "Root">

- `<install>` — install dependencies
- `<build>` — build
- `<test>` — run the tests
- `<one test>` — run a single test file
- `<lint>` / `<format>` — lint / format
- `<run>` — run locally (ports, proxies, what it expects to be running)

<Constraints the tooling imposes: where tests must live to be picked up, required env, services that must be up.>

### CI

<What CI runs on which events — and what it does NOT run, so nobody treats it as a safety net it isn't.>

## Architecture

<The layers and the folders that matter, as a short annotated tree — folder level, never file by file.>

```
src/<layer>/   # what lives here
```

## Conventions

<Only what differs from the language's defaults, each concrete and checkable:>

- <Pattern> — see `<path/to/reference-file>` and follow it.
- <Wiring that has to happen in more than one place when adding X: list every place.>
- <Error handling, naming, imports, module system quirks.>
- <Configuration: where env vars are read — names only, never values.>

## Tests

<What exists, what's actually covered, what to do when changing behaviour (add tests? where?).>

## Git workflow

- **Branching:** <model — e.g. GitFlow with `main` (releases) and `develop` (integration); work on `feature/*`, `fix/*`, `hotfix/*`, `release/*`; never commit directly on `main`/`develop`.>
- **Into `main`:** <which branches may be merged into it, and how (PR only, merge or squash).>
- **Commits:** <Conventional Commits; language of the messages; scope convention.>
- **Pull requests:** <target branch per branch type; title format enforced by CI; template.>
- **Versions:** <bumped by hand in `<file>` — or automatic (release-please / semantic-release / …): never bump by hand.>
- **Records:** <e.g. features, bugfixes and hotfixes are recorded in `docs/changes/` before and after the code.>

## Language

<Language for answers to the user, code comments, commit messages, PR descriptions, docs.>

## Gotchas

- <Things that look right and aren't in this repo.>

## Never

- <Commit secrets or `.env` files · force-push · skip hooks with `--no-verify` · edit generated files (`<paths>`) · …>

## More context

- <`README.md` for setup · `docs/…` for the domain model / ADRs · the knowledge base wiki, if any.>
