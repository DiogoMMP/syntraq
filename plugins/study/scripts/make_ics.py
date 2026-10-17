"""Turn a study plan written in markdown into an .ics calendar file (no dependencies).

Usage:
    python make_ics.py <plan.md> [--start HH:MM] [--json]

Writes <plan>.ics next to the source: one event per study day (its tasks in the description)
and one per exam. Study days are all-day events, or timed events starting at --start and lasting
the day's hours. With --json, prints the same events as JSON instead (used to create them through
a calendar connector) and writes nothing.

Plan format the script reads:

    ---
    title: "Study plan — ENGCIA and PPROGIA"
    exam_label: Exam           word used in the exam events, in the plan's language (e.g. "Exame")
    exams:
      - ENGCIA: 2027-01-12 09:30 1h
      - PPROGIA: 2027-01-15 14:00 2h
    ---

    ### 2026-10-20 · Monday · 2 h
    - [ ] ENGCIA summary — Bayes (pp. 12–20) · 1 h
    - [x] Flashcards ENGCIA · 20 min

Day headings start with "### YYYY-MM-DD"; the hours, if any, follow a "·" as "N h", "N,5 h" or
"N min". Tasks are "- [ ]" / "- [x]" lines under a day. Done tasks are left out of the events.

Exit codes: 0 ok, 2 bad input.
"""

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

DAY = re.compile(r"^###\s+(\d{4}-\d{2}-\d{2})\b(.*)$")
TASK = re.compile(r"^\s*-\s+\[( |x|X)\]\s+(.*)$")
HOURS = re.compile(r"(\d+(?:[.,]\d+)?)\s*(h|min)\b")
WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
EXAM = re.compile(r"^\s*-\s+([^:]+):\s*(\d{4}-\d{2}-\d{2})(?:\s+(\d{1,2}:\d{2}))?(?:\s+(\d+(?:[.,]\d+)?)\s*h)?\s*$")


def plain(text):
    """Calendar apps show text, not markdown: drop wiki links, code marks and emphasis."""
    text = WIKILINK.sub(lambda m: m.group(2) or m.group(1).split("/")[-1], text)
    text = re.sub(r"`([^`]*)`", lambda m: m.group(1), text)
    text = re.sub(r"\*\*(.+?)\*\*|__(.+?)__", lambda m: m.group(1) or m.group(2), text)
    return re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", lambda m: m.group(1), text)


def minutes(text):
    total = 0.0
    for value, unit in HOURS.findall(text):
        number = float(value.replace(",", "."))
        total += number * 60 if unit == "h" else number
    return int(round(total))


def parse(source):
    text = source.read_text(encoding="utf-8")
    title, label, exams = source.stem, "Exam", []
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if match:
        in_exams = False
        for line in match.group(1).splitlines():
            if re.match(r"^title:\s*", line):
                title = line.split(":", 1)[1].strip().strip("\"'")
            if re.match(r"^exam_label:\s*", line):
                label = line.split(":", 1)[1].strip().strip("\"'")
            if re.match(r"^exams:\s*$", line):
                in_exams = True
                continue
            if in_exams:
                exam = EXAM.match(line)
                if exam:
                    exams.append({"course": exam.group(1).strip(), "date": exam.group(2),
                                  "time": exam.group(3), "hours": exam.group(4)})
                elif not line.startswith(" "):
                    in_exams = False
    days, current = [], None
    for line in text.splitlines():
        day = DAY.match(line)
        if day:
            current = {"date": day.group(1), "minutes": minutes(day.group(2)), "tasks": []}
            days.append(current)
            continue
        task = TASK.match(line)
        if task and current is not None:
            if task.group(1) == " ":
                current["tasks"].append(plain(task.group(2).strip()))
            else:
                current["done"] = True
    days = [d for d in days if d["tasks"]]
    if not days and not exams:
        sys.stderr.write("no study days or exams found\n")
        sys.exit(2)
    for item in days + exams:
        try:
            dt.date.fromisoformat(item["date"])
        except ValueError:
            sys.stderr.write(f"bad date: {item['date']}\n")
            sys.exit(2)
    return title, label, days, exams


def events(title, label, days, exams, start):
    out = []
    for day in days:
        remaining = sum(minutes(t) for t in day["tasks"])
        # once some of the day's tasks are checked off, the block lasts only as long as what's left
        mins = (remaining or day["minutes"]) if day.get("done") else (day["minutes"] or remaining)
        first = re.sub(r"\s*·[^·]*$", "", day["tasks"][0])
        first = re.sub(r"\s+—\s+`[^`]+`.*$", "", first)
        summary = first + (f" (+{len(day['tasks']) - 1})" if len(day["tasks"]) > 1 else "")
        event = {"summary": summary, "description": "\n".join(f"- {t}" for t in day["tasks"]),
                 "date": day["date"], "uid": f"study|{day['date']}"}
        if start and mins:
            event["start"] = f"{day['date']}T{start}"
            begin = dt.datetime.fromisoformat(event["start"])
            event["end"] = (begin + dt.timedelta(minutes=mins)).isoformat(timespec="minutes")
        out.append(event)
    for exam in exams:
        event = {"summary": f"{label} — {exam['course']}", "description": title, "date": exam["date"],
                 "uid": f"exam|{exam['course']}|{exam['date']}"}
        if exam["time"]:
            event["start"] = f"{exam['date']}T{exam['time']:0>5}"
            hours = float((exam["hours"] or "2").replace(",", "."))
            begin = dt.datetime.fromisoformat(event["start"])
            event["end"] = (begin + dt.timedelta(hours=hours)).isoformat(timespec="minutes")
        out.append(event)
    return out


def escape(text):
    return text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold(line):
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    parts, chunk = [], b""
    for char in line:
        encoded = char.encode("utf-8")
        if len(chunk) + len(encoded) > (75 if not parts else 74):
            parts.append(chunk.decode("utf-8"))
            chunk = b""
        chunk += encoded
    parts.append(chunk.decode("utf-8"))
    return "\r\n ".join(parts)


def to_ics(source, items):
    now = dt.datetime.now(dt.timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    sequence = int(now.timestamp() // 60)  # a later export is a newer revision of the same events
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//study-plugin//study-plan//EN", "CALSCALE:GREGORIAN"]
    for item in items:
        # the UID depends only on the plan and the day (or exam), so re-importing an updated plan
        # updates the same events instead of adding new ones when tasks change
        uid = hashlib.sha1(f"{source.name}|{item['uid']}".encode("utf-8")).hexdigest()
        lines += ["BEGIN:VEVENT", f"UID:{uid}@study-plugin", f"DTSTAMP:{stamp}", f"SEQUENCE:{sequence}"]
        if "start" in item:
            begin = dt.datetime.fromisoformat(item["start"]).strftime("%Y%m%dT%H%M%S")
            end = dt.datetime.fromisoformat(item["end"]).strftime("%Y%m%dT%H%M%S")
            lines += [f"DTSTART:{begin}", f"DTEND:{end}"]
        else:
            day = dt.date.fromisoformat(item["date"])
            lines += [f"DTSTART;VALUE=DATE:{day:%Y%m%d}", f"DTEND;VALUE=DATE:{day + dt.timedelta(days=1):%Y%m%d}"]
        lines += [f"SUMMARY:{escape(item['summary'])}", f"DESCRIPTION:{escape(item['description'])}", "END:VEVENT"]
    lines.append("END:VCALENDAR")
    out = source.with_suffix(".ics")
    out.write_bytes(("\r\n".join(fold(line) for line in lines) + "\r\n").encode("utf-8"))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path)
    parser.add_argument("--start", help="start time of study blocks, HH:MM (default: all-day events)")
    parser.add_argument("--json", action="store_true", help="print the events as JSON instead of writing an .ics")
    args = parser.parse_args()
    source = args.source.resolve()
    if not source.is_file() or source.suffix.lower() != ".md":
        sys.stderr.write(f"not a markdown file: {source}\n")
        sys.exit(2)
    if args.start and not re.fullmatch(r"\d{1,2}:\d{2}", args.start):
        sys.stderr.write("--start must be HH:MM\n")
        sys.exit(2)
    title, label, days, exams = parse(source)
    items = events(title, label, days, exams, args.start and f"{args.start:0>5}")
    if args.json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return
    out = to_ics(source, items)
    print(f"{out} — {len(days)} study days, {len(exams)} exams")


if __name__ == "__main__":
    main()
