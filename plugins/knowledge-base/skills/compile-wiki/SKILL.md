---
name: compile-wiki
description: Compile/update the markdown wiki/ of a knowledge base created by the knowledge-base skill — research mode (summarize raw/ sources into concept articles) or code mode (fold notes/, git commits, GitHub issues, and pull requests into decision/subsystem articles, plus regenerate an always-current wiki/Estrutura.md project structure and domain-model overview). Cross-links articles and keeps wiki/index.md current. Use when the user wants to compile, refresh, sync, or update their wiki, process newly added sources/notes, or asks to "run the ingest".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(find *), Bash(mkdir *), Bash(mv *), Bash(git log *), Bash(git show *), Bash(git rev-parse *), Bash(gh repo view *), Bash(gh issue list *), Bash(gh pr list *), AskUserQuestion
---

# Compile wiki

Turns whatever's pending — external sources or your own notes/commits — into the compiled
markdown wiki in `wiki/`, incrementally. Behavior branches on the KB's mode.

## Steps

1. **Find the knowledge base.** If the user gave a path, use it. Otherwise look in the current
   directory (and immediate subdirectories) for a `wiki/` next to a `KB_GUIDE.md`. If exactly
   one candidate is found, confirm it with the user before touching anything. If none or several
   are found, ask for the path.

2. **Read `KB_GUIDE.md`'s frontmatter** to get `mode` (`research` or `code`), `topic` and
   `language`. If the file has no frontmatter, treat it as `research` mode for backward
   compatibility. If `language` is set, write every article in it (technical terms stay as-is)
   and skip the language inference described below; if it's missing (older KBs), fall back to
   the inference rules and offer to record the choice in `KB_GUIDE.md`.

3. **Load shared context.** Read `wiki/index.md` (current map of content). If `wiki/_geral/`
   exists (a directory link into a general/shared vault), skim its `index.md` too, so you can
   link out to existing general concepts instead of duplicating them locally.

4. Follow the steps for the KB's mode:

### Research mode

a. Read `wiki/sources.md` if it exists — a manifest of every raw source, a one-line summary,
   which wiki article(s) cover it, and when it was last compiled. Create it (with a header row)
   if it doesn't exist yet.

b. List every file under `raw/` recursively (skip its `README.md`). A source is *pending* if it
   has no entry in `wiki/sources.md`, or if its mtime is newer than the "last compiled" date
   recorded there. If nothing is pending here and step (d) finds no pending notes either, skip
   ahead to the Deletions check; if that finds nothing too, say so and stop.

c. For each pending source:
   - Read it in full. For very large files, read enough to summarize accurately and note in
     `wiki/sources.md` that it was only partially read.
   - Decide which existing concept article it belongs to, or whether it warrants a new one.
     Prefer extending an existing article over fragmenting the wiki.
   - Write or update that concept article under `wiki/`: synthesize, don't copy-paste. Cite the
     source back with a relative link into `raw/` (e.g. `[source](../raw/paper.pdf)`).
   - **Write in the language of the source material**, not the language of this instruction file
     or of the chat. If sources are mixed, match whichever language dominates this KB's sources so
     far (check `wiki/sources.md` / existing articles) rather than switching per-source; ask the
     user once, on the first source, if it's genuinely ambiguous. Keep technical/domain terms,
     proper nouns, API and library names, and established jargon in their original language even
     when the surrounding prose is translated — don't force a translation nobody in the field uses.
   - Cross-link related articles with Obsidian-style `[[Article Name]]` links. If a concept
     already has an article in `wiki/_geral/`, link there (`[[_geral/Article Name]]`) instead of
     duplicating it.
   - Embed any associated images from `raw/` with a relative markdown image link — don't copy
     the bytes.
   - Add/update the source's row in `wiki/sources.md`: path, one-line summary, article(s) it
     feeds, today's date.

d. **Process pending notes** (skip if there's no `notes/` folder). Notes are the user's own
   material and what other people told them, not external sources, so they aren't tracked in
   `wiki/sources.md`. Pending notes are the loose files at the top of `notes/` (glob
   `notes/*.md`, not recursive, skipping `README.md`) whose frontmatter is missing or doesn't
   say `status: compiled`. Subfolders of `notes/` are the archive — never reprocess them. For
   each pending note:
   - Read it and fold it into the concept article it relates to (or a new one). If its
     frontmatter has `source:`, attach it to the article covering that `raw/` file. Prefer
     extending what the article says over adding a parallel section that repeats it.
   - Respect `kind:`:
     - `thought` (default) and `decision` are the author's view — mark them as such, apart
       from what the sources say (e.g. a "Notas pessoais"/"Decisões" section, or an inline
       "(nota minha)").
     - `message` is someone else's word: attribute it to `from:` (e.g. "segundo o perito"),
       neither as the author's view nor as something a `raw/` source states.
     - `ai-response` is **unverified**: attribute it to `from:` (e.g. "segundo o ChatGPT") and
       never state it as fact unless a `raw/` source backs it up, in which case cite that source.
     - `question` goes under the open questions of that concept.
   - Write in the KB's `language` (or the note's own, if `language` isn't set); technical terms
     stay as-is.
   - Rewrite the note's frontmatter to `status: compiled`, `compiled: <today's date>`, and
     `articles:` listing what it fed (keep `kind`, `from` and `source`). Leave the body untouched.
   - **Archive it**: move the file to `notes/<area>/`, where `<area>` is the wiki area folder of
     the main article it fed (`general/` — in the KB's language — if it fits no area;
     `notes/compiled/` if the wiki has no area folders at all). Create the folder if needed.
     Cite the note from the wiki by its archived path, e.g. `[nota](../../notes/<area>/<file>.md)`
     (relative to the article).
   - **Older KBs**: notes at the top of `notes/` that already say `status: compiled` were
     compiled before archiving existed. Don't reprocess them; list them in the report and offer
     to move each to its area (from its `articles:`), fixing the wiki links that cite it — only
     on a yes.

### Code mode

a. **Regenerate the structure overview.** Rewrite `wiki/Estrutura.md` from scratch every run
   (unlike everything else in this mode, this isn't incremental — it should always reflect the
   project as it is right now):
   - Folder/module layout: a short annotated tree of the meaningful directories (skip
     `node_modules/`, build output, etc.).
   - Tech stack: infer from manifest files present (`package.json`, `pyproject.toml`,
     `go.mod`, `Cargo.toml`, etc.) — languages, frameworks, key dependencies.
   - Entry points: main scripts, servers, CLI commands — wherever execution starts.
   - Domain model: if `KB_GUIDE.md`'s `domain_model` frontmatter field is set, read whatever it
     points to (files/folder or description) and summarize the key entities and how they
     relate. Render it as a small Mermaid class or ER diagram when the model is concrete enough
     (Obsidian renders Mermaid natively); otherwise a short prose summary is fine. Leave this
     section out entirely if `domain_model` is empty — don't invent one.
   - Make sure `wiki/index.md` links `Estrutura.md` first, as the "start here" entry.

b. **Process pending notes.** Same inbox rule as research mode: glob `notes/*.md` at the top
   level only (skip `README.md`); a note there is *pending* if its frontmatter is missing or
   doesn't say `status: compiled`. Subfolders are the archive. For each pending note:
   - Read it. Decide which existing wiki article (by decision/subsystem) it belongs to, or
     whether it warrants a new one.
   - Write or update that article: synthesize the note's content into it, don't paste it
     verbatim. Cross-link related articles with `[[Article Name]]` (link into `wiki/_geral/`
     when the concept already lives there). Write in the language the note itself is written in
     (same rule as research mode) — technical terms stay as-is.
   - A `kind: decision` note (e.g. from `adr-new`) feeds the article for that decision or
     subsystem as a recorded decision, with its context and consequences.
   - Rewrite the note's frontmatter to `status: compiled`, `compiled: <today's date>`, and
     `articles:` listing what it fed. Leave the note's body untouched.
   - Archive it exactly as in research mode (`notes/<area>/`, or `notes/compiled/` when the
     wiki has no area folders), citing it by its archived path; same handling for older notes
     already compiled at the top level.

c. **Walk repo activity since the last compile.** Read `last_compiled_at` from `KB_GUIDE.md`'s
   frontmatter.
   - If empty (first run), ask the user how far back to look (e.g. all history, last N months,
     since a given tag/date) and use that as the starting point instead of assuming.

   **Commits**: `git log --since="<last_compiled_at>" --oneline` (or the range from the
   first-run answer). Skim messages; use `git show <sha> --stat` when a message alone doesn't
   make the scope clear. Skip trivial commits (typos, formatting, dependency bumps).

   **Issues and pull requests**: first check `gh` is usable — `gh repo view` succeeds and the
   repo has a GitHub remote. If not, skip this part and note in the final report that
   issues/PRs weren't checked (missing/unauthenticated `gh` or no GitHub remote).

   Otherwise:
   - `gh issue list --state all --json number,title,body,state,updatedAt,url --limit 200`
   - `gh pr list --state all --json number,title,body,state,mergedAt,updatedAt,url --limit 200`

   Keep only entries updated after `last_compiled_at` (or everything, on a first run per the
   user's chosen range). A merged PR's description/discussion is often the best source for
   "why" — prefer it over the raw commit list when both cover the same change, to avoid
   documenting the same thing twice.

   For everything gathered (commits, issues, PRs), fold a short synthesized note into the
   relevant wiki article — create one if none fits — citing back: a commit hash (e.g.
   `` `abc1234` ``) for commits, or `#123` for issues/PRs.

   After processing, set `last_compiled_at` in `KB_GUIDE.md`'s frontmatter to the current UTC
   timestamp.

   If there's nothing new anywhere — no pending notes, no new commits, no new issues/PRs — and
   the deletions check below also finds nothing, say so and stop. Don't rewrite the wiki when
   there's nothing pending.

### Deletions (both modes)

Run this after the mode-specific steps (and even when nothing else is pending): removing a
source or a note must be reflected in the wiki, not just addition.

a. **Find what's gone.**
   - Research mode: every row of `wiki/sources.md` whose file no longer exists under `raw/`.
   - Both modes: every link from `wiki/` articles into `../raw/…` or `../notes/…` whose target
     no longer exists (this catches deleted notes, which leave no manifest row behind).

b. **Guard against a false alarm.** If `raw/` is a link (or contains one) and it doesn't
   resolve, or lists as empty while `wiki/sources.md` has many rows, the external folder is
   probably just unmounted or moved — **stop, report it, and change nothing.** Same if nearly
   everything looks deleted at once.

c. **Show the user what would change and get a yes before editing**, since this removes wiki
   content: for each vanished source/note, the articles that cite it. A file that reappears
   under another name/path is a rename, not a deletion — update the citation instead of
   dropping the content.

d. **Reconcile each affected article:**
   - Remove the citation and any statement that only that source/note supported; keep what other
     sources or notes still back. Never leave a link to a file that doesn't exist.
   - If that leaves an article with no remaining source or note, propose deleting it (ask; don't
     delete silently), then remove it from `wiki/index.md` and repoint or remove `[[wikilinks]]`
     to it from other articles.
   - Remove the vanished source's row from `wiki/sources.md`.

e. **Code mode extra:** `wiki/Estrutura.md` is regenerated every run so it already drops
   deleted files; articles that cite a deleted repo path in backticks are only *flagged* in the
   report (code moves legitimately), not rewritten.

5. **Refresh `wiki/index.md`** once everything pending is processed: make sure every
   concept/article is listed and grouped sensibly, and remove stale entries for articles that no
   longer exist.

6. **Report back**: what was processed (sources/notes/commits/issues/PRs), which articles were
   created vs. updated vs. trimmed or removed because a source/note was deleted, and flag anything skipped (unreadable formats, datasets too large to
   read directly — research mode may need a dedicated tool in `tools/` instead; or issues/PRs
   skipped because `gh` wasn't usable). In code mode, confirm `wiki/Estrutura.md` was refreshed.

## Notes

- Safe to re-run any time — only what's pending (or deleted) gets touched. Deletions are never
  applied without showing the affected articles and getting a yes first.
- No RAG/vector DB needed at small-to-medium scale: the index files plus direct reads of
  relevant articles are enough context to work from.
- Never edit files inside `raw/` (research mode) — it's the append-only source of truth. In
  both modes, never rewrite a note's body — only its frontmatter, and move it to its archive
  folder once compiled.
- The wiki is the single source of truth. Never replace an article's content with a pointer to
  something in `outputs/` ("the analysis is in outputs/…") — if it's knowledge, it goes in the
  article. Outputs may link to the wiki, not stand in for it.
- Never assume a research-mode KB is a git repository: nothing in research mode reads or
  writes git. Only code mode walks git history, because it lives inside a code repo.
- Never write into `wiki/_geral/` — it's a directory link into a general vault maintained by its
  own `compile-wiki` run. Read and link to it, don't edit through it.
- `gh` is optional for code mode: if it's not installed/authenticated or there's no GitHub
  remote, still process notes and git log — don't block the whole run on it.
- Language is not fixed by this skill or by the English `SKILL.md`/README files of this plugin —
  those document the tool, not the wiki it produces. The wiki follows the source material (see
  step 4's language rule); once a KB has settled on one, stay consistent across articles rather
  than drifting per session.
