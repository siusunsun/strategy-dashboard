"""Inspect 'Blave' occurrences in the whale flow PDFs so we know font/size/bbox."""
import pymupdf  # PyMuPDF
import sys

paths = [
    r"C:\Users\siusu\dashboard_website\public\pdfs\onchain\whale_flow_EN.pdf",
    r"C:\Users\siusu\dashboard_website\public\pdfs\onchain\whale_flow_ZH.pdf",
]

for p in paths:
    print(f"\n=== {p} ===")
    doc = pymupdf.open(p)
    for pno, page in enumerate(doc, start=1):
        text = page.get_text()
        if "Blave" not in text and "blave" not in text:
            continue
        print(f"  Page {pno}: contains Blave")
        # Use dict mode to get span-level info
        d = page.get_text("dict")
        for block in d.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    t = span.get("text", "")
                    if "Blave" in t or "blave" in t:
                        print(f"    SPAN text   : {t!r}")
                        print(f"    SPAN font   : {span.get('font')}  size={span.get('size')}  flags={span.get('flags')}  color={span.get('color')}")
                        print(f"    SPAN bbox   : {span.get('bbox')}")
                        print(f"    LINE bbox   : {line.get('bbox')}")
        # Also: page.search_for, in case the span splits across operators
        print(f"  page.search_for('Blave') -> {page.search_for('Blave')}")
    doc.close()
