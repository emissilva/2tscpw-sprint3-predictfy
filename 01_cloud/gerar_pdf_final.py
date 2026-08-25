#!/usr/bin/env python3
"""Gera o PDF final com cabeçalho, rodapé, marcas e paginação."""

from __future__ import annotations

import base64
import subprocess
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "evidencias" / "entrega_final"
BRANDS = OUT / "marcas"


def data_url(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


predictfy = data_url(BRANDS / "predictfy-logo.svg", "image/svg+xml")
fiap = data_url(BRANDS / "fiap-oficial.ico", "image/x-icon")

header = f"""
<div style="width:100%;padding:0 12mm 2mm;font-family:Arial,sans-serif;color:#12324f">
  <div style="height:8mm;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #bdd3e5;padding:0 2mm">
    <div style="display:flex;align-items:center;gap:6px;font-size:9px;font-weight:700">
      <img src="{predictfy}" style="width:17px;height:17px">
      <span>Predictfy</span>
    </div>
    <div style="font-size:8px;color:#526d82;letter-spacing:.35px">CLOUD SOLUTIONS · SPRINT 3</div>
    <div style="display:flex;align-items:center;gap:5px;color:#ed145b;font-size:10px;font-weight:800;letter-spacing:1px">
      <img src="{fiap}" style="width:16px;height:16px;image-rendering:auto">
      <span>FIAP</span>
    </div>
  </div>
</div>
"""

footer = """
<div style="width:100%;padding:2mm 12mm 0;font-family:Arial,sans-serif;color:#526d82">
  <div style="height:7mm;display:flex;align-items:center;justify-content:space-between;border-top:1px solid #bdd3e5;padding:0 2mm;font-size:8px">
    <span>Challenge Locaweb 2026</span>
    <span>Cloud Solutions &amp; Scalable Infrastructure</span>
    <span>Página <span class="pageNumber"></span> de <span class="totalPages"></span></span>
  </div>
</div>
"""

with tempfile.TemporaryDirectory(prefix="predictfy_pdf_") as temporary:
    temporary_path = Path(temporary)
    cover_pdf = temporary_path / "capa.pdf"
    content_pdf = temporary_path / "conteudo.pdf"

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()

        cover = browser.new_page()
        cover.goto((OUT / "RELATORIO_ENTREGA_COMPLETO.html").as_uri(), wait_until="networkidle")
        cover.add_style_tag(content="""
            @page { margin: 0 !important; }
            .page:not(.cover) { display: none !important; }
            .cover { width: 210mm !important; height: 297mm !important; margin: 0 !important; }
        """)
        cover.pdf(
            path=str(cover_pdf),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            display_header_footer=False,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )

        content = browser.new_page()
        content.goto((OUT / "RELATORIO_ENTREGA_COMPLETO.html").as_uri(), wait_until="networkidle")
        content.add_style_tag(content="""
            @page { margin: 17mm 0 15mm !important; }
            .cover { display: none !important; }
        """)
        content.pdf(
            path=str(content_pdf),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            display_header_footer=True,
            header_template=header,
            footer_template=footer,
            margin={"top": "17mm", "right": "0", "bottom": "15mm", "left": "0"},
        )
        browser.close()

    subprocess.run(
        ["pdfunite", str(cover_pdf), str(content_pdf), str(ROOT / "Cloud_Locaweb_Sprint3_Predictfy.pdf")],
        check=True,
    )

print(ROOT / "Cloud_Locaweb_Sprint3_Predictfy.pdf")
