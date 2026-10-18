---
name: study-plan
description: Build a day-by-day study plan up to one or more exams, inside a research knowledge base created by the knowledge-base skill — time per topic in proportion to exam weight × weakness × size, phases (material, practice, mock exams under exam conditions), daily flashcards, spaced review and buffer days, each day with concrete tasks that link the KB's study material and say which study skill to run. Asks how the user studies (reading vs exercises, order, session length…) and shapes the plan around it. Saves a markdown plan with checkboxes (markdown only — no Word/PDF) and, after asking, an .ics file and/or events in the user's calendar when a calendar connector is active. Also answers "what do I have today?" and replans from what's done. Use when the user wants a study plan, a revision schedule or a calendar up to an exam, or says they're behind — e.g. "faz-me um plano de estudo até ao exame", "plano para a época de exames", "o que tenho hoje?", "estou atrasado, replaneia", "study plan", "revision timetable".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(find *), Bash(python *), Bash(py *), AskUserQuestion
---

# Study plan

A calendar to the exam that spends the time where it pays: on the topics that weigh most in the exams and where the user is weakest, with practice and mock exams before the day, and enough slack to survive a bad week.

## Ground rules

- **Markdown without hard wraps.** Every `.md` this skill writes has one paragraph, list item or table row per line, however long — never broken at 80/100 columns; the viewer wraps lines. Line breaks only between blocks and inside code blocks (and, in flashcard decks, inside a card, where a line break is part of the card).
- **Plan with the user's real time.** Never assume hours or dates: ask for what can't be read from the KB.
- **Tasks are concrete**: a section of a summary with its pages, catalog questions by id, a quiz on a topic, a mock exam — with the study skill to run for each. Never "study Bayes".
- **Nothing reaches the user's calendar without a yes.** Creating events is outward-facing: show what would be created and wait for confirmation; ask before writing the `.ics` too.
- **`raw/` has no rules and is never written to.** Don't assume the KB is a git repository.
- **The KB's language**; the template is in English — translate headings, labels, frontmatter values (keys stay in English) and `exam_label`.

## Steps

1. **Find the knowledge base and the courses** — same discovery as `exam-map`. A plan can cover one course or several whose exams fall in the same season; then it is one plan that interleaves them.

2. **Ask for what the KB can't tell.** With `AskUserQuestion` where it fits:
   - the **date** (and time, if known) of each exam;
   - the **start** of the plan (default: today);
   - the **hours available** per weekday (e.g. 2 h on weekdays, 5 h on Saturday, none on Sunday);
   - **days off**;
   - **how they study** — it is individual, so ask instead of assuming (step 3).

3. **Ask how the user studies.** Don't impose a method. First look for hints in what exists — past plans, the progress record, the study folder (lots of summaries and few solved sheets says something) — and propose a default from them, then confirm with `AskUserQuestion`. Examples of what to settle (these are only examples; follow what the user says):
   - the **mix**: more reading/summaries or more exercises, and roughly in what proportion;
   - the **order**: all reading first and exercises after, or each topic read then practised straight away (interleaved);
   - the **session shape**: long blocks or short ones with breaks, best time of day, subjects per day;
   - how they like to **review**: flashcards, quizzes, rewriting, past exams — or which they dislike;
   - anything else they volunteer (e.g. weekends for mocks only, never two courses in one day).
   Record the answers in the plan's frontmatter (`study_style`) so replans reuse them without asking again unless the user wants to change them.

4. **Gather the data** for each course:
   - the exams article (bands, weights) and the question catalog;
   - the progress record (`references/progress.md` in the plugin): each topic's state 🔴/🟡/🟢/⚪ and the study priority;
   - the size of each topic, estimated from its wiki article and the number of slides/pages behind it in `raw/` (through `wiki/sources.md`);
   - the study material that already exists in the study folder — summaries, mock exams, flashcards, solved exercise sheets.

5. **Share out the time.** Hours per topic in proportion to **exam weight × weakness × size**, then split each topic's hours between reading and practice following the user's mix (step 3), with weakness 🔴 ×1.5, 🟡 ×1.2, ⚪ ×1, 🟢 ×0.6. Reserve 10–15% of the total as free buffer, and the daily flashcard time (15–20 min) before sharing out the rest. If the time can't cover the material, say so and propose what to cut (📎 topics already 🟢 first) rather than cramming.

6. **Lay out the phases** for each course, backwards from its exam, in the order the user chose in step 3 (the default below is reading first, then practice; an interleaved style merges phases 1 and 2 topic by topic):
   1. **material** — each topic's summary section, in course order;
   2. **practice** — exercise sheets and real catalog questions per topic, and a quiz per topic;
   3. **final stretch** — two or three mock exams under exam conditions, each followed by marking (`correct-attempt`) and a review of the mistakes; the last day before the exam light. Throughout: flashcards every study day; each topic comes back a few days after it was studied (spaced review); with several courses, interleave them and give the nearest exam more weight in its final week.
   **Past exams go oldest first, most recent last.** Whenever the plan uses real past exams — catalog questions in the practice phase, whole exams solved or taken as mock exams in the final stretch — order them by date, oldest earliest, so the most recent exams (the best picture of the current exam's style and difficulty) are the last ones done, untouched until the final stretch. Don't spend a recent exam's questions on early topic practice when older ones cover the topic.

7. **Fill each day with concrete tasks**, each with its duration and, where a skill does it, the skill: `ENGCIA summary — Bayes section (pp. 12–20)`, `Solve N23-P3 and R21-P2 — solve-exam in hints mode if stuck`, `Quiz on Bayes — quiz`, `Mock exam 1 under exam conditions — mock-exam`, then `Mark it — correct-attempt`. Respect the session shape from step 3 (block length, tasks per day). When material a task needs doesn't exist yet (no summary, no flashcards), schedule making it first (`study-summary`, `flashcards`).

8. **Show the plan's outline and wait for a yes**: the study style you understood, hours per course and per topic, the phase dates, the mock exam days, the buffer, and anything that didn't fit.

9. **Write the plan** following `templates/plan.md` — frontmatter (exams, availability, study style, version), an overview (hours per course and per topic), then one section per week with a table (day, hours, focus) and one `### YYYY-MM-DD · weekday · N h` heading per day with its tasks as `- [ ]` checkboxes and durations. Keep that heading and task format: `make_ics.py` and replanning read it.

10. **Save it where the KB says** — the study purpose folder in `KB_GUIDE.md`/`outputs/README.md`: `outputs/<area>/<study>/<plan>-<scope>/` for one course, or the general area's study folder (e.g. `outputs/geral/estudo/`) when the plan covers several, with names in the KB's language (`plano-<scope>`; scope = the course, or the season, e.g. `plano-epoca-normal-2026-27`). Versioned like summaries: the name never changes, `version`/`updated` in the frontmatter, no changelog. The plan is the `.md` only — don't render a Word or PDF. Add or update one short row in the index table of `outputs/README.md`.

11. **Calendar — ask first.** Check whether a calendar connector is available in this session (tools that create calendar events, e.g. Google Calendar's). Then ask with `AskUserQuestion`:
    - with a connector: create the events **in the calendar**, write an **`.ics`** to import, **both**, or **neither**;
    - without one: write an **`.ics`** to import, or not. Also ask whether study blocks should be all-day events or start at a set time (e.g. 18:00).
    - **`.ics`**: `python <plugin>/scripts/make_ics.py <plan.md> [--start HH:MM]` writes `<plan>.ics` next to the plan (one event per study day with its tasks in the description, one per exam).
    - **Calendar connector**: `python <plugin>/scripts/make_ics.py <plan.md> --json [--start HH:MM]` prints the same events. Show how many would be created and three examples, and only after a yes create them one by one with the connector, in the calendar the user chooses. Report what was created; if some failed, say which. Never delete or change existing events. When replanning after events were created, ask before creating the new ones, and remind the user that the old ones are still there.

12. **Report**: the files written, hours per course, the mock exam dates, what didn't fit, and the calendar outcome.

## What do I have today?

Read the latest plan for the course(s), find today's heading, and answer in the chat with today's unchecked tasks (and any unchecked ones from past days). Don't write anything.

## Replan

"Estou atrasado", "replaneia", or a change of exam date or availability: read the plan's checked and unchecked tasks, re-read the progress record (states may have changed since), and rebuild the plan from today to the exams with what's left — checked tasks stay as done in the past days. Show the new outline (step 8), then write it as the next version (steps 9–11).

## Notes

- Never promote a plan into the wiki.
- A day with no available hours gets no tasks; don't move work onto days off.
