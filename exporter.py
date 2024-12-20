import os
from datetime import datetime
from pathlib import Path

import streamlit as st
from markdown_pdf import MarkdownPdf, Section


def export_to_markdown() -> str:
    output = f"# Report del {datetime.now().replace(microsecond=0).isoformat()}\n"
    output += "| # |Calcolo | Risultato | Voto | Commenti |\n"
    output += "|---|--------|-----------|------|----------|\n"
    for i, grade in enumerate(st.session_state.grades):
        output += f"|{i+1}|{grade.input}|{grade.result}|{grade.grade_value}|{grade.warning or ''}|\n"
    return output


def export_to_pdf():
    md = export_to_markdown()
    pdf = MarkdownPdf(toc_level=2)
    css = """
      table {
        border-collapse: collapse;
        width: 100%;
      }

      th, td {
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #ddd;
      }
    """
    pdf.add_section(Section(md), user_css=css)
    date_suffix = datetime.now().replace(microsecond=0).isoformat()
    pdf.meta["title"] = f"Report del {date_suffix}"
    pdf.meta["author"] = "Assistente"

    file_name = os.path.abspath("guide.pdf")
    pdf.save(file_name=file_name)
    print(f"Saved PDF {file_name}")
