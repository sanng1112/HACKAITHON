#!/usr/bin/env python3
"""Create VoiceOne team logo using Pillow."""

from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    # Create 200x200 RGBA image (transparent background)
    img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    primary = (0, 102, 204)  # #0066CC
    white = (255, 255, 255, 255)
    light_blue = (0, 102, 204, 60)  # semi-transparent for circle bg

    # Draw a circular background (semi-transparent blue circle)
    draw.ellipse([10, 10, 190, 190], fill=light_blue, outline=primary + (255,), width=3)

    # Draw a microphone icon (simplified)
    # Mic body - a rounded rectangle
    mic_color = primary + (255,)
    mic_x, mic_y = 100, 80
    # Mic capsule (rounded rectangle)
    draw.rounded_rectangle([mic_x-18, mic_y-30, mic_x+18, mic_y+10], radius=10, fill=mic_color)
    # Mic grille lines
    for i in range(3):
        y_pos = mic_y - 20 + i * 12
        draw.line([(mic_x-10, y_pos), (mic_x+10, y_pos)], fill=white, width=2)
    # Mic stand (vertical line down)
    draw.line([(mic_x, mic_y+10), (mic_x, mic_y+30)], fill=mic_color, width=4)
    # Mic base (arc)
    draw.arc([mic_x-18, mic_y+25, mic_x+18, mic_y+45], start=0, end=180, fill=mic_color, width=4)
    # Two arms holding the mic
    draw.line([(mic_x-25, mic_y-10), (mic_x-18, mic_y-10)], fill=mic_color, width=3)
    draw.line([(mic_x+18, mic_y-10), (mic_x+25, mic_y-10)], fill=mic_color, width=3)

    # Sound waves (arcs on left and right)
    for offset, radius_offset in [(-30, 10), (-42, 10), (-54, 10)]:
        draw.arc([mic_x+offset, mic_y-15, mic_x+offset+radius_offset, mic_y+15],
                 start=270, end=90, fill=mic_color, width=2)
    for offset, radius_offset in [(20, 10), (32, 10), (44, 10)]:
        draw.arc([mic_x+offset, mic_y-15, mic_x+offset+radius_offset, mic_y+15],
                 start=90, end=270, fill=mic_color, width=2)

    # Text "VoiceOne" below the icon
    try:
        # Try to load a font, fallback to default
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    except (IOError, OSError):
        font = ImageFont.load_default()

    text = "VoiceOne"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_x = (200 - text_w) / 2
    draw.text((text_x, 145), text, fill=mic_color, font=font)

    # Small subtitle text
    try:
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except (IOError, OSError):
        small_font = ImageFont.load_default()

    sub_text = "TRỢ LÝ GIỌNG NÓI"
    sub_bbox = draw.textbbox((0, 0), sub_text, font=small_font)
    sub_w = sub_bbox[2] - sub_bbox[0]
    sub_x = (200 - sub_w) / 2
    draw.text((sub_x, 172), sub_text, fill=(0, 102, 204, 200), font=small_font)

    # Save as PNG
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'logo-team.png')
    img.save(output_path, 'PNG')
    print(f"Logo saved to {output_path}")
    print(f"Image size: {img.size}, Mode: {img.mode}")

if __name__ == '__main__':
    create_logo()
