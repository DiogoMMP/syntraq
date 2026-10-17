# README style — voice and formatting

The README should read like a senior engineer briefing a new colleague: dense, specific, and always saying *why*.

---

## Voice

**Write for the new joiner who will break something.** Every rule states the trap it prevents. Compare:

- ✗ "We use the factory pattern for entity creation."
- ✓ "**Factories** build entities; **update paths mutate** the loaded entity — calling the factory on an update would INSERT a new row."

**Assert, don't hedge.** State the rule and the consequence. No "generally", "should", "we try to". If something is genuinely conditional, name the condition.

**Name real things.** Real class names, real folder paths, real policy names, real ports, real error codes. A sentence with no proper noun in it is usually filler.

**Say why, once, briefly.** The most valuable half-sentences in a good README are the rationales — why a lint rule is disabled, why jobs are invoked through DI instead of HTTP, why the schema is owned by the migration tool and not the ORM. One clause is enough.

**No filler.** Never: "This project aims to…", "In this section we will…", "Feel free to…", "Happy coding!", "As you can see". No emoji. No exclamation marks.

**Third person, present tense, active.** "The API serves…", "Repositories return the page and the total; the service assembles the envelope." Use the imperative only for instructions to the reader ("Never force-push the protected branches").

**Density over length.** A prose lead of 1–3 lines, then a table or bullets. If a paragraph runs past four lines, it is probably a table.

---

## Formatting

**Never hard-wrap.** One paragraph, list item or table row per line, however long — never break prose at 80/100/110 columns; the viewer wraps it, and manual breaks only make diffs noisy and the README awkward on other screen widths. Line breaks belong between blocks and inside code fences only. If the repo's markdownlint enforces a line length (MD013), say so and ask instead of wrapping.

**Horizontal rules.** `---` between every `##` section, and after the lead paragraph. Never between a `###` and its parent.

**Headings.** One `#` (the title). `##` for sections, `###` for sub-sections, `####` for numbered setup steps. Sentence case, not Title Case. `&` not `and` in headings.

**Bold** for terms being defined and for the choice column in tables. *Italics* for an optional/aside qualifier (`| **<Tool>** | *Optional* | … |`). `Backticks` for every path, file, command, type, property, env var, port, error code and package name — no exceptions.

**Tables.** Always left-aligned: `| :--- | :--- | :--- |`. Header words are singular nouns. Never leave a cell empty in a table whose other rows are filled, except the last column where "no caveat" is a legitimate value. Prefer a table to any list of pairs.

**Bullets.** `-` only. One rule per bullet. Lead with the bolded subject, then an em-dash, then the rule. Sub-bullets one level deep at most.

**Numbered lists** only for genuinely ordered steps.

**Code fences.** Always tagged: `powershell`, `bash`, `json`, `sql`, `mermaid`, `csharp`, `ts`. The *Solution layout* tree is the one deliberately untagged block. Put a `#` comment inside the fence when a command needs a caveat — that is where readers actually look:

```bash
# Whole suite
<test command>

# Single module
<test command with filter>
```

**Blockquotes** for one thing only: a caveat or an external-doc pointer that must not be missed.

**Links.** Relative for anything in the repo, and the link text is the path in backticks: [`docs/some-guide.md`](docs/some-guide.md). Absolute only for genuinely external documentation. Every link verified against the filesystem.

**Numbers.** Pick one thousands style and keep it (thin space or plain digits) — do not mix. Versions exactly as the manifest pins them.

**Em-dashes** (`—`) for the explanatory aside, which is this format's characteristic move. At most one per sentence.

---

## Anti-patterns

| Don't | Do |
| :--- | :--- |
| "Uses an ORM for data access." | "**\<ORM\> \<version\>** + `\<driver\>` — ORM only; the schema is owned by \<migration tool\>." |
| "Run the tests." | A fenced block with the real commands and their inline comments. |
| "Configure your environment variables." | The complete settings / `.env` example, redacted. |
| "Standard GitFlow." | The branch table with the real ticket-key pattern, plus the rules for the protected branches. |
| A `## Jobs` section saying "N/A". | No `## Jobs` section at all. |
| "See the code for details." | The path to the code, and the one-line rule the code implements. |
| A badge for a tech absent from the tech-stack table. | Badges and table agree, version for version. |
| A `<SLOT>` or a `>>` guidance line from the template. | Every slot replaced with an evidenced fact, or the line deleted. |
