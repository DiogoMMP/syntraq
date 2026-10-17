---
name: resume
description: Give a "where was I" briefing for a personal project's knowledge base — current structure, recent decisions/notes, and recent git activity (including uncommitted changes). Use when the user wants to resume, catch up on, or get reacquainted with a project after a break, or asks "where was I", "what's the status", or "catch me up".
allowed-tools: Read, Glob, Grep, Bash(git log *), Bash(git status *), Bash(git diff --stat *)
---

# Resume

A read-only briefing for picking a project back up after time away. Never edits the knowledge base or the repo — this is purely a summary.

## Steps

1. **Find the knowledge base.** Same discovery as `compile-wiki`: look for `wiki/` next to `KB_GUIDE.md` nearby, ask if not found or ambiguous.

2. **Read `KB_GUIDE.md`'s frontmatter** for `mode` and `topic`, and read `wiki/index.md`. In code mode, also read `wiki/Estrutura.md` if present — it's the fastest way to re-orient on what the project even is.

3. **Gather recent activity**, branching on mode:

   **Code mode:**
   - Pending notes at the top level of `notes/` (files without `status: compiled`; its subfolders are the archive) — these are unfinished thoughts from last time, likely the most useful signal of "what I was in the middle of".
   - The last few *compiled* notes (by `compiled:` date, in the archive subfolders) for recent context.
   - `git log --oneline -20` (or since `last_compiled_at` if that's more recent) for recent commits.
   - `git status --short` and `git diff --stat` for anything uncommitted — this is often literally what was left mid-edit.

   **Research mode:**
   - The most recent rows in `wiki/sources.md` (by date) for what was last ingested.
   - Any files in `raw/` with no corresponding entry in `wiki/sources.md` — unfinished ingest work.
   - Pending notes at the top level of `notes/` (files without `status: compiled`; its subfolders are the archive), noting any `kind: question` ones as open questions and any `kind: message` ones as replies still to fold in, plus the last few compiled notes for context.
   - No git: a research KB is not assumed to be a repository.

4. **Write the briefing** directly in the response (not to a file): a short paragraph on what the project is (from `wiki/index.md` / `Estrutura.md`), then bullet points for open threads (pending notes/sources, uncommitted changes) and recent decisions. End with a concrete suggestion for a next step when one is obvious (e.g. "tens 3 notas por compilar e 2 ficheiros por commitar — talvez corras `compile-wiki` primeiro").

## Notes

- Read-only: never write to `wiki/`, `notes/`, `raw/`, or the repo. If something looks like it needs fixing (e.g. lots of pending notes piling up), say so instead of acting on it.
- Keep the briefing tight — a few bullets, not a full replay of the git log.
