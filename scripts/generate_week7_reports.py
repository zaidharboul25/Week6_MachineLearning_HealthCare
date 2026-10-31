# -*- coding: utf-8 -*-
"""
HealthConnect Rwanda — Week 7 Report Formatter (DOCX & PDF).
Generates:
- deliverables/HealthConnect_Week7_ML_Engineering_Report.docx
- deliverables/HealthConnect_Week7_ML_Engineering_Report.pdf
"""

import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from markdown_pdf import Section, MarkdownPdf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
DELIVERABLES_DIR = PROJECT_ROOT / "deliverables"

# Deep Corporate Color Palette
COLOR_PRIMARY_HEX = "1B365D"      # Navy
COLOR_SECONDARY_HEX = "008080"    # Teal Accent
COLOR_DARK_TEXT_HEX = "1E293B"    # Slate Dark
COLOR_LIGHT_BG_HEX = "F1F5F9"     # Light Slate Header
COLOR_BORDER_HEX = "CBD5E1"       # Light Grey Border

COLOR_PRIMARY = RGBColor(27, 54, 93)
COLOR_SECONDARY = RGBColor(0, 128, 128)
COLOR_DARK_TEXT = RGBColor(30, 41, 59)
COLOR_MUTED = RGBColor(100, 116, 139)


def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def build_docx_report(md_content: str, output_path: Path):
    doc = docx.Document()
    
    # Page setup - Margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # 1. Title Page / Header Block
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(20)
    title_p.paragraph_format.space_after = Pt(10)
    run_title = title_p.add_run("HealthConnect Clinic Experience Lab")
    run_title.font.name = "Arial"
    run_title.font.size = Pt(26)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_PRIMARY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(15)
    run_sub = sub_p.add_run("Week 7 Machine Learning Engineering Testing & End-to-End Validation Report")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(16)
    run_sub.font.bold = True
    run_sub.font.color.rgb = COLOR_SECONDARY

    # Metadata Table
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Programme", "AnalystLab Africa Experience Lab Internship Programme"),
        ("Project Title", "Improving Patient Appointment Attendance & Healthcare Support Using Data and AI"),
        ("Track", "Machine Learning Engineering"),
        ("Lead Engineer", "Zaid Harboul"),
        ("Milestone", "Week 7: Pipeline Testing, Reliability, Refinement & End-to-End Validation"),
        ("Status & Verification", "100% Passed (65/65 Automated Tests, 9/9 E2E Stages Verified)")
    ]
    for row_idx, (k, v) in enumerate(meta_data):
        row = meta_table.rows[row_idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.text = k
        cell_v.text = v
        set_cell_background(cell_k, COLOR_LIGHT_BG_HEX)
        cell_k.paragraphs[0].runs[0].font.bold = True
        cell_k.paragraphs[0].runs[0].font.color.rgb = COLOR_PRIMARY
        cell_v.paragraphs[0].runs[0].font.color.rgb = COLOR_DARK_TEXT
        set_cell_margins(cell_k, 60, 60, 100, 100)
        set_cell_margins(cell_v, 60, 60, 100, 100)

    doc.add_page_break()

    # Process Markdown Lines into DOCX Elements
    lines = md_content.splitlines()
    in_table = False
    table_lines = []

    for line in lines:
        stripped = line.strip()

        # Handle Markdown Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            in_table = True
            table_lines.append(stripped)
            continue
        elif in_table:
            # End of table, render it
            if table_lines:
                render_docx_table(doc, table_lines)
                table_lines = []
            in_table = False

        if not stripped:
            continue

        # Headers
        if stripped.startswith("# "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            run = p.add_run(stripped[2:])
            run.font.name = "Arial"
            run.font.size = Pt(20)
            run.font.bold = True
            run.font.color.rgb = COLOR_PRIMARY
        elif stripped.startswith("## "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(stripped[3:])
            run.font.name = "Arial"
            run.font.size = Pt(15)
            run.font.bold = True
            run.font.color.rgb = COLOR_PRIMARY
        elif stripped.startswith("### "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(stripped[4:])
            run.font.name = "Arial"
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = COLOR_SECONDARY
        elif stripped.startswith("- ") or stripped.startswith("* "):
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after = Pt(3)
            run = p.add_run(stripped[2:])
            run.font.name = "Calibri"
            run.font.size = Pt(10.5)
            run.font.color.rgb = COLOR_DARK_TEXT
        elif stripped.startswith("```"):
            continue  # Fenced code markers
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(stripped)
            run.font.name = "Calibri"
            run.font.size = Pt(10.5)
            run.font.color.rgb = COLOR_DARK_TEXT

    if table_lines:
        render_docx_table(doc, table_lines)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    print(f"Generated DOCX: {output_path}")


def render_docx_table(doc, table_lines):
    rows_data = []
    for l in table_lines:
        if "---" in l:
            continue
        cells = [c.strip() for c in l.split("|")[1:-1]]
        if cells:
            rows_data.append(cells)
    
    if not rows_data:
        return

    n_rows = len(rows_data)
    n_cols = len(rows_data[0])
    table = doc.add_table(rows=n_rows, cols=n_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for r_idx, row in enumerate(rows_data):
        for c_idx in range(min(n_cols, len(row))):
            cell = table.rows[r_idx].cells[c_idx]
            cell.text = row[c_idx]
            set_cell_margins(cell, 50, 50, 80, 80)
            if r_idx == 0:
                set_cell_background(cell, COLOR_PRIMARY_HEX)
                if cell.paragraphs[0].runs:
                    cell.paragraphs[0].runs[0].font.bold = True
                    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, COLOR_LIGHT_BG_HEX)
                if cell.paragraphs[0].runs:
                    cell.paragraphs[0].runs[0].font.size = Pt(9.5)
                    cell.paragraphs[0].runs[0].font.color.rgb = COLOR_DARK_TEXT
    doc.add_paragraph().paragraph_format.space_after = Pt(8)


def build_pdf_report(md_content: str, output_path: Path):
    pdf = MarkdownPdf(toc_level=2)
    
    # Custom CSS for executive presentation
    css = """
    body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #1e293b;
        font-size: 10.5pt;
        line-height: 1.5;
    }
    h1 {
        color: #1b365d;
        font-size: 20pt;
        border-bottom: 2px solid #1b365d;
        padding-bottom: 4px;
        margin-top: 18pt;
    }
    h2 {
        color: #1b365d;
        font-size: 14pt;
        margin-top: 14pt;
        border-bottom: 1px solid #cbd5e1;
        padding-bottom: 2px;
    }
    h3 {
        color: #008080;
        font-size: 11.5pt;
        margin-top: 10pt;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 12pt 0;
        font-size: 9pt;
    }
    th {
        background-color: #1b365d;
        color: #ffffff;
        font-weight: bold;
        padding: 6pt;
        border: 1px solid #cbd5e1;
        text-align: left;
    }
    td {
        padding: 5pt;
        border: 1px solid #cbd5e1;
    }
    tr:nth-child(even) {
        background-color: #f8fafc;
    }
    code {
        background-color: #f1f5f9;
        padding: 2pt 4pt;
        border-radius: 3px;
        font-family: Consolas, Monaco, monospace;
        font-size: 9pt;
    }
    pre {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #1b365d;
        padding: 8pt;
        font-size: 8.5pt;
        overflow-x: auto;
    }
    """
    pdf.add_section(Section(md_content, toc=False), user_css=css)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.save(str(output_path))
    print(f"Generated PDF: {output_path}")


def main():
    report_md_path = REPORTS_DIR / "HealthConnect_Week7_ML_Engineering_Testing_Report.md"
    if not report_md_path.exists():
        print(f"Error: {report_md_path} does not exist.")
        sys.exit(1)

    with open(report_md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    docx_path = DELIVERABLES_DIR / "HealthConnect_Week7_ML_Engineering_Report.docx"
    pdf_path = DELIVERABLES_DIR / "HealthConnect_Week7_ML_Engineering_Report.pdf"

    build_docx_report(md_text, docx_path)
    build_pdf_report(md_text, pdf_path)
    print("All deliverables generated successfully!")

if __name__ == "__main__":
    main()

