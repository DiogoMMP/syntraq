# notes/

Your own material and what other people tell you, kept apart from `../raw/` (what the sources say). One file per note, not one growing file.

## Inbox and archive

- **Loose files at the top of `notes/` are pending.** Drop a new note here whenever you want; don't organise it.
- **`notes/<area>/` holds compiled notes.** When `compile-wiki` folds a note into `../wiki/`, it updates the note's frontmatter and moves it into the folder of the wiki area it fed (`general/` if it fits no area; `notes/compiled/` if the wiki has no area folders at all). So what is still to process is always just the files at the top level.

## Frontmatter

```markdown
---
status: pending
kind: message
from: the expert
source: raw/some/file.pdf
---

Whatever you want to write, unstructured. Paste AI answers and other people's messages as they are.
```

- `status` — `pending` until `compile-wiki` processes it.
- `kind` (optional) — what the note is:
  - `thought` (default) — your own idea, reaction or opinion.
  - `decision` — something that was decided, and why.
  - `question` — something still open.
  - `ai-response` — text produced by an AI (Claude, ChatGPT, …).
  - `message` — something another person sent or said: a teacher, an expert, a colleague.
- `from` — who or what produced it, for `ai-response` (which AI) and `message` (which person or role).
- `source` (optional) — the `raw/` file the note is about, so `compile-wiki` attaches it to the right article instead of guessing.

How the wiki treats each kind:

- `thought` and `decision` are your view — shown as such, distinct from what the sources state.
- `message` is attributed to `from:` ("according to the expert…") — someone else's word, neither yours nor a source's.
- `ai-response` is **unverified**: attributed to the AI, never stated as fact unless a `raw/` source backs it up.
- `question` goes under the open questions of the article it relates to.

After processing, `compile-wiki` rewrites the frontmatter to `status: compiled`, adds `compiled: <date>` and `articles:` (what it fed), and moves the file to `notes/<area>/`. The body is never rewritten.
