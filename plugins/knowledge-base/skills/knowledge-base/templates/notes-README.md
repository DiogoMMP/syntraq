# notes/

Scratch notes — one file per note, not one growing file. Drop a thought here whenever you want to capture it (a decision, a "why did I do it this way", a gotcha you just hit) without stopping to organise it. `compile-wiki` reads this folder and folds pending notes into `../wiki/`.

## Inbox and archive

- **Loose files at the top of `notes/` are pending.**
- **Compiled notes are moved out of the way**: into `notes/<area>/` when `../wiki/` is split into area folders, or into `notes/compiled/` when it isn't. What is still to process is always just the files at the top level.

## Frontmatter

```markdown
---
status: pending
kind: decision
---

Whatever you want to write, unstructured.
```

- `status` — `pending` until `compile-wiki` processes it.
- `kind` (optional) — `thought` (default), `decision` (something decided, and why) or `question` (something still open).

After `compile-wiki` processes a note, it rewrites the frontmatter and moves the file to its archive folder:

```markdown
---
status: compiled
kind: decision
compiled: 2026-08-02
articles:
  - Some Article Name
---
```

The body is never rewritten. This keeps any single file small and means `compile-wiki` only ever has to read what's actually new.
