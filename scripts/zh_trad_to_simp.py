"""
Convert the whale flow ZH PDF from Traditional to Simplified Chinese in-place.

For every text span that contains CJK characters:
  1. Convert text via OpenCC (t2s — basic Trad→Simp character mapping).
  2. Redact the original span (fill white).
  3. Re-insert converted text at the same baseline, with matching font/size/color.

Font selection:
  - span.font contains 'Bold' (case-insensitive) → msyhbd.ttc (Microsoft YaHei Bold)
  - otherwise                                     → msyh.ttc   (Microsoft YaHei)
  - DejaVuSans (Latin-only spans) is left untouched.

Font subsetting is applied at the end so the file size stays small.
"""
from __future__ import annotations

import re
import pymupdf
from opencc import OpenCC

PDF = r"C:\Users\siusu\dashboard_website\public\pdfs\onchain\whale_flow_ZH.pdf"

FONT_REG  = r"C:\Windows\Fonts\msyh.ttc"
FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"

# Match any CJK Unified Ideograph or CJK punctuation. (We do NOT want to touch
# spans containing only ASCII / digits / Western punctuation.)
CJK_RE = re.compile(r"[　-〿㐀-䶿一-鿿豈-﫿＀-￯]")


def has_cjk(s: str) -> bool:
    return bool(CJK_RE.search(s))


def int_to_rgb(c: int) -> tuple[float, float, float]:
    return ((c >> 16) & 0xFF) / 255.0, ((c >> 8) & 0xFF) / 255.0, (c & 0xFF) / 255.0


def main() -> None:
    cc = OpenCC("t2s")
    doc = pymupdf.open(PDF)

    total_converted = 0
    for pno, page in enumerate(doc, start=1):
        # 1) Collect spans needing conversion BEFORE applying any redactions.
        jobs: list[dict] = []
        d = page.get_text("dict")
        for block in d.get("blocks", []):
            for line in block.get("lines", []):
                # Capture text direction so we can preserve rotation (e.g.
                # matplotlib y-axis labels rotated 90° upward).
                line_dir = tuple(line.get("dir", (1.0, 0.0)))
                if line_dir == (1.0, 0.0):
                    rotate = 0
                elif line_dir == (0.0, -1.0):
                    rotate = 90        # text reads bottom-to-top
                elif line_dir == (-1.0, 0.0):
                    rotate = 180
                elif line_dir == (0.0, 1.0):
                    rotate = 270       # text reads top-to-bottom
                else:
                    rotate = 0
                for span in line.get("spans", []):
                    txt = span.get("text", "")
                    # Drop the 'Blave' brand reference (with trailing space)
                    cleaned = txt.replace("Blave ", "")
                    if not has_cjk(cleaned) and cleaned == txt:
                        # No CJK and no Blave to remove → skip
                        continue
                    new_txt = cc.convert(cleaned)
                    if new_txt == txt:
                        continue
                    jobs.append({
                        "old":    txt,
                        "new":    new_txt,
                        "bbox":   pymupdf.Rect(span["bbox"]),
                        "size":   span["size"],
                        "color":  int_to_rgb(span["color"]),
                        "font":   span["font"],
                        "bold":   "bold" in span["font"].lower(),
                        "rotate": rotate,
                    })

        if not jobs:
            continue

        print(f"\nPage {pno}: {len(jobs)} spans to convert")

        # 2) Redact every job's bbox.
        #    fill=None → just remove the text, don't draw an overlay rectangle.
        #    This is critical for spans like white text on a dark-navy table
        #    header, where a white overlay would destroy the navy background.
        for j in jobs:
            page.add_redact_annot(j["bbox"], fill=None)
        page.apply_redactions()

        # 3) Re-insert converted text on each redacted span.
        for j in jobs:
            fontfile = FONT_BOLD if j["bold"] else FONT_REG
            internal = "F-yahei-bold" if j["bold"] else "F-yahei"

            if j["rotate"] == 0:
                # Horizontal: place baseline at y1 - 22% of font size (empirically matches)
                baseline_y = j["bbox"].y1 - j["size"] * 0.22
                page.insert_text(
                    (j["bbox"].x0, baseline_y),
                    j["new"],
                    fontname=internal,
                    fontfile=fontfile,
                    fontsize=j["size"],
                    color=j["color"],
                )
            else:
                # Rotated text — use insert_text with rotate.
                # For rotate=90 (reading bottom→top), the baseline runs vertically
                # near the RIGHT edge of the bbox, and the first character starts
                # at the BOTTOM of the bbox.
                bb = j["bbox"]
                size = j["size"]
                if j["rotate"] == 90:
                    point = (bb.x1 - size * 0.22, bb.y1)
                elif j["rotate"] == 270:
                    point = (bb.x0 + size * 0.22, bb.y0)
                elif j["rotate"] == 180:
                    point = (bb.x1, bb.y0 + size * 0.22)
                else:
                    point = (bb.x0, bb.y1 - size * 0.22)
                page.insert_text(
                    point,
                    j["new"],
                    fontname=internal,
                    fontfile=fontfile,
                    fontsize=j["size"],
                    color=j["color"],
                    rotate=j["rotate"],
                )
            total_converted += 1
            preview_old = j["old"][:24].replace("\n", " ")
            preview_new = j["new"][:24].replace("\n", " ")
            marker = "B" if j["bold"] else " "
            rot_tag = f" rot={j['rotate']}" if j["rotate"] else ""
            print(f"  [{marker}] size={j['size']:5.1f}{rot_tag}  {preview_old!r} → {preview_new!r}")

    print(f"\nTotal spans converted: {total_converted}")

    # Subset all embedded fonts so the file doesn't explode in size.
    removed = doc.subset_fonts(verbose=False)
    print(f"subset_fonts: cleaned {removed!r}")

    out_bytes = doc.tobytes(garbage=4, deflate=True)
    doc.close()

    # Sanity-check: confirm no obviously-Traditional chars remain.
    verify = pymupdf.open(stream=out_bytes, filetype="pdf")
    full_text = "\n".join(p.get_text() for p in verify)
    verify.close()

    trad_markers = ["訊號", "鯨魚", "籌碼", "數據", "壓力", "對沖", "資產", "績效", "標的", "頻率", "倉位"]
    leftover = [m for m in trad_markers if m in full_text]
    if leftover:
        print(f"WARNING: Traditional markers still present: {leftover}")
    else:
        print("OK: no Traditional markers remain in text")

    with open(PDF, "wb") as f:
        f.write(out_bytes)
    print(f"Saved → {PDF}")


if __name__ == "__main__":
    main()
