---
name: study-summary
description: Write a complete, printable study summary (Word .docx + PDF) of a course, a block of it or a few topics, inside a research knowledge base created by the knowledge-base skill — built from the wiki, the detail in raw/ (slides, books, exercise sheets, solutions) and the exam map, giving each topic space in proportion to how much it weighs in the exams, with worked examples, common mistakes and the real exam questions on each topic. Shows the outline for approval before writing, keeps one versioned file per scope (no date in the name), and renders through pandoc and Word. Use when the user wants a summary, revision notes or study notes to print — e.g. "faz um resumo de ENGCIA", "resumo completo para o exame", "resumo da matéria de restrições", "quero imprimir a matéria", "study notes", "summary for the exam".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(find *), Bash(python *), Bash(py *), Bash(pandoc *), Bash(winget install *), Bash(brew install *), Bash(sudo apt-get install *), Skill, AskUserQuestion
---

# Study summary

A summary to print and study from: everything the course asks for, weighted by what the exams actually ask, in a Word document and a PDF. It's a view of the knowledge base made for printing — the knowledge itself stays in the wiki.

## Ground rules

- **Markdown without hard wraps.** Every `.md` this skill writes has one paragraph, list item or table row per line, however long — never broken at 80/100 columns; the viewer wraps lines. Line breaks only between blocks and inside code blocks (and, in flashcard decks, inside a card, where a line break is part of the card).
- **`raw/` has no rules and is never written to.** Read whatever is there; don't expect a structure. Don't assume the KB is a git repository.
- **Ground everything in the KB.** Every definition, formula and example comes from the wiki or `raw/`, cited in the section it's used in. Anything from general knowledge is marked as being outside the KB; a made-up example is marked as made up. Never fill a gap with a guess. **Missing from the wiki is not missing from the KB:** when the wiki lacks what a topic or an exam question needs (a definition, a formula, a table, a worked example, the detail a catalog question relies on), go and find it in `raw/` and put it into the summary — never write "see the slides / the book, p. X" in place of the content, the reader must not be sent away to look it up. Only when `raw/` doesn't have it either, say so in the document and in the report.
- **Write in the KB's language** (`language:` in `KB_GUIDE.md`); technical terms stay as-is. `templates/summary.md` is in English — translate its headings, labels and frontmatter values.
- **No changelog anywhere in the summary** — not in the document, not in the frontmatter. Only the version number and the date, on the cover and in the footer.

## Steps

1. **Find the knowledge base and the course** — same discovery as `exam-map`: a `wiki/` next to a `KB_GUIDE.md` with `mode: research`; the course is one of the wiki's areas (ask if ambiguous).

2. **Check the renderer.** Run `pandoc --version`.
   - If pandoc is missing, **tell the user** that it's needed to produce the Word/PDF files, and ask with `AskUserQuestion` whether you should install it: `winget install --id JohnMacFarlane.Pandoc -e` on Windows, `brew install pandoc` on macOS, `sudo apt-get install pandoc` on Debian/Ubuntu. Install only on a yes, then check `pandoc --version` again (a new terminal may be needed for PATH — on Windows, look in `%LOCALAPPDATA%\Pandoc\pandoc.exe` too).
   - On a no, carry on and write only the `.md` source; say at the end that the Word/PDF files weren't produced and why.
   - Also check `python -c "import docx"` (python-docx, used for the styles and the footer). If it's missing, ask before running `python -m pip install python-docx`.

3. **Agree the scope and the level.** Use what the user said; ask only for what's missing:
   - **Scope** — the whole course, a block (a wiki sub-folder such as "2. Programação com Restrições"), a list of topics (wiki articles), or **my weak spots** — the 🔴 and 🟡 topics of the course's progress record, in its study-priority order.
   - **Level** — `complete` (default: everything the course covers, at exam depth) or `condensed` (for last-minute revision: definitions, formulas, methods and the exam box, no long examples).

4. **Gather the material.**
   - **The wiki first** — the area's index and every article in scope, and what they link to.
   - **`raw/` for the detail the wiki summarised away** — exact definitions, formulas, figures, tables, worked examples from exercise sheets and solutions. This is also the fallback for anything the wiki doesn't give: for every topic, and especially for the real questions in the catalog, check that the summary will contain everything needed to answer them, and read the right `raw/` files (through `wiki/sources.md`, or by searching `raw/` when the wiki has no pointer) for whatever is missing. Use `wiki/sources.md` to find which files back each article. Read PDFs with `Read`, using the `pdf` skill for scanned ones.
   - **The exam map** — the course's exams article and question catalog (written by `exam-map`): each topic's ranking, number of exams and weight, and the real questions. If there is no exam map, say so and offer to run `exam-map` first; if the user prefers to go on without it, write the summary without weights and say so on its quick map.
   - **The progress record**, if `correct-attempt` has started one for the course (`<progress>-<course>.md` in the study folder): the user's state per topic (🔴/🟡/🟢) and their recurring mistakes, so the quick map can show it and each topic's common mistakes can include the ones they actually make.
   - **Notes** — only `kind: message` notes that say something about the assessment (e.g. what a teacher said would come up), attributed to who said it.

5. **Show the outline and wait for a yes.** Before writing anything, show in chat:
   - the topics in course order (the order of the wiki/sources, not of the ranking), each with its 🔥/⚠️/📎 band, number of exams and weight;
   - how deep each one goes — space proportional to its weight: 🔥 topics get every subsection and full worked examples, ⚠️ a normal treatment, 📎 a short one;
   - topics the exams ask about that neither the wiki nor `raw/` cover (after searching `raw/` — what was found only in `raw/` is not a gap);
   - an estimate of the page count. Adjust if the user changes it, and only then write.

6. **Write the source** following `templates/summary.md`:
   - **Cover** (pandoc title block from the frontmatter): course, scope, "version N — date".
   - **Quick map** — topic, exams, weight, band; the band rule in one line. With a progress record, add a column with the user's state per topic.
   - **One section per topic**, in course order, with its band in the heading and "comes up in X of N exams, about Y% of the grade" under it, then: concepts and definitions; formulas and rules (LaTeX `$…$`/`$$…$$` — pandoc turns them into Word equations); the method step by step; a worked example (`Example box`); common mistakes (`Warning box`, from solutions, marking criteria and repeated errors); **how it comes up in the exam** (`Exam box`: one to three real questions with their catalog id, marks and one-line summary); related topics.
   - **Self-assessment** — questions to test yourself with, drawn from the catalog, with their ids.
   - **Sources** — the wiki articles and `raw/` files used, with slide/page ranges.
   - Code in fenced blocks with the language (```prolog, ```java, ```python…), tables as pipe tables. Figures from `raw/`: export the page or image into a `figuras/` subfolder next to the source (translated name) and link it relatively; never write into `raw/`.
   - **Notes about the document never go in the running text.** The text of a section is the content — definitions, formulas, methods, examples — and nothing else. Remarks *about* the content ("not found in the KB or in `raw/`", "the sources disagree", "example made up for this summary", "this came up in question N22-P4b of exam X") go in a `Note box` at the end of the subsection they refer to, one short line each; how a topic comes up in the exams belongs in its `Exam box`, not scattered through the definitions. Never write a line like "the wiki doesn't list them, check slide X before the exam" as a bullet among the concepts.
   - Use the boxes only through the four custom styles above (`Exam box`, `Warning box`, `Example box`, `Note box`) (`::: {custom-style="…"}`). Don't put Obsidian-only syntax in the document (callouts, embeds); `[[links]]` are fine — the renderer turns them into plain text.

7. **Save it where the KB says.** Look up the study purpose folder in `KB_GUIDE.md`/ `outputs/README.md` (e.g. `outputs/<area>/estudo/`). Each summary is its own folder, named by scope, without a date:
   ```
   outputs/<area>/<study>/<summary>-<scope>/
   ├── <summary>-<scope>.md     source, with the frontmatter
   ├── <summary>-<scope>.docx
   ├── <summary>-<scope>.pdf
   └── <figures>/               only when there are figures
   ```
   `<summary>` is "summary" in the KB's language (e.g. `resumo`), `<scope>` a short slug: the course's own name for the whole course (`resumo-engcia`), or the block or topic (`resumo-restricoes`).
   - **Versions:** the file name never changes and always holds the latest version. A new summary starts at version 1; regenerating an existing one with content changes bumps `version` and sets `updated` to today; re-rendering without content changes keeps both. Older versions aren't kept — they can be regenerated from the wiki.

8. **Render**: `python <plugin>/scripts/render.py <source.md>` (the plugin's `scripts/` folder, two levels above this skill). It writes the `.docx` and `.pdf` next to the source, with the cover, a table of contents, the boxes, Word equations, highlighted code, and "title — vN — date" plus the page number in the footer. Layout is automatic: every top-level `#` section starts on a new page, and paragraphs, code blocks, boxes and tables are never cut across pages (a small table (up to 12 rows and about 1200 characters) stays whole on one page; a larger one breaks only between rows and repeats its header) — so use `#` only for the major sections and `##` for what lives inside them.
   - Exit code 3 means pandoc is missing — go back to step 2. Exit code 4 means pandoc rejected the source — fix the markdown and run it again.
   - If the last line says the PDF was skipped (no Word or LibreOffice), report that the `.docx` is ready and the PDF isn't.

9. **Index it.** Add one short row to the index table in `outputs/README.md` (type: summary, what for: one sentence, status: the KB's word for *final*, as listed in `outputs/README.md` — e.g. `final` in `pt-PT`), or update the existing row's date and version.

10. **Keep the wiki the single source of truth.** A summary is never promoted into the wiki as a whole. If writing it surfaced something the wiki doesn't say yet (a definition, an example, a detail from `raw/`), offer to capture it as a note (`capture-note`) so `compile-wiki` folds it into the wiki — then the next version of the summary will carry it from there.

11. **Report**: the files written, version, page count, what the KB didn't cover, any place where sources disagreed, and whether the PDF was produced.

## Notes

- Write for printing: no "click here", no colour-only meaning, tables that fit A4 portrait and stay short enough to sit on one page (split a long table by topic instead of one giant one). Use the band and state emoji (🔥 ⚠️ 📎, 🔴 🟡 🟢 ⚪) freely in the `.md`: the renderer swaps them for plain symbols in the Word/PDF (●●● ●●○ ●○○, ▼ ◆ ▲ ○), which keeps the PDF small — so the quick map's legend line must name each band in words too.
- A summary covers what the course teaches; the exam map only decides how much space each topic gets. A topic that never comes up still gets its short section if it's in scope.
- Don't summarise exam questions beyond one line each — the catalog links to the papers.
