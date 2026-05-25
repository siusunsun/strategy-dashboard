"""Find any rotated text spans in the original ZH PDF."""
import pymupdf

PDF = r"C:\Users\siusu\dashboard_website\backups\whale_flow_ZH.pdf.bak"

doc = pymupdf.open(PDF)
for pno, page in enumerate(doc, start=1):
    d = page.get_text("dict")
    for block in d.get("blocks", []):
        for line in block.get("lines", []):
            ldir = line.get("dir", (1, 0))
            if ldir == (1, 0):
                continue  # horizontal — boring
            for span in line.get("spans", []):
                txt = span.get("text", "")
                if txt.strip():
                    print(f"  p{pno}  dir={ldir}  bbox={span['bbox']}  text={txt!r}")
doc.close()
