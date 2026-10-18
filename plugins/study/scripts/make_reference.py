"""Build the reference.docx that gives study documents their look (fonts, headings, boxes, page).

It starts from pandoc's own default reference.docx — so every style pandoc emits exists — and
restyles it. The result is cached per user and rebuilt when STYLE_VERSION changes, so nothing
binary has to live in the plugin.

Custom paragraph styles, used from markdown as fenced divs:
    ::: {custom-style="Exam box"}      how a topic comes up in the exam (real questions)
    ::: {custom-style="Warning box"}   common mistakes
    ::: {custom-style="Example box"}   worked examples

Usage (normally called by render.py): python make_reference.py [<output.docx>]
"""

import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

STYLE_VERSION = 3

BODY_FONT = "Calibri"
CODE_FONT = "Consolas"
ACCENT = RGBColor(0x1F, 0x3A, 0x5F)

BOXES = {
    "Exam box": ("DCE8F5", "2E5C8A"),
    "Warning box": ("FBEBD6", "C77C1E"),
    "Example box": ("EEEEEE", "7A7A7A"),
}


def cache_dir():
    if platform.system() == "Windows":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return base / "study-plugin"


def cached_reference(pandoc):
    path = cache_dir() / f"reference-v{STYLE_VERSION}.docx"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        build(pandoc, path)
    return path


def shade_and_border(style, fill, border):
    p_pr = style.element.get_or_add_pPr()
    shading = OxmlElement("w:shd")
    shading.set(qn("w:val"), "clear")
    shading.set(qn("w:color"), "auto")
    shading.set(qn("w:fill"), fill)
    borders = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    for key, value in (("val", "single"), ("sz", "24"), ("space", "8"), ("color", border)):
        left.set(qn(f"w:{key}"), value)
    borders.append(left)
    p_pr.append(borders)
    p_pr.append(shading)


def style_or_none(doc, name):
    try:
        return doc.styles[name]
    except KeyError:
        return None


def build(pandoc, out):
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "default.docx"
        with open(base, "wb") as handle:
            subprocess.run([pandoc, "--print-default-data-file", "reference.docx"], stdout=handle, check=True)
        doc = Document(str(base))

    for section in doc.sections:
        section.page_width, section.page_height = Cm(21), Cm(29.7)
        section.left_margin = section.right_margin = Cm(2)
        section.top_margin = section.bottom_margin = Cm(2)

    for name in ("Normal", "Body Text", "First Paragraph", "Compact"):
        style = style_or_none(doc, name)
        if style is not None:
            style.font.name = BODY_FONT
            style.font.size = Pt(11)
            style.paragraph_format.space_after = Pt(6)
            # A paragraph is never cut across two pages, and no lone first/last line is left behind.
            style.paragraph_format.keep_together = True
            style.paragraph_format.widow_control = True

    for level, size in ((1, 18), (2, 14), (3, 12), (4, 11)):
        style = style_or_none(doc, f"Heading {level}")
        if style is not None:
            style.font.name = BODY_FONT
            style.font.size = Pt(size)
            style.font.bold = True
            style.font.color.rgb = ACCENT
            style.paragraph_format.space_before = Pt(14 if level <= 2 else 10)
            style.paragraph_format.keep_with_next = True
    heading_1 = style_or_none(doc, "Heading 1")
    if heading_1 is not None:
        # Every major section starts on a new page (render.py can switch this off per document).
        heading_1.paragraph_format.page_break_before = True
        heading_1.paragraph_format.space_before = Pt(22)

    for name in ("Title", "Subtitle"):
        style = style_or_none(doc, name)
        if style is not None:
            style.font.name = BODY_FONT
            style.font.color.rgb = ACCENT

    for name in ("Source Code", "Verbatim Char"):
        style = style_or_none(doc, name)
        if style is not None:
            style.font.name = CODE_FONT
            style.font.size = Pt(9.5)
            if style.type == WD_STYLE_TYPE.PARAGRAPH:
                style.paragraph_format.keep_together = True

    body = style_or_none(doc, "Body Text") or doc.styles["Normal"]
    for name, (fill, border) in BOXES.items():
        style = style_or_none(doc, name) or doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        style.base_style = body
        style.font.name = BODY_FONT
        style.font.size = Pt(10.5)
        style.paragraph_format.left_indent = Cm(0.4)
        style.paragraph_format.space_after = Pt(4)
        style.paragraph_format.keep_together = True
        shade_and_border(style, fill, border)

    doc.save(str(out))


def main():
    pandoc = shutil.which("pandoc")
    if not pandoc:
        sys.stderr.write("pandoc not found on PATH\n")
        sys.exit(3)
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else cache_dir() / f"reference-v{STYLE_VERSION}.docx"
    out.parent.mkdir(parents=True, exist_ok=True)
    build(pandoc, out)
    print(out)


if __name__ == "__main__":
    main()
