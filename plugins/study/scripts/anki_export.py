"""Export a flashcard deck written in markdown to Anki.

Usage:
    python anki_export.py <deck.md> [--apkg]

Writes <deck>.txt (Anki's text import, tab-separated, with header lines) next to the source, or
<deck>.apkg with --apkg (needs genanki; embeds images). Re-importing an updated deck updates the
existing notes — each card keeps its id as the note's GUID — so review history is kept.

Deck source format — frontmatter, then one block per card:

    ---
    deck: MEIA::ENGCIA
    anki_basic: Basic          name of Anki's basic note type in the user's install (e.g. "Básico")
    anki_cloze: Cloze          name of the cloze note type (e.g. "Omissão de palavras")
    ---

    <!-- card id=engcia-0001 type=basic tags="engcia bayes exame::frequente" -->
    Front, in markdown
    ---
    Back, in markdown
    Source: [[Raciocínio com Incerteza]], slides 12–14
    <!-- /card -->

    <!-- card id=engcia-0002 type=cloze tags="engcia drools" -->
    {{c1::insertLogical}} keeps a fact only while the rule's conditions hold.
    ---
    Optional back extra
    <!-- /card -->

Markdown supported in cards: **bold**, *italic*, `code`, $inline$ and $$display$$ math (turned
into Anki's MathJax), ![](image) (only in .apkg), [[wiki links]] (plain text), line breaks.

Exit codes: 0 ok, 2 bad input, 5 genanki missing for --apkg.
"""

import argparse
import hashlib
import html
import re
import sys
from pathlib import Path

CARD = re.compile(r"<!--\s*card\s+(.*?)-->\s*\n(.*?)\n<!--\s*/card\s*-->", re.S)
ATTR = re.compile(r'(\w+)=(?:"([^"]*)"|(\S+))')
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
WIKILINK = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def read_frontmatter(text):
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    meta = {}
    if match:
        for line in match.group(1).splitlines():
            pair = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
            if pair and pair.group(2):
                meta[pair.group(1)] = pair.group(2).strip().strip("\"'")
    return meta


def to_html(text, media):
    """Minimal markdown → HTML for a card field. Collects image paths into `media`."""
    keep = {}

    def protect(value):
        key = f"\x00{len(keep)}\x00"
        keep[key] = value
        return key

    text = re.sub(r"\$\$(.+?)\$\$", lambda m: protect(r"\[" + html.escape(m.group(1)) + r"\]"), text, flags=re.S)
    text = re.sub(r"\$(.+?)\$", lambda m: protect(r"\(" + html.escape(m.group(1)) + r"\)"), text)
    text = re.sub(r"`([^`]+)`", lambda m: protect("<code>" + html.escape(m.group(1)) + "</code>"), text)

    def image(m):
        path = m.group(1)
        media.append(path)
        return protect(f'<img src="{html.escape(Path(path).name)}">')

    text = IMAGE.sub(image, text)
    text = WIKILINK.sub(lambda m: m.group(2) or m.group(1).split("/")[-1], text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", text)
    text = text.strip().replace("\r\n", "\n").replace("\n", "<br>")
    for key, value in keep.items():
        text = text.replace(key, value)
    return text.replace("\t", " ")


def parse(source):
    text = source.read_text(encoding="utf-8")
    meta = read_frontmatter(text)
    cards, seen = [], set()
    for attrs, body in CARD.findall(text):
        fields = {m.group(1): m.group(2) if m.group(2) is not None else m.group(3) for m in ATTR.finditer(attrs)}
        card_id, kind = fields.get("id"), fields.get("type", "basic")
        if not card_id or kind not in ("basic", "cloze"):
            sys.stderr.write(f"card without a valid id/type: {attrs.strip()}\n")
            sys.exit(2)
        if card_id in seen:
            sys.stderr.write(f"duplicate card id: {card_id}\n")
            sys.exit(2)
        seen.add(card_id)
        parts = re.split(r"\n-{3,}\s*\n", body, maxsplit=1)
        front, back = parts[0], parts[1] if len(parts) > 1 else ""
        if kind == "cloze" and "{{c" not in front:
            sys.stderr.write(f"cloze card without a {{{{c1::…}}}} deletion: {card_id}\n")
            sys.exit(2)
        cards.append({"id": card_id, "type": kind, "front": front, "back": back,
                      "tags": fields.get("tags", "").split()})
    if not cards:
        sys.stderr.write("no cards found\n")
        sys.exit(2)
    return meta, cards


def export_txt(source, meta, cards):
    deck = meta.get("deck", source.stem)
    names = {"basic": meta.get("anki_basic", "Basic"), "cloze": meta.get("anki_cloze", "Cloze")}
    lines = ["#separator:tab", "#html:true", "#guid column:1", "#notetype column:2",
             "#deck column:3", "#tags column:6"]
    for card in cards:
        media = []
        front, back = to_html(card["front"], media), to_html(card["back"], media)
        if media:
            print(f"warning: {card['id']} has images, which a .txt import can't carry — use --apkg")
        lines.append("\t".join([card["id"], names[card["type"]], deck, front, back, " ".join(card["tags"])]))
    out = source.with_suffix(".txt")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def stable_id(text):
    return int(hashlib.sha1(text.encode("utf-8")).hexdigest()[:8], 16) | (1 << 30)


def export_apkg(source, meta, cards):
    try:
        import genanki
    except ImportError:
        sys.stderr.write("genanki not installed (python -m pip install genanki)\n")
        sys.exit(5)
    deck_name = meta.get("deck", source.stem)
    css = ".card { font-family: Calibri, Arial, sans-serif; font-size: 20px; text-align: left; }"
    basic = genanki.Model(
        stable_id("study-plugin basic"), "Study — Basic",
        fields=[{"name": "Front"}, {"name": "Back"}],
        templates=[{"name": "Card 1", "qfmt": "{{Front}}",
                    "afmt": '{{FrontSide}}<hr id="answer">{{Back}}'}],
        css=css,
    )
    cloze = genanki.Model(
        stable_id("study-plugin cloze"), "Study — Cloze",
        fields=[{"name": "Text"}, {"name": "Back Extra"}],
        templates=[{"name": "Cloze", "qfmt": "{{cloze:Text}}", "afmt": "{{cloze:Text}}<br>{{Back Extra}}"}],
        css=css, model_type=genanki.Model.CLOZE,
    )
    deck = genanki.Deck(stable_id(deck_name), deck_name)
    media_files = []
    for card in cards:
        media = []
        fields = [to_html(card["front"], media), to_html(card["back"], media)]
        for path in media:
            full = (source.parent / path).resolve()
            if not full.exists():
                sys.stderr.write(f"image not found for {card['id']}: {path}\n")
                sys.exit(2)
            media_files.append(str(full))
        model = basic if card["type"] == "basic" else cloze
        deck.add_note(genanki.Note(model=model, fields=fields, tags=card["tags"], guid=card["id"]))
    out = source.with_suffix(".apkg")
    package = genanki.Package(deck)
    package.media_files = sorted(set(media_files))
    package.write_to_file(str(out))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path)
    parser.add_argument("--apkg", action="store_true", help="write an .apkg with images (needs genanki)")
    args = parser.parse_args()
    source = args.source.resolve()
    if not source.is_file() or source.suffix.lower() != ".md":
        sys.stderr.write(f"not a markdown file: {source}\n")
        sys.exit(2)
    meta, cards = parse(source)
    out = export_apkg(source, meta, cards) if args.apkg else export_txt(source, meta, cards)
    counts = {kind: sum(c["type"] == kind for c in cards) for kind in ("basic", "cloze")}
    print(f"{out} — {len(cards)} cards ({counts['basic']} basic, {counts['cloze']} cloze)")


if __name__ == "__main__":
    main()
