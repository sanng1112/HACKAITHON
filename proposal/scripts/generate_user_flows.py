#!/usr/bin/env python3
"""Generate professional user flow diagrams for GovOne proposal."""
import os, math
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Font setup
FONT_PATHS = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
]
_font_path = None
for fp in FONT_PATHS:
    if os.path.exists(fp):
        _font_path = fp
        break

def _font(size=13, bold=False):
    try:
        path = _font_path
        if bold and path:
            bp = path.replace("-Regular", "-Bold")
            if os.path.exists(bp):
                path = bp
        if path:
            return ImageFont.truetype(path, size)
    except:
        pass
    return ImageFont.load_default()

# ── Color palette ──
C_BG = (245, 247, 250)
C_WHITE = (255, 255, 255)
C_DARK = (28, 38, 58)
C_GRAY = (100, 112, 134)
C_LIGHT = (210, 218, 230)

BLUE = (0, 102, 178)
GREEN = (30, 156, 80)
ORANGE = (210, 140, 20)
PURPLE = (120, 60, 180)
TEAL = (0, 140, 120)
RED = (200, 60, 50)

STEP_COLORS = [BLUE, GREEN, ORANGE, PURPLE, TEAL, (180, 80, 60)]

def draw_rounded_rect(draw, xy, r=8, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def draw_arrow_head(draw, x, y, angle, size=8, color=C_GRAY):
    a1 = (x - size * math.cos(angle - 0.5), y - size * math.sin(angle - 0.5))
    a2 = (x - size * math.cos(angle + 0.5), y - size * math.sin(angle + 0.5))
    draw.line([(x, y), a1], fill=color, width=2)
    draw.line([(x, y), a2], fill=color, width=2)

def generate_citizen_flow():
    """Figure 2.1: Modern timeline-style citizen flow diagram."""
    W, H = 1100, 400
    img = Image.new("RGB", (W, H), C_BG)
    draw = ImageDraw.Draw(img)

    # Header bar
    draw_rounded_rect(draw, (0, 0, W, 52), r=0, fill=C_DARK)
    draw.text((W//2, 26), "Hình 2.1: Luồng xử lý của công dân trên GovOne — Từ tương tác đến hoàn tất",
              fill=C_WHITE, font=_font(15, True), anchor="mm")

    steps = [
        ("01", "Chào hỏi\nbằng giọng nói", "Kiosk nhận diện\nvà chào người dùng", BLUE),
        ("02", "Chọn thủ tục\nNói nhu cầu", "Hệ thống phân tích\ný định bằng NLP", GREEN),
        ("03", "OCR + eKYC\nXác thực", "Quét CCCD, so sánh\nkhuôn mặt <30s", ORANGE),
        ("04", "Xác nhận\nbằng giọng nói", "TTS đọc lại thông tin\nchờ xác nhận", PURPLE),
        ("05", "Hoàn tất\nGửi kết quả", "Hồ sơ điện tử\ntự động gửi đến cán bộ", TEAL),
        ("06", "Ghi nhận\nĐo hài lòng", "Sentiment AI phân tích\ntrải nghiệm người dùng", RED),
    ]

    box_w, box_h = 155, 150
    gap = 12
    total_w = len(steps) * box_w + (len(steps) - 1) * gap
    start_x = (W - total_w) // 2
    y_center = 90

    # Connecting line behind boxes
    line_y = y_center + box_h // 2
    draw.line([(start_x + 20, line_y), (start_x + total_w - 20, line_y)],
              fill=C_LIGHT, width=4)

    for i, (num, title, desc, color) in enumerate(steps):
        x = start_x + i * (box_w + gap)

        # Box shadow
        draw_rounded_rect(draw, (x+2, y_center+2, x+box_w+2, y_center+box_h+2), r=10, fill=(0, 0, 0, 20))
        # Box
        draw_rounded_rect(draw, (x, y_center, x+box_w, y_center+box_h), r=10, fill=C_WHITE, outline=color, width=2)

        # Step number circle
        cx, cy = x + box_w//2, y_center + 28
        draw.ellipse([cx-18, cy-18, cx+18, cy+18], fill=color)
        draw.text((cx, cy), num, fill=C_WHITE, font=_font(14, True), anchor="mm")

        # Title
        title_lines = title.split('\n')
        for j, line in enumerate(title_lines):
            draw.text((cx, y_center + 60 + j*16), line, fill=C_DARK, font=_font(12, True), anchor="mm")

        # Description
        desc_lines = desc.split('\n')
        for j, line in enumerate(desc_lines):
            draw.text((cx, y_center + 100 + j*14), line, fill=C_GRAY, font=_font(9), anchor="mm")

        # Arrow connector
        if i < len(steps) - 1:
            ax = x + box_w
            ay = line_y
            draw_arrow_head(draw, ax, ay, 0, color=color)

    # Bottom legend
    legend_items = [
        ("Voice-First", BLUE, "\u0110a k\u00eanh t\u01b0\u01a1ng t\u00e1c"),
        ("AI X\u1eed l\u00fd", GREEN, "T\u1ef1 \u0111\u1ed9ng h\u00f3a"),
        ("X\u00e1c th\u1ef1c", ORANGE, "B\u1ea3o m\u1eadt cao"),
        ("Ph\u00e2n t\u00edch", PURPLE, "Th\u00f4ng minh"),
    ]
    for i, (name, clr, extra) in enumerate(legend_items):
        lx = 110 + i * 245
        ly = H - 45
        draw.ellipse([lx, ly+2, lx+14, ly+16], fill=clr)
        draw.text((lx+22, ly+2), name, fill=C_DARK, font=_font(11, True))
        draw.text((lx+22, ly+18), extra, fill=C_GRAY, font=_font(9))

    path = os.path.join(ASSETS_DIR, "user-flow-citizen.png")
    img.save(path, "PNG")
    print(f"\u2705 Generated: user-flow-citizen.png ({os.path.getsize(path)//1024}KB)")


def generate_officer_flow():
    """Figure 2.2: Professional dashboard-style officer flow."""
    W, H = 1100, 580
    img = Image.new("RGB", (W, H), C_BG)
    draw = ImageDraw.Draw(img)

    # Header
    draw_rounded_rect(draw, (0, 0, W, 50), r=0, fill=C_DARK)
    draw.text((W//2, 25), "Hình 2.2: Quy trình xử lý hồ sơ của cán bộ trên GovOne Dashboard",
              fill=C_WHITE, font=_font(15, True), anchor="mm")

    # ── Row 1: Processing Pipeline ──
    pipeline = [
        ("01", "Hồ sơ mới", "Tiếp nhận tự động t\u1eeb Kiosk/Web/Zalo", BLUE),
        ("02", "AI Auto-Fill", "OCR \u0111i\u1ec1n form, eKYC xác th\u1ef1c", GREEN),
        ("03", "Cán bộ duyệt", "Kiểm tra, ch\u1ec9nh s\u1eeda, xác nh\u1eadn", ORANGE),
        ("04", "X\u1eed lý", "Phê duyệt ho\u1eb7c yêu c\u1ea7u b\u1ed5 sung", PURPLE),
        ("05", "Hoàn tất", "Gửi SMS/Zalo k\u1ebft qu\u1ea3 cho dân", TEAL),
    ]

    pw, ph = 180, 80
    pgap = 18
    total_pw = len(pipeline) * pw + (len(pipeline) - 1) * pgap
    px = (W - total_pw) // 2
    py = 70

    # Pipeline background panel
    draw_rounded_rect(draw, (px-15, py-10, px+total_pw+15, py+ph+15), r=12, fill=C_WHITE)

    for i, (num, title, desc, clr) in enumerate(pipeline):
        x = px + i * (pw + pgap)

        # Box
        draw_rounded_rect(draw, (x, py, x+pw, py+ph), r=8, fill=C_WHITE, outline=clr, width=2)

        # Number badge
        cx = x + pw // 2
        draw.ellipse([cx-14, py-14, cx+14, py+14], fill=clr)
        draw.text((cx, py), num, fill=C_WHITE, font=_font(11, True), anchor="mm")

        # Content
        draw.text((cx, py+26), title, fill=C_DARK, font=_font(12, True), anchor="mm")
        draw.text((cx, py+48), desc, fill=C_GRAY, font=_font(8), anchor="mm")

        # Arrow
        if i < len(pipeline) - 1:
            ax = x + pw
            ay = py + ph // 2 + 8
            draw.line([(ax, ay), (ax + pgap, ay)], fill=clr, width=2)
            draw_arrow_head(draw, ax + pgap, ay, 0, size=6, color=clr)

    # ── Row 2: KPI Metrics ──
    metrics = [
        ("12 h\u1ed3 s\u01a1", "Ch\u1edd x\u1eed lý", BLUE, "+3 hôm nay"),
        ("8 h\u1ed3 s\u01a1", "\u0110ang x\u1eed lý", ORANGE, "5 h\u1ed3 s\u01a1 c\u1ee7a b\u1ea1n"),
        ("6 h\u1ed3 s\u01a1", "\u0110ã x\u1eed lý hôm nay", GREEN, "\u0110\u1ea1t 75% ch\u1ec9 tiêu"),
        ("94%", "T\u1ef7 l\u1ec7 hài lòng", PURPLE, "T\u0103ng 12% so v\u1edbi tháng tr\u01b0\u1edbc"),
    ]

    mw, mh = 230, 100
    mgap = 20
    total_mw = len(metrics) * mw + (len(metrics) - 1) * mgap
    mx = (W - total_mw) // 2

    draw_rounded_rect(draw, (mx-10, py+ph+25-5, mx+total_mw+10, py+ph+25+mh+5), r=12, fill=C_WHITE)

    for i, (val, label, clr, sub) in enumerate(metrics):
        x = mx + i * (mw + mgap)
        # Left accent bar
        draw_rounded_rect(draw, (x, py+ph+25, x+6, py+ph+25+mh), r=3, fill=clr)
        draw.text((x+18, py+ph+30), val, fill=clr, font=_font(22, True))
        draw.text((x+18, py+ph+60), label, fill=C_DARK, font=_font(12, True))
        draw.text((x+18, py+ph+80), sub, fill=C_GRAY, font=_font(9))

    # ── Row 3: Recent Activity ──
    ay0 = py + ph + 25 + mh + 25
    draw_rounded_rect(draw, (mx-10, ay0-5, mx+total_mw+10, ay0+70), r=12, fill=C_WHITE)
    draw.text((mx+10, ay0+8), "Ho\u1ea1t \u0111\u1ed9ng g\u1ea7n \u0111ây", fill=C_DARK, font=_font(12, True))

    activities = [
        ("HS-2024-12345", "C\u1ea5p l\u1ea1i CCCD", "\u0110ã x\u1eed lý", GREEN, "2 phút tr\u01b0\u1edbc"),
        ("HS-2024-12346", "\u0110\u0103ng ký khai sinh", "\u0110ang x\u1eed lý (AI)", BLUE, "15 phút tr\u01b0\u1edbc"),
        ("HS-2024-12348", "\u0110\u0103ng ký k\u1ebft hôn", "\u26a0 C\u1ea3nh báo t\u1ed3n \u0111\u1ecdng", RED, "2 ngày tr\u01b0\u1edbc"),
    ]

    for i, (code, doc_name, status, st_clr, time) in enumerate(activities):
        ay = ay0 + 30 + i * 14
        draw.ellipse([mx+12, ay+2, mx+20, ay+10], fill=st_clr)
        draw.text((mx+28, ay), f"{code} — {doc_name}", fill=C_DARK, font=_font(10))
        draw.text((mx+total_mw-140, ay), status, fill=st_clr, font=_font(10, True))
        draw.text((mx+total_mw-50, ay), time, fill=C_GRAY, font=_font(8))

    # Footer bar
    draw_rounded_rect(draw, (0, H-30, W, H), r=0, fill=C_DARK)
    draw.text((20, H-20), "GovOne Dashboard v1.0 — HackAIthon 2026 (B\u1ea3ng B — Challenger)",
              fill=(150, 170, 190), font=_font(9))
    draw.text((W-240, H-20), "D\u1eef li\u1ec7u th\u1ef1c t\u1ebf · C\u1eadp nh\u1eadt 2 giây tr\u01b0\u1edbc",
              fill=(150, 170, 190), font=_font(9))

    path = os.path.join(ASSETS_DIR, "user-flow-officer.png")
    img.save(path, "PNG")
    print(f"\u2705 Generated: user-flow-officer.png ({os.path.getsize(path)//1024}KB)")


if __name__ == "__main__":
    generate_citizen_flow()
    generate_officer_flow()
