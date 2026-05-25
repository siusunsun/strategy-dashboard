"""Catalog every text span in the ZH PDF: font, size, weight, color, page."""
import pymupdf
from collections import Counter

PDF = r"C:\Users\siusu\dashboard_website\public\pdfs\onchain\whale_flow_ZH.pdf"

doc = pymupdf.open(PDF)
all_fonts = Counter()
for pno, page in enumerate(doc, start=1):
    d = page.get_text("dict")
    for block in d.get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                txt = span.get("text", "")
                if not txt.strip():
                    continue
                key = (span.get("font"), span.get("size"), span.get("flags"), span.get("color"))
                all_fonts[key] += 1
                # Show a sample first time per key
                if all_fonts[key] == 1:
                    sample = txt[:30].replace('\n', ' ')
                    print(f"  p{pno}  font={span.get('font'):30s}  size={span.get('size'):5.1f}  flags={span.get('flags')}  color=0x{span.get('color'):06X}  sample={sample!r}")

print("\n=== Font totals (sorted by count) ===")
for (font, size, flags, color), count in sorted(all_fonts.items(), key=lambda x: -x[1]):
    print(f"  {count:4d}  font={font:30s}  size={size:5.1f}  flags={flags}  color=0x{color:06X}")
doc.close()
