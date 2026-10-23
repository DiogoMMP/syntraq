---
title: "Study plan — {{COURSES}}"
subtitle: "{{START}} to {{LAST_EXAM}}"
date: "Version {{VERSION}} — {{UPDATED}}"
lang: {{LANGUAGE}}
toc: false
version: {{VERSION}}
updated: {{UPDATED}}
type: study-plan
scope: {{SCOPE_SLUG}}
courses: [{{AREAS}}]
start: {{START}}
exam_label: Exam
exams:
  - ENGCIA: 2027-01-12 09:30 1h
  - PPROGIA: 2027-01-15 14:00 2h
study_style:
  mix: more reading than exercises
  order: reading first, then exercises
  sessions: 45 min blocks with short breaks
  review: flashcards and quizzes
availability:
  weekdays: 2h
  saturday: 5h
  sunday: 0h
  off: [2026-12-24, 2026-12-25]
based_on:
  - "[[Exams of ENGCIA]]"
  - outputs/ENGCIA/study/progress-engcia/progress-engcia.md
notion_page: https://www.notion.so/...   # only when the plan was put in Notion
status: final
---

# Overview

| Course | Exam | Hours | Weakest topics first |
| --- | --- | --- | --- |
| ENGCIA | 2027-01-12 | 38 h | Bayes (🔴, 🔥), Temporal (🟡, 🔥) |

Phases: **material** (until {{DATE}}) → **practice** (until {{DATE}}) → **final stretch** (mock exams). Flashcards every day; each topic comes back a few days after it was studied; about 10–15% of the time is left free for days that go wrong.

| Topic | Course | Band | State | Hours |
| --- | --- | --- | --- | --- |
| Bayes | ENGCIA | 🔥 | 🔴 | 6 h |

# Week 1 — {{DATES}}

| Day | Hours | Focus |
| --- | --- | --- |
| Mon 20 | 2 h | ENGCIA — Bayes |

### 2026-10-20 · Monday · 2 h

- [ ] ENGCIA summary — Bayes section (pp. 12–20) · 1 h
- [ ] Solve N23-P3 and R21-P2 (catalog) — `solve-exam` in hints mode if stuck · 40 min
- [ ] Flashcards ENGCIA · 20 min

### 2026-10-21 · Tuesday · 2 h

- [ ] Quiz of 10 questions on Bayes — `quiz` · 30 min
- [ ] …

# Week 2 — {{DATES}}

### 2026-10-31 · Saturday · 5 h

- [ ] Mock exam 1 under exam conditions — `mock-exam` · 1 h
- [ ] Mark it — `correct-attempt` · 30 min
- [ ] Review the mistakes in the summary · 1 h
- [ ] Free time (buffer) · 1 h
