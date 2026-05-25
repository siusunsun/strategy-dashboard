"""Render page 6 of both PDFs to PNGs so we can eyeball the result."""
import pymupdf

pdfs = [
    r"C:\Users\siusu\dashboard_website\public\pdfs\onchain\whale_flow_EN.pdf",
    r"C:\Users\siusu\dashboard_website\public\pdfs\onchain\whale_flow_ZH.pdf",
]

for p in pdfs:
    doc = pymupdf.open(p)
    page = doc[5]  # page 6 (0-indexed)
    pix = page.get_pixmap(dpi=150)
    out = p.replace(".pdf", "_page6_preview.png")
    pix.save(out)
    print(f"Wrote {out}")
    # Also print text
    print(page.get_text())
    print("---")
    doc.close()
