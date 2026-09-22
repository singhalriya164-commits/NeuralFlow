"""
NEURALFLOW BUILDER CORE
========================
Strict IEEE A4 two-column template helpers.
Column width: 3.32 in (239 pt), gutter: 0.25 in (18 pt).
Tables: max 3.32 in wide, 7-point font, no vertical borders.
Figures: max 3.30 in wide, 300 DPI.
"""

import os, io, zipfile
import docx
from docx.shared import Inches, Pt, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# ── exact column geometry ─────────────────────────────────────────────────────
COL_W_IN   = 3.27          # single-column printable width (inches)
COL_W_EMU  = int(COL_W_IN * 914400)  # in EMU

# ── namespace conversion ──────────────────────────────────────────────────────
_STRICT_MAP = [
    (b'http://purl.oclc.org/ooxml/officeDocument/relationships',
     b'http://schemas.openxmlformats.org/officeDocument/2006/relationships'),
    (b'http://purl.oclc.org/ooxml/wordprocessingml/main',
     b'http://schemas.openxmlformats.org/wordprocessingml/2006/main'),
    (b'http://purl.oclc.org/ooxml/drawingml/main',
     b'http://schemas.openxmlformats.org/drawingml/2006/main'),
    (b'http://purl.oclc.org/ooxml/drawingml/wordprocessingDrawing',
     b'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'),
    (b'http://purl.oclc.org/ooxml/officeDocument/math',
     b'http://schemas.openxmlformats.org/officeDocument/2006/math'),
]

def strict_to_transitional(data: bytes) -> bytes:
    for a, b in _STRICT_MAP:
        data = data.replace(a, b)
    return data


def load_template_doc(path: str) -> docx.Document:
    buf = io.BytesIO()
    with zipfile.ZipFile(path, 'r') as zin, \
         zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            zout.writestr(item, strict_to_transitional(zin.read(item.filename)))
    buf.seek(0)
    return docx.Document(buf)


# ── table helpers ─────────────────────────────────────────────────────────────

def _tcPr_remove(cell, tag):
    tcPr = cell._tc.get_or_add_tcPr()
    for e in tcPr.xpath(f'./w:{tag}'):
        tcPr.remove(e)


def set_cell_margins(cell, top=30, bottom=30, left=36, right=36):
    tcPr = cell._tc.get_or_add_tcPr()
    for e in tcPr.xpath('./w:tcMar'):
        tcPr.remove(e)
    tcPr.append(parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    ))


def set_cell_borders(cell, top="none", bottom="none"):
    """IEEE: only top/bottom horizontal rules, no vertical lines."""
    top_xml = ('<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
               if top == "single" else '<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>')
    bot_xml = ('<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
               if bottom == "single" else '<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>')
    tcPr = cell._tc.get_or_add_tcPr()
    for e in tcPr.xpath('./w:tcBorders'):
        tcPr.remove(e)
    tcPr.append(parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'{top_xml}{bot_xml}'
        f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'</w:tcBorders>'
    ))


def _fix_table_width(tbl, total_emu=COL_W_EMU):
    """Force the table's XML w:tblW to exact column width."""
    tblPr = tbl._tbl.xpath('./w:tblPr')
    if not tblPr:
        return
    pr = tblPr[0]
    for e in pr.xpath('./w:tblW'):
        pr.remove(e)
    # width in dxa (twips), 1 in = 1440 twips
    dxa = int(total_emu / 914400 * 1440)
    pr.append(parse_xml(
        f'<w:tblW {nsdecls("w")} w:w="{dxa}" w:type="dxa"/>'
    ))


# ── heading helpers ───────────────────────────────────────────────────────────

def add_heading_1(doc, text):
    p = doc.add_paragraph(style='Heading 1')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(3)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    return p


def add_heading_2(doc, text):
    p = doc.add_paragraph(style='Heading 2')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    return p


def add_heading_3(doc, text):
    p = doc.add_paragraph(style='Heading 3')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    return p


def add_heading_4(doc, text):
    p = doc.add_paragraph(style='Heading 4')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after  = Pt(2)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    return p


def add_heading_5(doc, text):
    p = doc.add_paragraph(style='Heading 5')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after  = Pt(3)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    return p


# ── body text ─────────────────────────────────────────────────────────────────

def add_body_p(doc, text, indent=True):
    p = doc.add_paragraph(style='Body Text')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(3)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.first_line_indent = Inches(0.16) if indent else Inches(0)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)
    return p


def add_bullet_item(doc, bold_prefix, text):
    p = doc.add_paragraph(style='bullet list')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after  = Pt(1)
    p.paragraph_format.left_indent  = Inches(0.18)
    p.paragraph_format.first_line_indent = Inches(-0.1)
    if bold_prefix:
        r1 = p.add_run(f"\u2022  {bold_prefix} ")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(9)
        r1.font.bold = True
    r2 = p.add_run(text)
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(9)
    return p


# ── equations ────────────────────────────────────────────────────────────────

def add_equation(doc, eq_text, eq_num):
    """
    Two-cell table: [eq text centred | (n) right-aligned]
    Total width = single column width.
    """
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    _fix_table_width(tbl)

    w_eq  = int(COL_W_EMU * 0.85)
    w_num = COL_W_EMU - w_eq

    c0, c1 = tbl.rows[0].cells
    c0.width = w_eq
    c1.width = w_num

    # remove all borders from both cells
    for cell in (c0, c1):
        set_cell_borders(cell, "none", "none")
        set_cell_margins(cell, top=20, bottom=20, left=20, right=20)

    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(1)
    p0.paragraph_format.space_after  = Pt(1)
    r0 = p0.add_run(eq_text)
    r0.font.name   = 'Times New Roman'
    r0.font.size   = Pt(9.5)
    r0.font.italic = True

    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.space_before = Pt(1)
    p1.paragraph_format.space_after  = Pt(1)
    r1 = p1.add_run(f"({eq_num})")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(9.5)


# ── figures ───────────────────────────────────────────────────────────────────

def add_figure(doc, img_path, caption_text, fig_num):
    """Insert figure at exactly COL_W_IN wide, with IEEE caption below."""
    if not os.path.exists(img_path):
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after  = Pt(1)
    p_img.paragraph_format.keep_with_next = True
    p_img.add_run().add_picture(img_path, width=Inches(COL_W_IN))

    p_cap = doc.add_paragraph(style='figure caption')
    p_cap.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cap.paragraph_format.space_before = Pt(1)
    p_cap.paragraph_format.space_after  = Pt(5)
    r_num = p_cap.add_run(f"Fig. {fig_num}.  ")
    r_num.font.name = 'Times New Roman'
    r_num.font.size = Pt(8)
    r_num.font.bold = True
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(8)


# ── tables ────────────────────────────────────────────────────────────────────

def add_table_ieee(doc, title, col_names, data_rows, col_fracs, footnote=None):
    """
    col_fracs: list of fractions summing to 1.0 (e.g. [0.4, 0.3, 0.3])
    Total table width is locked to COL_W_EMU.
    """
    # ---- title ----
    p_head = doc.add_paragraph(style='table head')
    p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_head.paragraph_format.space_before = Pt(6)
    p_head.paragraph_format.space_after  = Pt(1)
    p_head.paragraph_format.keep_with_next = True
    r_head = p_head.add_run(title)
    r_head.font.name = 'Times New Roman'
    r_head.font.size = Pt(7.5)

    # ---- build table ----
    ncols = len(col_names)
    nrows = len(data_rows)
    tbl = doc.add_table(rows=nrows + 1, cols=ncols)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    _fix_table_width(tbl)

    col_emus = [int(f * COL_W_EMU) for f in col_fracs]

    # header row
    hdr = tbl.rows[0]
    for ci, name in enumerate(col_names):
        cell = hdr.cells[ci]
        cell.width = col_emus[ci]
        set_cell_margins(cell, top=25, bottom=25, left=30, right=30)
        set_cell_borders(cell, top="single", bottom="single")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after  = Pt(0)
        r = p.add_run(name)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(6.5)
        r.font.bold = True

    # data rows
    for ri, row_data in enumerate(data_rows):
        row = tbl.rows[ri + 1]
        is_last = (ri == nrows - 1)
        for ci, val in enumerate(row_data):
            cell = row.cells[ci]
            cell.width = col_emus[ci]
            set_cell_margins(cell, top=18, bottom=18, left=30, right=30)
            set_cell_borders(cell, "none", "single" if is_last else "none")
            p = cell.paragraphs[0]
            p.alignment = (WD_ALIGN_PARAGRAPH.LEFT if ci == 0
                           else WD_ALIGN_PARAGRAPH.CENTER)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after  = Pt(0)
            r = p.add_run(str(val))
            r.font.name = 'Times New Roman'
            r.font.size = Pt(6.5)

    if footnote:
        p_fn = doc.add_paragraph(style='table footnote')
        p_fn.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_fn.paragraph_format.space_before = Pt(1)
        p_fn.paragraph_format.space_after  = Pt(4)
        r_fn = p_fn.add_run(f"\u2020 {footnote}")
        r_fn.font.name   = 'Times New Roman'
        r_fn.font.size   = Pt(6)
        r_fn.font.italic = True


# ── references ────────────────────────────────────────────────────────────────

def add_reference_item(doc, ref_num, authors, title=None, publication=None, year=None, extra=""):
    p = doc.add_paragraph(style='references')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after  = Pt(2)
    p.paragraph_format.left_indent  = Inches(0.18)
    p.paragraph_format.first_line_indent = Inches(-0.18)
    p.paragraph_format.line_spacing = Pt(9)

    def _r(text, bold=False, italic=False):
        run = p.add_run(text)
        run.font.name   = 'Times New Roman'
        run.font.size   = Pt(7.5)
        run.font.bold   = bold
        run.font.italic = italic

    _r(f"[{ref_num}] ")
    if title is None:
        _r(str(authors))
    else:
        _r(f"{authors}, ")
        _r(f'"{title}," ', italic=False)
        if publication:
            _r(f"{publication}, ", italic=True)
        if year:
            _r(f"{year}.")
        if extra:
            _r(f" {extra}")
    return p
