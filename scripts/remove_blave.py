"""
Remove the word 'Blave' from the Whale Flow pitch decks.

Strategy:
  1. Find the line containing 'Blave' on page 6 (one span, MicrosoftYaHei-Bold 17pt).
  2. Redact the whole line (fills with white).
  3. Re-insert the corrected text at the same position using msyhbd.ttc.

EN line:
    'Signal: Blave whale-positioning data (proprietary alpha)'
  becomes
    'Signal: Whale-positioning data (proprietary alpha)'

ZH line (left in Traditional Chinese for consistency with the rest of the deck):
    '訊號來源：Blave 鯨魚籌碼數據（專有 alpha）'
  becomes
    '訊號來源：鯨魚籌碼數據（專有 alpha）'
"""
from __future__ import annotations

import pymupdf

FONT_PATH = r"C:\Windows\Fonts\msyhbd.ttc"  # Microsoft YaHei Bold

PDFS = [
    {
        "path": r"C:\Users\siusu\dashboard_website\public\pdfs\onchain\whale_flow_EN.pdf",
        "old":  "Signal: Blave whale-positioning data (proprietary alpha)",
        "new":  "Signal: Whale-positioning data (proprietary alpha)",
    },
    {
        "path": r"C:\Users\siusu\dashboard_website\public\pdfs\onchain\whale_flow_ZH.pdf",
        "old":  "訊號來源：Blave 鯨魚籌碼數據（專有 alpha）",
        "new":  "訊號來源：鯨魚籌碼數據（專有 alpha）",
    },
]


def int_to_rgb(color_int: int) -> tuple[float, float, float]:
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    return (r / 255.0, g / 255.0, b / 255.0)


def process(path: str, old_text: str, new_text: str) -> None:
    print(f"\n--- {path} ---")
    doc = pymupdf.open(path)

    # Register the Microsoft YaHei Bold font once on each page that needs it.
    found = False
    for pno, page in enumerate(doc, start=1):
        text = page.get_text()
        if "Blave" not in text:
            continue
        found = True

        # Locate the span
        target_span = None
        d = page.get_text("dict")
        for block in d.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    if "Blave" in span.get("text", ""):
                        target_span = span
                        break
                if target_span:
                    break
            if target_span:
                break
        if not target_span:
            print(f"  Page {pno}: 'Blave' in text but no span match; skipping")
            continue

        bbox = pymupdf.Rect(target_span["bbox"])
        size = target_span["size"]
        color = int_to_rgb(target_span["color"])
        print(f"  Page {pno}: redacting {bbox}, size={size}, color={color}")

        # 1) Redact the whole line (fills the rect with white).
        page.add_redact_annot(bbox, fill=(1, 1, 1))
        page.apply_redactions()

        # 2) Re-insert the corrected text on the same baseline.
        #    PyMuPDF insert_text places the text with its BASELINE at the y coord.
        #    A reasonable baseline for size=17 sitting in a bbox of height ~22.5
        #    is bbox.y1 - (size * 0.22) ≈ y1 - 3.74.
        baseline_y = bbox.y1 - size * 0.22
        page.insert_text(
            (bbox.x0, baseline_y),
            new_text,
            fontname="F-yahei-bold",   # arbitrary internal name
            fontfile=FONT_PATH,
            fontsize=size,
            color=color,
        )
        print(f"  Page {pno}: wrote replacement at baseline y={baseline_y:.2f}")

    if not found:
        print("  (no 'Blave' anywhere — nothing to do)")
        doc.close()
        return

    # IMPORTANT: subset embedded fonts before saving. Without this, the full
    # ~10MB Microsoft YaHei Bold (full CJK character set) gets embedded and
    # bloats the PDF by ~25x.
    removed = doc.subset_fonts(verbose=False)
    print(f"  subset_fonts: dropped {removed} unused glyphs")

    # Sanity-check: confirm 'Blave' is gone, 'new_text' is present.
    out_bytes = doc.tobytes(garbage=4, deflate=True)
    doc.close()

    # Verify by reopening from bytes
    verify = pymupdf.open(stream=out_bytes, filetype="pdf")
    full_text = "\n".join(p.get_text() for p in verify)
    if "Blave" in full_text:
        print("  WARNING: 'Blave' still present after edit")
    else:
        print("  OK: 'Blave' no longer found in text")
    if new_text in full_text:
        print("  OK: replacement text present")
    else:
        # Could be split across spans on extraction — search by a fragment instead
        marker = new_text.split(":", 1)[-1].strip()[:10]
        if marker in full_text:
            print(f"  OK: replacement fragment '{marker}' present")
        else:
            print("  WARNING: replacement text NOT found")
    verify.close()

    # Write to original path
    with open(path, "wb") as f:
        f.write(out_bytes)
    print(f"  Saved -> {path}")


def main() -> None:
    for spec in PDFS:
        process(spec["path"], spec["old"], spec["new"])


if __name__ == "__main__":
    main()
