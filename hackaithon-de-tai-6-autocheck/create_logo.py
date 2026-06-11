#!/usr/bin/env python3
"""
create_logo.py - Generate AutoCheck logo (200x200 PNG)
Document + magnifying glass icon with "AutoCheck" text.
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "logo-autocheck.png")
LOGO_SIZE = 200

def create_logo():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    img = Image.new("RGBA", (LOGO_SIZE, LOGO_SIZE), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # ── Document icon (base shape) ──
    doc_color = (0, 102, 204)      # blue #0066CC
    doc_light = (200, 225, 245)    # lighter blue for inner face

    # Document body — rounded rectangle simulation via polygon
    doc_left, doc_top = 30, 25
    doc_w, doc_h = 100, 120

    # Outer document shape
    doc_coords = [
        (doc_left + 8, doc_top),
        (doc_left + doc_w - 8, doc_top),
        (doc_left + doc_w, doc_top + 8),
        (doc_left + doc_w, doc_top + doc_h),
        (doc_left, doc_top + doc_h),
        (doc_left, doc_top + 8),
    ]
    draw.polygon(doc_coords, fill=doc_color, outline=(0, 80, 170), width=2)

    # Inner lighter rectangle (page area)
    inner_margin = 8
    inner_coords = [
        (doc_left + inner_margin + 4, doc_top + inner_margin + 8),
        (doc_left + doc_w - inner_margin - 4, doc_top + inner_margin + 8),
        (doc_left + doc_w - inner_margin - 4, doc_top + doc_h - inner_margin),
        (doc_left + inner_margin + 4, doc_top + doc_h - inner_margin),
    ]
    draw.polygon(inner_coords, fill=doc_light, outline=None)

    # Text lines on document
    line_color = (100, 130, 170)
    for i, y_off in enumerate([30, 44, 58, 72, 86]):
        y = doc_top + y_off
        draw.line(
            [(doc_left + 20, y), (doc_left + doc_w - 20, y)],
            fill=line_color, width=2 if i == 0 else 1,
        )

    # ── Magnifying glass ──
    glass_color = (0, 102, 204)
    glass_light = (180, 210, 240)

    # Glass circle
    circle_cx, circle_cy = 148, 110
    circle_r = 42
    draw.ellipse(
        [circle_cx - circle_r, circle_cy - circle_r,
         circle_cx + circle_r, circle_cy + circle_r],
        outline=glass_color, width=5, fill=(255, 255, 255, 220),
    )

    # Glass highlight (inner lighter circle)
    draw.ellipse(
        [circle_cx - 30, circle_cy - 30,
         circle_cx + 15, circle_cy + 15],
        outline=None, fill=glass_light,
    )

    # Handle
    handle_start_x = circle_cx + int(circle_r * 0.7)
    handle_start_y = circle_cy + int(circle_r * 0.7)
    handle_end_x = handle_start_x + 35
    handle_end_y = handle_start_y + 35
    draw.line(
        [(handle_start_x, handle_start_y), (handle_end_x, handle_end_y)],
        fill=glass_color, width=8,
    )

    # ── "AutoCheck" text at bottom ──
    text = "AutoCheck"
    # Try multiple font sources
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    font = None
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                font = ImageFont.truetype(fp, 22)
            except Exception:
                continue
            break
    if font is None:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (LOGO_SIZE - tw) // 2
    ty = LOGO_SIZE - th - 10
    draw.text((tx, ty), text, fill=doc_color, font=font)

    # Save
    img.save(OUTPUT_PATH, "PNG")
    print(f"Logo saved to {OUTPUT_PATH}  ({LOGO_SIZE}x{LOGO_SIZE})")


if __name__ == "__main__":
    create_logo()
