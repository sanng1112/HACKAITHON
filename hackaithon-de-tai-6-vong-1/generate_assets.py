#!/usr/bin/env python3
"""Generate all asset images for VoiceOne proposal."""
from PIL import Image, ImageDraw, ImageFont
import os

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def get_font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)
    except:
        return ImageFont.load_default()

def create_architecture_diagram():
    W, H = 1600, 1000
    img = Image.new('RGB', (W, H), 'white')
    draw = ImageDraw.Draw(img)
    colors = {
        'user': ('#4CAF50', '#E8F5E9'),
        'ai': ('#2196F3', '#E3F2FD'),
        'process': ('#FF9800', '#FFF3E0'),
        'data': ('#9C27B0', '#F3E5F5'),
    }
    f_title = get_font(24, bold=True)
    f_layer = get_font(16, bold=True)
    f_item = get_font(13)
    f_small = get_font(11)

    draw.text((W//2-200, 15), 'KIẾN TRÚC TỔNG THỂ VOICEONE', fill='#0066CC', font=f_title)

    layers = [
        (80, 100, 1440, 150, 'TẦNG 1 — USER LAYER', 'user',
         ['Kiosk Touchscreen', 'Web App (React/Vue)', 'Mobile App']),
        (80, 280, 1440, 250, 'TẦNG 2 — AI CORE (VNPT APIs)', 'ai',
         ['SmartVoice STT', 'SmartVoice TTS', 'Smartbot NLP', 'eKYC OCR',
          'eKYC Compare', 'eKYC Liveness', 'SmartReader', 'SmartVision']),
        (80, 560, 1440, 150, 'TẦNG 3 — PROCESSING LAYER', 'process',
         ['Voice Gateway', 'Intent Engine', 'Doc Processor', 'Sentiment Analyzer']),
        (80, 740, 1440, 150, 'TẦNG 4 — DATA LAYER', 'data',
         ['PostgreSQL', 'Redis Cache', 'Knowledge Base']),
    ]

    for x, y, w, h, title, key, items in layers:
        bg = colors[key][1]
        border = colors[key][0]
        draw.rounded_rectangle([x, y, x+w, y+h], radius=10, fill=bg, outline=border, width=2)
        draw.rounded_rectangle([x, y, x+w, y+35], radius=10, fill=border)
        draw.rectangle([x, y+20, x+w, y+35], fill=border)
        draw.text((x+15, y+8), title, fill='white', font=f_layer)

        n = len(items)
        for i, item in enumerate(items):
            ix = x + 20 + i * (min(175, (w-40)//n - 8))
            iy = y + 50
            iw = min(170, (w-40)//n - 8)
            draw.rounded_rectangle([ix, iy, ix+iw, iy+70], radius=6, fill='white', outline=border, width=1)
            tb = draw.textbbox((0,0), item, font=f_item)
            tx = ix + (iw - (tb[2]-tb[0]))//2
            draw.text((tx, iy+15), item, fill='#333333', font=f_item)

        if key != 'data':
            draw.line([(W//2, y+h), (W//2, y+h+15)], fill='#666666', width=2)
            draw.polygon([(W//2-8, y+h+15), (W//2+8, y+h+15), (W//2, y+h+25)], fill='#666666')

    path = os.path.join(ASSETS_DIR, 'architecture-diagram.png')
    img.save(path, 'PNG')
    print(f'✅ Architecture diagram: {path} ({W}x{H})')


def create_user_flow():
    W, H = 1400, 900
    img = Image.new('RGB', (W, H), 'white')
    draw = ImageDraw.Draw(img)
    f_title = get_font(22, bold=True)
    f_step = get_font(14, bold=True)
    f_label = get_font(12)

    draw.text((W//2-250, 15), 'LUỒNG NGƯỜI DÙNG VOICEONE', fill='#0066CC', font=f_title)

    # Flow: list of (x, y, text, color, is_diamond)
    nodes = [
        (700, 80, 'Bắt đầu', '#4CAF50', False),
        (700, 200, 'Camera phát hiện\n→ Phát giọng chào', '#2196F3', False),
        (700, 320, 'Người dân nói yêu cầu\n→ STT → Smartbot', '#2196F3', False),
        (400, 450, 'Cần giấy tờ?', '#FF9800', True),
        (1000, 450, 'TTS trả lời\nkết quả', '#2196F3', False),
        (400, 580, 'Hướng dẫn đưa CCCD\n→ Scan → OCR → eKYC', '#2196F3', False),
        (700, 700, 'Xác nhận thông tin\n→ Camera phân tích cảm xúc', '#2196F3', False),
        (700, 820, 'Kết thúc.\nLog phiên giao dịch', '#4CAF50', False),
    ]

    for x, y, text, color, is_diamond in nodes:
        lines = text.split('\n')
        max_lw = max(draw.textbbox((0,0), l, font=f_step)[2] for l in lines)
        th = len(lines) * 22
        bw = max(max_lw + 50, 180)
        bh = max(th + 40, 70)

        if is_diamond:
            # Draw diamond shape
            pts = [(x, y-bh//2), (x+bw//2, y), (x, y+bh//2), (x-bw//2, y)]
            draw.polygon(pts, fill='white', outline=color, width=2)
        else:
            draw.rounded_rectangle([x-bw//2, y-bh//2, x+bw//2, y+bh//2],
                                   radius=12, fill='white', outline=color, width=2)

        for li, line in enumerate(lines):
            lb = draw.textbbox((0,0), line, font=f_step)
            lw = lb[2] - lb[0]
            draw.text((x - lw//2, y - th//2 + li*22), line, fill='#333', font=f_step)

    # Arrows
    arrows = [
        ((700, 115), (700, 165)), ((700, 235), (700, 285)),
        ((700, 355), (530, 415)), ((400, 485), (400, 545)),
        ((400, 615), (700, 665)), ((700, 735), (700, 790)),
        ((830, 415), (960, 440)),
    ]
    for (x1,y1), (x2,y2) in arrows:
        draw.line([(x1,y1),(x2,y2)], fill='#666', width=2)
        mx, my = (x1+x2)//2, (y1+y2)//2
        draw.polygon([(mx-5,my-5),(mx+5,my+5),(mx-5,my+5)], fill='#666')

    draw.text((450, 445), 'Có', fill='#FF9800', font=f_label)
    draw.text((870, 430), 'Không', fill='#4CAF50', font=f_label)

    path = os.path.join(ASSETS_DIR, 'user-flow.png')
    img.save(path, 'PNG')
    print(f'✅ User flow: {path} ({W}x{H})')


def create_wireframe():
    W, H = 1600, 1000
    img = Image.new('RGB', (W, H), '#F5F5F5')
    draw = ImageDraw.Draw(img)
    f_title = get_font(22, bold=True)
    f_hdr = get_font(18, bold=True)
    f_txt = get_font(14)
    f_sm = get_font(12)
    f_xs = get_font(10)
    BLUE = '#2196F3'
    DARK_BLUE = '#0066CC'

    draw.text((W//2-250, 10), 'WIREFRAME GIAO DIỆN VOICEONE', fill=DARK_BLUE, font=f_title)

    def draw_phone(x, y, w, h, title):
        draw.rounded_rectangle([x, y, x+w, y+h], radius=10, fill='white', outline=BLUE, width=2)
        draw.text((x+w//2-80, y+30), title, fill=DARK_BLUE, font=f_hdr)

    # Screen 1: Welcome
    x1, y1 = 40, 60; sw, sh = 500, 900
    draw_phone(x1, y1, sw, sh, 'MÀN HÌNH CHÀO (Kiosk)')
    draw.rounded_rectangle([x1+20, y1+80, x1+sw-20, y1+125], radius=6, fill=DARK_BLUE)
    draw.text((x1+60, y1+92), 'UBND PHƯỜNG [TÊN PHƯỜNG]', fill='white', font=get_font(12, bold=True))

    cx, cy = x1+sw//2, y1+250
    draw.ellipse([cx-55, cy-55, cx+55, cy+55], fill='#E3F2FD', outline=BLUE, width=3)
    draw.rectangle([cx-10, cy-30, cx+10, cy+5], fill=DARK_BLUE)
    draw.line([(cx, cy+5), (cx, cy+20)], fill=DARK_BLUE, width=4)
    draw.arc([cx-16, cy+15, cx+16, cy+35], start=0, end=180, fill=DARK_BLUE, width=3)

    draw.text((x1+70, y1+350), 'Xin chào! Hãy nói yêu cầu của bác ạ', fill='#333', font=f_txt)
    btns = [('Tra cứu thủ tục', BLUE), ('Khai báo hồ sơ', BLUE), ('Hướng dẫn', BLUE)]
    for i, (lbl, clr) in enumerate(btns):
        bx = x1 + 25 + i*160
        draw.rounded_rectangle([bx, y1+430, bx+140, y1+475], radius=8, fill=clr)
        draw.text((bx+8, y1+442), lbl, fill='white', font=get_font(11, bold=True))

    draw.text((x1+100, y1+520), 'VoiceOne v1.0 — Trợ lý giọng nói', fill='#999', font=f_xs)

    # Screen 2: Voice Conversation
    x2, y2 = 570, 60
    draw_phone(x2, y2, sw, sh, 'MÀN HÌNH HỘI THOẠI')
    draw.rounded_rectangle([x2+20, y2+80, x2+sw-20, y2+120], radius=6, fill='#4CAF50')
    draw.text((x2+180, y2+92), '● Đang nghe...', fill='white', font=get_font(15, bold=True))

    wx, wy = x2+sw//2, y2+185
    for i in range(25):
        bh = 8 + (i * 11) % 45
        bx = wx - 120 + i*10
        draw.rectangle([bx, wy-bh//2, bx+6, wy+bh//2], fill=DARK_BLUE)

    draw.text((x2+70, y2+250), '"Tôi muốn làm giấy xác nhận', fill='#333', font=get_font(15, bold=True))
    draw.text((x2+70, y2+280), 'tình trạng hôn nhân"', fill='#333', font=get_font(15, bold=True))

    draw.rounded_rectangle([x2+25, y2+360, x2+sw-25, y2+400], radius=8, fill='#E3F2FD')
    draw.text((x2+45, y2+370), '🤖 Mời bác đưa CCCD vào khay scan ạ', fill=DARK_BLUE, font=f_sm)

    for i, (lbl, clr) in enumerate([('Nói lại', '#FF9800'), ('Xác nhận', '#4CAF50')]):
        bx = x2 + 50 + i*200
        draw.rounded_rectangle([bx, y2+440, bx+160, y2+485], radius=8, fill=clr)
        draw.text((bx+40, y2+452), lbl, fill='white', font=get_font(13, bold=True))

    # Screen 3: Dashboard
    x3, y3 = 1100, 60
    draw_phone(x3, y3, sw, sh, 'DASHBOARD CÁN BỘ')
    draw.rectangle([x3+10, y3+80, x3+85, y3+sh-10], fill='#1A237E')
    icons = '☰📊📁📋⚙'
    for i, ic in enumerate(icons):
        draw.text((x3+35, y3+100+i*80), ic, fill='white', font=get_font(16))

    kpis = [('1,234', 'Tổng GD'), ('45', 'Đang XL'), ('1,189', 'Hoàn thành'), ('92%', 'Hài lòng')]
    for i, (v, l) in enumerate(kpis):
        kx = x3 + 105 + i*100
        draw.rounded_rectangle([kx, y3+85, kx+90, y3+135], radius=6, fill='#E3F2FD', outline=BLUE)
        draw.text((kx+15, y3+90), v, fill=DARK_BLUE, font=get_font(16, bold=True))
        draw.text((kx+15, y3+115), l, fill='#666', font=f_xs)

    draw.rounded_rectangle([x3+105, y3+150, x3+sw-20, y3+280], radius=6, fill='#F9F9F9', outline='#DDD')
    draw.text((x3+280, y3+205), '📈 Biểu đồ xu hướng', fill='#999', font=f_sm)

    draw.rounded_rectangle([x3+105, y3+295, x3+sw-20, y3+480], radius=6, fill='white', outline='#DDD')
    draw.text((x3+120, y3+305), 'Bảng hồ sơ gần đây', fill='#333', font=get_font(13, bold=True))
    for i, h in enumerate(['STT', 'Họ tên', 'Dịch vụ', 'Trạng thái']):
        draw.text((x3+115+i*100, y3+335), h, fill=DARK_BLUE, font=get_font(11, bold=True))
    for r in range(4):
        ry = y3+365+r*25
        draw.line([(x3+110, ry), (x3+sw-25, ry)], fill='#EEE')
        draw.text((x3+125, ry+3), str(r+1), fill='#666', font=f_xs)
        draw.text((x3+165, ry+3), f'Nguyễn Văn...', fill='#333', font=f_xs)
        draw.text((x3+265, ry+3), 'Xác nhận HNT', fill='#333', font=f_xs)
        draw.text((x3+365, ry+3), '✅ Hoàn thành', fill='#4CAF50', font=f_xs)

    path = os.path.join(ASSETS_DIR, 'wireframe-voice-interface.png')
    img.save(path, 'PNG')
    print(f'✅ Wireframe: {path} ({W}x{H})')


if __name__ == '__main__':
    os.makedirs(ASSETS_DIR, exist_ok=True)
    create_architecture_diagram()
    create_user_flow()
    create_wireframe()
    print('🎯 All assets generated successfully!')
