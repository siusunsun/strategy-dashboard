"""Render all pages of the ZH PDF as PNGs for visual review."""
import pymupdf
from pathlib import Path

PDF = r"C:\Users\siusu\dashboard_website\public\pdfs\onchain\whale_flow_ZH.pdf"
OUT = Path(r"C:\Users\siusu\dashboard_website\scripts\preview")
OUT.mkdir(exist_ok=True)

doc = pymupdf.open(PDF)
for pno, page in enumerate(doc, start=1):
    pix = page.get_pixmap(dpi=120)
    p = OUT / f"zh_page{pno}.png"
    pix.save(p)
    print(f"wrote {p}")
doc.close()
