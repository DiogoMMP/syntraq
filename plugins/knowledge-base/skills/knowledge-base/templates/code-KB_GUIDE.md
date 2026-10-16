---
mode: code
topic: {{TOPIC}}
language: {{LANGUAGE}}
created: {{DATE}}
last_compiled_at:
domain_model:
---

# Knowledge Base guide — {{TOPIC}}

Conventions for any LLM session working in this directory. Lighter variant of Andrej Karpathy's
["LLM Knowledge Bases"](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) note,
adapted for a personal, single-author code repo: there's no large external corpus to ingest, so
there's no `raw/` — the source material is your own notes plus the repo's git history, issues,
and pull requests.

## Layout

- `wiki/` — the compiled knowledge base: `.md` files with backlinks, organized by
  decision/subsystem. LLM-maintained; you mostly just read it (e.g. in Obsidian).
  - `wiki/Estrutura.md` — always-current overview (folder layout, tech stack, entry points,
    domain model if any). Fully regenerated on every `compile-wiki` run, unlike the rest of the
    wiki which only accumulates what's new.
- `notes/` — one file per scratch note, each with a `status: pending`/`status: compiled`
  frontmatter marker (see `notes/README.md`). Drop thoughts here as you work: loose files at
  the top of `notes/` are pending, and `compile-wiki` moves each one into an archive folder
  (`notes/<area>/`, or `notes/compiled/` when the wiki has no areas) once it's folded in.

## Workflow

1. **Note** — whenever something worth remembering happens (a decision, a "why did I do it this
   way", a gotcha), drop a new file in `notes/` with `status: pending` frontmatter. Don't stop to
   organize it — that's `compile-wiki`'s job.
2. **Compile** — run `compile-wiki` periodically (or whenever you want the wiki caught up). It
   folds pending notes into the right wiki articles, walks commits, issues, and pull requests
   since `last_compiled_at` for anything note-worthy (issues/PRs need the `gh` CLI installed,
   authenticated, and a GitHub remote — otherwise it falls back to notes + git log only), and
   regenerates `wiki/Estrutura.md` from scratch (including the domain model described in
   `domain_model` below, if set). Cross-links related articles and keeps `wiki/index.md`
   current. Re-run it any time — only the decision articles are incremental; the structure
   overview is always rebuilt fresh.

## Ground rules

- The wiki is written and maintained by the LLM. You view it, you don't hand-edit it.
- Keep `wiki/index.md` accurate — it's the entry point for every future session.
- A note is done once `compile-wiki` marks it `status: compiled` and moves it to its archive
  folder — keep it there as a record, don't delete it.
- `wiki/Estrutura.md` reflects the project *right now* — don't hand-edit it either, it gets
  overwritten on the next compile.
