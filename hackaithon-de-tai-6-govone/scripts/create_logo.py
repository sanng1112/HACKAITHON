#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "logo-govone.png")
LOGO_SIZE = 400
FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]

def get_font(size, bold=True):
    for fp in FONT_PATHS:
        if os.path.exists(fp):
            try: return ImageFont.truetype(fp, size)
            except: continue
    return ImageFont.load_default()

def create_logo():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    img = Image.new("RGBA", (LOGO_SIZE, LOGO_SIZE), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    BLUE = (0, 102, 204); LIGHT_BLUE = (0, 102, 204, 40); WHITE = (255, 255, 255, 255)

    draw.ellipse([20, 20, 380, 380], fill=LIGHT_BLUE, outline=BLUE + (255,), width=4)
    # Document icon
    draw.rounded_rectangle([100, 110, 200, 260], radius=10, fill=BLUE + (255,))
    draw.rounded_rectangle([110, 120, 190, 250], radius=6, fill=(200, 225, 245, 255))
    for i, y_off in enumerate([30, 50, 70, 90]):
        draw.line([(125, 135 + y_off), (175, 135 + y_off)], fill=(100, 130, 170), width=3 if i == 0 else 2)
    # Microphone
    mic_x, mic_y = 260, 170
    draw.rounded_rectangle([mic_x-20, mic_y-35, mic_x+20, mic_y+10], radius=12, fill=BLUE + (255,))
    for i in range(3):
        draw.line([(mic_x-12, mic_y-20+i*12), (mic_x+12, mic_y-20+i*12)], fill=WHITE, width=3)
    draw.line([(mic_x, mic_y+10), (mic_x, mic_y+35)], fill=BLUE + (255,), width=5)
    draw.arc([mic_x-20, mic_y+30, mic_x+20, mic_y+55], start=0, end=180, fill=BLUE + (255,), width=5)
    for offset, radius in [(30, 12), (44, 12), (58, 12)]:
        draw.arc([mic_x+offset, mic_y-15, mic_x+offset+radius, mic_y+15], start=270, end=90, fill=BLUE + (255,), width=3)
    # Text
    font = get_font(36)
    bbox = draw.textbbox((0, 0), "GovOne", font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((LOGO_SIZE - tw) // 2, 310), "GovOne", fill=BLUE + (255,), font=font)
    font_small = get_font(14, bold=False)
    bbox2 = draw.textbbox((0, 0), "Hành chính công thông minh", font=font_small)
    sw = bbox2[2] - bbox2[0]
    draw.text(((LOGO_SIZE - sw) // 2, 355), "Hành chính công thông minh", fill=(0, 102, 204, 200), font=font_small)
    img.save(OUTPUT_PATH, "PNG")
    print(f"✅ Logo saved: {OUTPUT_PATH} ({LOGO_SIZE}x{LOGO_SIZE})")

if __name__ == '__main__':
    create_logo()
