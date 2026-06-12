# Đề tài 6 — Bảng B — Vòng 1: AutoCheck — Hệ thống OCR & Xử lý Hồ sơ Lưu trữ Thông minh

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hoàn thiện bộ hồ sơ ý tưởng Vòng 1 cho **AutoCheck** — hệ thống OCR thông minh để số hóa, xử lý và đối chiếu hồ sơ giấy tờ lưu trữ tại bộ phận một cửa.

**Architecture:** Hệ thống 3 tầng (Scan → AI Processing → Output) tích hợp VNPT SmartReader (OCR bóc tách), VNPT eKYC (xác thực), VNPT SmartVision (phân loại tài liệu) để tự động hóa quy trình số hóa hồ sơ giấy tờ cũ. Backend Python/FastAPI, Database PostgreSQL, Storage MinIO/S3.

**Tech Stack:** VNPT SmartReader (OCR, Doc AI), VNPT eKYC (Liveness, Compare), VNPT SmartVision (Classification), Python FastAPI, PostgreSQL, Redis, MinIO (S3), Docker, GitHub Actions

**Sản phẩm đầu ra:** 01 file PDF hồ sơ ý tưởng (tối đa 15-20 trang) bao gồm:
1. Trang bìa & Thông tin đội thi
2. Đặt vấn đề (Problem Statement)
3. Giải pháp AutoCheck
4. Thiết kế tổng quan (Architecture & Wireframe)
5. Tính khả thi (Feasibility)
6. Tính đổi mới & khác biệt (Innovation)
7. Tác động dự kiến (Impact)
8. Phương hướng triển khai (Roadmap)

**Các API VNPT có thể dùng:** SmartReader (OCR, Doc AI), eKYC (OCR, Liveness, Compare), SmartVision (Classification), vnFace

---

## 📁 Cấu trúc File & Thư mục

```
/run/media/sanng/New Volume/HACKAITHON/
├── docs/superpowers/plans/
│   └── 2026-06-11-hackaithon-de-tai-6-autocheck-vong-1.md   ← Plan này
├── hackaithon-de-tai-6-autocheck/
│   ├── proposal.docx                                          ← File soạn thảo chính
│   ├── proposal.pdf                                           ← File nộp BTC
│   ├── assets/
│   │   ├── architecture-diagram.png                           ← Sơ đồ kiến trúc AutoCheck
│   │   ├── user-flow.png                                      ← Sơ đồ luồng xử lý hồ sơ
│   │   ├── wireframe-scan-interface.png                       ← Wireframe giao diện scan
│   │   ├── wireframe-validation-dashboard.png                 ← Wireframe dashboard xác thực
│   │   └── logo-autocheck.png                                 ← Logo AutoCheck
│   ├── create_proposal.py                                     ← Tạo proposal.docx từ đầu
│   ├── add_section1.py                                        ← Thêm section Đặt vấn đề
│   ├── add_section2.py                                        ← Thêm section Giải pháp
│   ├── add_section3.py                                        ← Thêm section Kiến trúc
│   ├── add_section4.py                                        ← Thêm section Tính khả thi
│   ├── add_section5.py                                        ← Thêm section Đổi mới
│   ├── add_section6.py                                        ← Thêm section Tác động
│   ├── finalize_proposal.py                                   ← Hoàn thiện + Xuất PDF
│   ├── generate_assets.py                                     ← Sinh ảnh assets bằng Pillow
│   ├── create_logo.py                                         ← Tạo logo AutoCheck
│   ├── verify_content.py                                      ← Kiểm tra nội dung proposal
│   └── test_autocheck.py                                      ← Test tự động
```



## 📋 Cấu trúc Hồ sơ Vòng 1 (Bảng B)

| Phần | Nội dung | Điểm tối đa |
|------|----------|:-----------:|
| **1. Trang bìa** | Tên sản phẩm, thông tin đội thi | — |
| **2. Đặt vấn đề & Giải pháp** | Problem statement + solution overview | **25đ** |
| **3. Tính đổi mới & khác biệt** | So sánh với giải pháp hiện có, USP ≥30% | **20đ** |
| **4. Tính khả thi** | Dữ liệu, kỹ thuật, chi phí, pháp lý, lộ trình | **25đ** |
| **5. Tác động dự kiến** | TAM-SAM-SOM, lợi ích, cạnh tranh, doanh thu | **20đ** |
| **6. Chất lượng hồ sơ** | Trình bày logic, sơ đồ, ngôn ngữ rõ ràng | **10đ** |
| **7. Video thuyết minh** (không bắt buộc) | — | — |

---

## 📝 Task 1: Trang bìa & Thông tin đội thi

**File:** `hackaithon-de-tai-6-autocheck/proposal.docx`

- [ ] **Step 1: Tạo script `create_proposal.py` với trang bìa**

```python
#!/usr/bin/env python3
"""Create proposal.docx with cover page for AutoCheck team."""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os


def create_proposal():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)

    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(14)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')

    # Header with logo
    header = section.header
    header.is_linked_to_previous = False
    header_para = header.paragraphs[0]
    header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    logo_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'assets', 'logo-autocheck.png')
    if os.path.exists(logo_path):
        run = header_para.add_run()
        run.add_picture(logo_path, width=Cm(2.54), height=Cm(2.54))

    # Cover page content
    for _ in range(3):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run('')
        run.font.size = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('DỰ THI HACKATHON ĐỔI MỚI SÁNG TẠO 2026')
    run.bold = True
    run.font.size = Pt(20)
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('')
    run.font.size = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(
        'Đề tài 6: Ứng dụng trí tuệ nhân tạo (AI) nhằm nâng cao\n'
        'năng suất xử lý hồ sơ, thủ tục hành chính\ncho cơ quan nhà nước')
    run.font.size = Pt(14)
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')

    # Separator line
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '12')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '0066CC')
    pBdr.append(bottom)
    pPr.append(pBdr)
    run = p.add_run('')
    run.font.size = Pt(14)

    for _ in range(2):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run('')
        run.font.size = Pt(14)

    # Product name
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('AutoCheck')
    run.bold = True
    run.font.size = Pt(24)
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(
        'Hệ thống OCR & Xử lý Hồ sơ Lưu trữ Thông minh')
    run.bold = True
    run.font.size = Pt(16)
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')

    for _ in range(2):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run('')
        run.font.size = Pt(14)

    # Team info
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Bảng thi: Bảng B (Challenger)')
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = 'Times New Roman'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')


- [ ] **Step 3: Tạo thư mục, chạy script tạo logo và proposal**

Run:
```bash
cd /run/media/sanng/New\ Volume/HACKAITHON
mkdir -p hackaithon-de-tai-6-autocheck/assets
python3 hackaithon-de-tai-6-autocheck/create_logo.py
python3 hackaithon-de-tai-6-autocheck/create_proposal.py
```
Expected: `✅ Logo saved to ...` and `✅ Proposal saved to ...`

- [ ] **Step 4: Commit**

```bash
git add hackaithon-de-tai-6-autocheck/
git commit -m "task-1: add cover page, logo and team info for AutoCheck"
```

---

## 📝 Task 2: Đặt vấn đề (Problem Statement)

**File:** `hackaithon-de-tai-6-autocheck/proposal.docx`
**Tiêu chí:** Tính phù hợp đề bài (25đ — chung Task 2 & 3)
**Độ dài:** 2-3 trang

- [ ] **Step 1: Tạo `add_section1.py` với nội dung Đặt vấn đề**

```python
#!/usr/bin/env python3
"""Add section 1. ĐẶT VẤN ĐỀ to AutoCheck proposal."""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

# === HELPER FUNCTIONS (shared pattern) ===

def set_font(run, name='Times New Roman', size=14, bold=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if color:
        run.font.color.rgb = color

def add_page_break(doc):
    p = doc.add_paragraph()
    run = p.add_run()
    run.add_break(WD_BREAK.PAGE)

def add_heading(doc, text, level=1):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    size = {1: 18, 2: 16}.get(level, 14)
    color = RGBColor(0x00, 0x66, 0xCC)
    run = p.add_run(text)
    set_font(run, size=size, bold=True, color=color)
    if level == 1:
        pPr = p._p.get_or_add_pPr()
        pBdr = parse_xml(
            '<w:pBdr %s><w:bottom w:val="single" w:sz="8" '
            'w:space="1" w:color="0066CC"/></w:pBdr>' % nsdecls('w'))
        pPr.append(pBdr)

def add_para(doc, text, indent=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    if indent:
        p.paragraph_format.first_line_indent = Cm(1.27)
    run = p.add_run(text)
    set_font(run, size=14)
    return p

def add_bullet(doc, bold_prefix, normal_text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Cm(1.5)
    p.paragraph_format.line_spacing = 1.5
    run = p.add_run('• ')
    set_font(run, size=14, bold=True)
    run = p.add_run(bold_prefix)
    set_font(run, size=14, bold=True)
    run = p.add_run(normal_text)
    set_font(run, size=14)

def make_table(doc, headers, data):
    table = doc.add_table(rows=1 + len(data), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        set_font(run, size=11, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
        shading = parse_xml(
            '<w:shd %s w:fill="0066CC" w:val="clear"/>' % nsdecls('w'))
        cell._tc.get_or_add_tcPr().append(shading)
    for ri, row_data in enumerate(data):
        for ci, cell_text in enumerate(row_data):
            cell = table.rows[ri + 1].cells[ci]
            cell.text = ''
            p = cell.paragraphs[0]

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    doc_path = os.path.join(script_dir, 'proposal.docx')
    doc = Document(doc_path)

    add_page_break(doc)
    add_heading(doc, '2. GIẢI PHÁP AUTOCHECK')

    add_heading(doc, '2.1 Tổng quan giải pháp', level=2)
    add_para(doc,
        'AutoCheck là một hệ thống OCR thông minh cho phép số hóa hàng loạt hồ sơ '
        'giấy tờ lưu trữ tại các cơ quan nhà nước. Hệ thống sử dụng AI để tự động '
        'nhận dạng, bóc tách thông tin, đối chiếu với cơ sở dữ liệu hiện có, và '
        'đánh giá tính hợp lệ của hồ sơ.')

    add_para(doc,
        'Khác với các giải pháp OCR truyền thống chỉ trích xuất văn bản, AutoCheck '
        'hiểu ngữ cảnh của từng loại giấy tờ (CCCD, sổ hộ khẩu, giấy khai sinh, '
        'bằng cấp...) và tự động điền thông tin vào các trường dữ liệu tương ứng.')

    add_heading(doc, '2.2 Tính năng cốt lõi', level=2)
    make_table(doc,
        ['Tính năng', 'Mô tả', 'Công nghệ VNPT'],
        [
            ['Scan & OCR', 'Scan hồ sơ giấy → OCR nhận dạng → xuất text có cấu trúc',
             'SmartReader (Doc AI)'],
            ['Phân loại tự động', 'AI nhận diện loại giấy tờ → phân loại danh mục',
             'SmartVision (Classification)'],
            ['Bóc tách thông tin', 'Trích xuất họ tên, số CCCD, địa chỉ, ngày tháng...',
             'SmartReader (Entity Extraction)'],
            ['Đối chiếu & Xác thực', 'So sánh thông tin trích xuất với CSDL hiện có',
             'eKYC (Compare)'],
            ['Đánh giá hợp lệ', 'Kiểm tra đầy đủ, phát hiện sai lệch, cảnh báo',
             'SmartReader + AI Rules'],
            ['Xuất báo cáo', 'Tổng hợp kết quả số hóa → Excel/JSON/CSV', '—'],
        ])

    p = doc.add_paragraph()
    set_font(p.add_run(''), size=6)

    add_heading(doc, '2.3 Quy trình xử lý 6 bước', level=2)
    add_para(doc,
        'Quy trình xử lý hồ sơ giấy tờ lưu trữ với AutoCheck gồm 6 bước:', indent=True)
    for b, n in [
        ('Bước 1 — Nạp hồ sơ:', ' Cán bộ đưa hồ sơ giấy vào máy scan hoặc upload file.'),
        ('Bước 2 — Phân loại:', ' SmartVision tự động nhận diện loại giấy tờ.'),
        ('Bước 3 — OCR & Bóc tách:', ' SmartReader OCR nhận dạng, trích xuất các trường.'),
        ('Bước 4 — Đối chiếu:', ' Đối chiếu thông tin với CSDL, đánh dấu sai lệch.'),
        ('Bước 5 — Kiểm tra:', ' Cán bộ xem dashboard, kiểm tra cảnh báo, xác nhận.'),
        ('Bước 6 — Xuất dữ liệu:', ' Dữ liệu xuất ra CSDL, lưu bản scan gốc trên MinIO.'),
    ]:
        add_step(doc, b, n)

    add_heading(doc, '2.4 Vai trò các thành phần AI', level=2)
    add_para(doc, 'AutoCheck sử dụng 5 thành phần AI từ VNPT:', indent=True)
    for b, n in [
        ('SmartReader (OCR): ', 'Nhận dạng chữ tiếng Việt >95%. Hỗ trợ scan, PDF, JPEG.'),
        ('SmartReader (Doc AI): ', 'Bóc tách thông tin có cấu trúc từ giấy tờ.'),
        ('SmartVision (Classification): ', 'Phân loại giấy tờ theo chủng loại.'),
        ('eKYC (Compare): ', 'So sánh thông tin với CSDL, phát hiện sai lệch.'),
        ('eKYC (Liveness): ', 'Kiểm tra ảnh chân dung thật/giả, phát hiện cắt ghép.'),
    ]:
        add_component(doc, b, n)

    doc.save(doc_path)
    print(f'✅ Task 3: Section "Giải pháp" added')

if __name__ == '__main__':
    main()
```

            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(cell_text)
            set_font(run, size=10)
            if ri % 2 == 1:
                shading = parse_xml(
                    '<w:shd %s w:fill="E8F0FE" w:val="clear"/>' % nsdecls('w'))
                cell._tc.get_or_add_tcPr().append(shading)

- [ ] **Step 2: Chạy script**

Run:
```bash
cd /run/media/sanng/New\ Volume/HACKAITHON
python3 hackaithon-de-tai-6-autocheck/add_section2.py
```
Expected: `✅ Task 3: Section "Giải pháp" added`

- [ ] **Step 3: Commit**

```bash
git add hackaithon-de-tai-6-autocheck/add_section2.py hackaithon-de-tai-6-autocheck/proposal.docx
git commit -m "task-3: add AutoCheck solution with core features, 6-step process and AI components"
```

---

## 📝 Task 4: Thiết kế tổng quan (Architecture & Wireframe)

**Files:**
- `hackaithon-de-tai-6-autocheck/proposal.docx`
- `hackaithon-de-tai-6-autocheck/assets/architecture-diagram.png`
- `hackaithon-de-tai-6-autocheck/assets/user-flow.png`
- `hackaithon-de-tai-6-autocheck/assets/wireframe-scan-interface.png`
- `hackaithon-de-tai-6-autocheck/assets/wireframe-validation-dashboard.png`

- [ ] **Step 1: Tạo `generate_assets.py` sinh 4 ảnh assets**

    layers = [
        (80, 100, 1440, 150, 'TẦNG 1 — INPUT', 'input',
         ['Máy Scan thường', 'Máy Scan ống ADF', 'Upload PDF/JPEG', 'Camera chụp']),
        (80, 300, 1440, 220, 'TẦNG 2 — AI PROCESSING (VNPT APIs)', 'ai',
         ['SmartReader OCR', 'SmartReader Doc AI', 'SmartVision Classify',
          'eKYC Compare', 'eKYC Liveness', 'AI Rules Engine']),
        (80, 570, 1440, 120, 'TẦNG 3 — OUTPUT & STORAGE', 'output',
         ['PostgreSQL', 'MinIO/S3 (scan gốc)', 'Redis Cache']),
    ]

    for x, y, w, h, title, key, items in layers:
        bg = colors[key][1]; border = colors[key][0]
        draw.rounded_rectangle([x, y, x+w, y+h], radius=10, fill=bg, outline=border, width=2)
        draw.rounded_rectangle([x, y, x+w, y+35], radius=10, fill=border)
        draw.rectangle([x, y+20, x+w, y+35], fill=border)
        draw.text((x+15, y+8), title, fill='white', font=f_layer)
        n = len(items)
        for i, item in enumerate(items):
            ix = x + 20 + i * (min(200, (w-40)//n - 8))
            iy = y + 50; iw = min(195, (w-40)//n - 8)
            draw.rounded_rectangle([ix, iy, ix+iw, iy+65], radius=6, fill='white', outline=border, width=1)
            tb = draw.textbbox((0, 0), item, font=f_item)
            draw.text((ix + (iw - (tb[2]-tb[0]))//2, iy+12), item, fill='#333', font=f_item)

    for y_pos in [250, 520]:
        draw.line([(W//2, y_pos), (W//2, y_pos+30)], fill='#666', width=2)
        draw.polygon([(W//2-8, y_pos+30), (W//2+8, y_pos+30), (W//2, y_pos+40)], fill='#666')

    path = os.path.join(ASSETS_DIR, 'architecture-diagram.png')
    img.save(path, 'PNG')
    print(f'✅ Architecture diagram: {path}')


```python
#!/usr/bin/env python3
"""Generate all asset images for AutoCheck proposal."""
from PIL import Image, ImageDraw, ImageFont
import os


def create_user_flow():
    W, H = 1400, 900
    img = Image.new('RGB', (W, H), 'white')
    draw = ImageDraw.Draw(img)
    f_title = get_font(22, bold=True)
    f_step = get_font(14, bold=True)
    draw.text((W//2-250, 15), 'LUỒNG XỬ LÝ HỒ SƠ AUTOCHECK', fill='#0066CC', font=f_title)
    nodes = [
        (700, 80, 'Cán bộ nạp hồ sơ', '#4CAF50', False),
        (400, 200, 'Scan tài liệu', '#2196F3', False),
        (1000, 200, 'Upload file số', '#2196F3', False),
        (700, 320, 'SmartVision:\nPhân loại giấy tờ', '#FF9800', False),
        (700, 440, 'SmartReader:\nOCR & Bóc tách', '#2196F3', False),
        (400, 560, 'Đối chiếu CSDL\neKYC Compare', '#FF9800', True),
        (1000, 560, 'AI Rules:\nKiểm tra hợp lệ', '#FF9800', True),
        (700, 700, 'Dashboard:\nCán bộ kiểm tra', '#2196F3', False),
        (700, 820, 'Xuất dữ liệu\n+ Lưu scan gốc', '#4CAF50', False),
    ]
    for x, y, text, color, is_diamond in nodes:
        lines = text.split('\n')
        max_lw = max(draw.textbbox((0,0), l, font=f_step)[2] for l in lines)
        th = len(lines) * 22; bw = max(max_lw + 50, 180); bh = max(th + 40, 70)
        if is_diamond:
            pts = [(x, y-bh//2), (x+bw//2, y), (x, y+bh//2), (x-bw//2, y)]
            draw.polygon(pts, fill='white', outline=color, width=2)
        else:
            draw.rounded_rectangle([x-bw//2, y-bh//2, x+bw//2, y+bh//2], radius=12, fill='white', outline=color, width=2)
        for li, line in enumerate(lines):
            lb = draw.textbbox((0,0), line, font=f_step)
            lw = lb[2] - lb[0]
            draw.text((x - lw//2, y - th//2 + li*22), line, fill='#333', font=f_step)
    arrows = [((700,115),(520,165)),((700,115),(880,165)),((400,235),(700,285)),((1000,235),(700,285)),
              ((700,355),(700,405)),((700,475),(520,528)),((700,475),(880,528)),((400,595),(700,665)),
              ((1000,595),(700,665)),((700,735),(700,785))]
    for (x1,y1),(x2,y2) in arrows:
        draw.line([(x1,y1),(x2,y2)], fill='#666', width=2)
    path = os.path.join(ASSETS_DIR, 'user-flow.png')
    img.save(path, 'PNG')
    print(f'✅ User flow: {path}')

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def get_font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)
    except:
        return ImageFont.load_default()

def create_architecture_diagram():
    W, H = 1600, 800
    img = Image.new('RGB', (W, H), 'white')
    draw = ImageDraw.Draw(img)
    colors = {
        'input': ('#4CAF50', '#E8F5E9'),
        'ai': ('#2196F3', '#E3F2FD'),
        'output': ('#9C27B0', '#F3E5F5'),
    }
    f_title = get_font(22, bold=True)
    f_layer = get_font(16, bold=True)
    f_item = get_font(13)
    draw.text((W//2-180, 15), 'KIẾN TRÚC TỔNG THỂ AUTOCHECK',
              fill='#0066CC', font=f_title)


def create_wireframes():
    W, H = 1600, 1000
    img = Image.new('RGB', (W, H), '#F5F5F5')
    draw = ImageDraw.Draw(img)
    f_title = get_font(22, bold=True)
    f_hdr = get_font(18, bold=True)
    f_txt = get_font(14); f_sm = get_font(12); f_xs = get_font(10)
    BLUE = '#2196F3'; DARK_BLUE = '#0066CC'

    draw.text((W//2-200, 10), 'WIREFRAME GIAO DIỆN AUTOCHECK', fill=DARK_BLUE, font=f_title)

    # --- Screen 1: Validation Dashboard ---
    x1, y1 = 30, 50; sw, sh = 760, 920
    draw.rounded_rectangle([x1, y1, x1+sw, y1+sh], radius=10, fill='white', outline=BLUE, width=2)
    draw.text((x1+200, y1+15), 'DASHBOARD KIỂM TRA & XÁC THỰC', fill=DARK_BLUE, font=f_hdr)

    stats = [('1,234', 'Đã xử lý'), ('12', 'Cảnh báo'), ('3', 'Lỗi'), ('98.5%', 'Chính xác')]
    for i, (v, l) in enumerate(stats):
        sx = x1 + 20 + i * 180
        draw.rounded_rectangle([sx, y1+60, sx+170, y1+110], radius=6, fill='#E3F2FD', outline=BLUE)
        draw.text((sx+10, y1+67), v, fill=DARK_BLUE, font=get_font(18, bold=True))
        draw.text((sx+10, y1+92), l, fill='#666', font=f_xs)

    hdrs = ['STT', 'Loại hồ sơ', 'Ngày', 'Trạng thái', 'Kết quả']
    cw = [40, 150, 120, 120, 120]
    cx = x1 + 20
    draw.rounded_rectangle([cx, y1+140, cx+sw-40, y1+175], radius=4, fill=DARK_BLUE)
    for i, h in enumerate(hdrs):
        draw.text((cx+10+sum(cw[:i]), y1+150), h, fill='white', font=get_font(12, bold=True))
    rows = [['1','CCCD','10/06','✅ Đã XN','Khớp 100%'],['2','Sổ hộ khẩu','10/06','⚠️ Cảnh báo','Sai địa chỉ'],
            ['3','Giấy khai sinh','10/06','✅ Đã XN','Khớp 100%'],['4','Bằng TN','09/06','❌ Lỗi','Thiếu ảnh'],
            ['5','CCCD','09/06','✅ Đã XN','Khớp 100%']]
    for ri, row in enumerate(rows):
        ry = y1 + 185 + ri * 30
        draw.line([(cx, ry+28), (cx+sw-40, ry+28)], fill='#EEE')
        for ci, val in enumerate(row):
            draw.text((cx+10+sum(cw[:ci]), ry+4), val, fill='#333', font=f_xs)

    draw.rounded_rectangle([cx, y1+340, cx+sw-40, y1+520], radius=6, fill='#FFFDE7', outline='#FF9800')
    draw.text((cx+15, y1+350), '⚠️ Chi tiết cảnh báo (Hồ sơ #2)', fill='#FF9800', font=get_font(13, bold=True))
    for i, w in enumerate(['• Họ tên: Nguyễn Văn A (hồ sơ) ≠ Nguyễn Văn B (CSDL)',
                           '• Địa chỉ: 123 Lê Lợi (hồ sơ) ≠ 124 Lê Lợi (CSDL)',
                           '• Gợi ý: Kiểm tra lại bản scan hoặc đối chiếu bản gốc']):
        draw.text((cx+15, y1+390+i*25), w, fill='#333', font=f_xs)

    path = os.path.join(ASSETS_DIR, 'wireframe-validation-dashboard.png')
    img.save(path, 'PNG')
    print(f'✅ Wireframe dashboard: {path}')

    # --- Screen 2: Scan Interface (separate image) ---
    img2 = Image.new('RGB', (800, 920), '#F5F5F5')
    draw2 = ImageDraw.Draw(img2)
    draw2.rounded_rectangle([5, 5, 795, 915], radius=10, fill='white', outline=BLUE, width=2)
    draw2.text((250, 20), 'MÀN HÌNH SCAN HỒ SƠ', fill=DARK_BLUE, font=get_font(16, bold=True))
    draw2.rounded_rectangle([30, 55, 770, 250], radius=8, fill='#F0F0F0', outline='#CCC')
    draw2.text((300, 130), '📄 Khu vực scan', fill='#999', font=f_txt)
    draw2.rectangle([150, 160, 650, 180], fill=DARK_BLUE)
    draw2.text((200, 162), '📂 Kéo thả file hoặc scan trực tiếp', fill='white', font=f_xs)

    for i, (lbl, clr) in enumerate([('Scan từ máy', BLUE), ('Tải file lên', BLUE), ('Scan ống', '#FF9800')]):
        draw2.rounded_rectangle([40+i*240, 280, 260+i*240, 320], radius=6, fill=clr)
        draw2.text((50+i*240, 290), lbl, fill='white', font=get_font(13, bold=True))

    draw2.rounded_rectangle([30, 350, 770, 450], radius=6, fill='#F9F9F9', outline='#DDD')
    for i, s in enumerate(['Loại giấy tờ: ▾Tự động phát hiện', 'Độ phân giải: 300 DPI', 'Định dạng: JSON + PDF/A']):
        draw2.text((50, 370+i*25), s, fill='#666', font=f_xs)
    draw2.rounded_rectangle([30, 480, 770, 650], radius=6, fill='#F0F0F0', outline='#DDD')
    draw2.text((300, 550), '📄 Preview bản scan', fill='#999', font=f_sm)

    for i, (lbl, clr) in enumerate([('Xử lý OCR', '#4CAF50'), ('Lưu nháp', '#FF9800'), ('Hủy', '#F44336')]):
        draw2.rounded_rectangle([40+i*240, 680, 260+i*240, 720], radius=6, fill=clr)
        draw2.text((50+i*240, 690), lbl, fill='white', font=get_font(13, bold=True))

    path2 = os.path.join(ASSETS_DIR, 'wireframe-scan-interface.png')
    img2.save(path2, 'PNG')
    print(f'✅ Wireframe scan interface: {path2}')

if __name__ == '__main__':
    os.makedirs(ASSETS_DIR, exist_ok=True)
    create_architecture_diagram()
    create_user_flow()
    create_wireframes()
    print('🎯 All AutoCheck assets generated successfully!')
```



- [ ] **Step 2: Chạy script sinh assets**

Run:
```bash
cd /run/media/sanng/New\ Volume/HACKAITHON
python3 hackaithon-de-tai-6-autocheck/generate_assets.py
```
Expected: 4 ảnh PNG trong `assets/`

- [ ] **Step 3: Tạo `add_section3.py` với nội dung Kiến trúc**

```python
#!/usr/bin/env python3
"""Add section 3. Architecture to AutoCheck proposal."""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

def set_font(run, name='Times New Roman', size=14, bold=False, color=None):
    run.font.name = name; run.font.size = Pt(size); run.bold = bold
    run.element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if color: run.font.color.rgb = color

def add_page_break(doc):
    p = doc.add_paragraph(); run = p.add_run(); run.add_break(WD_BREAK.PAGE)

def add_heading(doc, text, level=1):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    sz = {1: 18, 2: 16}.get(level, 14)
    run = p.add_run(text)
    set_font(run, size=sz, bold=True, color=RGBColor(0x00, 0x66, 0xCC))
    if level == 1:
        pPr = p._p.get_or_add_pPr()
        pBdr = parse_xml(
            '<w:pBdr %s><w:bottom w:val="single" w:sz="8" '
            'w:space="1" w:color="0066CC"/></w:pBdr>' % nsdecls('w'))
        pPr.append(pBdr)

def add_para(doc, text, indent=True):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    if indent: p.paragraph_format.first_line_indent = Cm(1.27)
    run = p.add_run(text); set_font(run, size=14); return p

def add_image(doc, img_path, width_cm=15, caption=None):
    if os.path.exists(img_path):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(); run.add_picture(img_path, width=Cm(width_cm))
        if caption:
            p2 = doc.add_paragraph(); p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run2 = p2.add_run(caption)
            set_font(run2, size=11, bold=True, color=RGBColor(0x66, 0x66, 0x66))

def add_layer(doc, b, n):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Cm(1.0); p.paragraph_format.line_spacing = 1.5
    run = p.add_run(b); set_font(run, size=13, bold=True)
    run = p.add_run(n); set_font(run, size=13)

def add_bullet(doc, text):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Cm(1.5); p.paragraph_format.line_spacing = 1.5
    run = p.add_run('• '); set_font(run, size=13)
    run = p.add_run(text); set_font(run, size=13)

def main():
    sd = os.path.dirname(os.path.abspath(__file__))
    doc = Document(os.path.join(sd, 'proposal.docx'))
    ad = os.path.join(sd, 'assets')
    add_page_break(doc)
    add_heading(doc, '3. THIẾT KẾ TỔNG QUAN')
    add_heading(doc, '3.1 Kiến trúc hệ thống', level=2)
    add_para(doc,
        'AutoCheck được thiết kế theo mô hình 3 tầng, tối ưu cho việc xử lý '
        'hàng loạt hồ sơ giấy tờ lưu trữ. Kiến trúc đảm bảo tính mở rộng và '
        'khả năng xử lý song song.')
    for b, n in [
        ('Tầng 1 — Input Layer:', ' Tiếp nhận từ máy scan, upload PDF/JPEG, camera.'),
        ('Tầng 2 — AI Processing:', ' SmartReader OCR, SmartVision Classify, eKYC, AI Rules.'),
        ('Tầng 3 — Output & Storage:', ' PostgreSQL, MinIO/S3, Redis.'),
    ]:
        add_layer(doc, b, n)

    arch_img = os.path.join(ad, 'architecture-diagram.png')
    add_image(doc, arch_img, width_cm=16,
              caption='Figure 1: Sơ đồ kiến trúc tổng thể AutoCheck')

    add_heading(doc, '3.2 Giao diện người dùng', level=2)
    add_para(doc,
        'AutoCheck có 2 giao diện chính: Màn hình Scan (nhập liệu) và Dashboard '
        'Kiểm tra & Xác thực (dành cho cán bộ một cửa).')
    add_bullet(doc, 'Màn hình Scan: Kéo thả file, chọn nguồn scan, cài đặt, xem preview.')
    add_bullet(doc, 'Dashboard: Thống kê, danh sách hồ sơ, chi tiết cảnh báo sai lệch.')

    scan_img = os.path.join(ad, 'wireframe-scan-interface.png')
    add_image(doc, scan_img, width_cm=14, caption='Figure 2: Giao diện Scan')
    userflow_img = os.path.join(ad, 'user-flow.png')
    add_image(doc, userflow_img, width_cm=16, caption='Figure 3: Luồng xử lý')
    dash_img = os.path.join(ad, 'wireframe-validation-dashboard.png')
    add_image(doc, dash_img, width_cm=16, caption='Figure 4: Dashboard xác thực')

    add_heading(doc, '3.3 Quy trình xử lý dữ liệu', level=2)
    add_para(doc,
        'Pipeline: Scan → Phân loại (SmartVision) → OCR & Bóc tách (SmartReader) '
        '→ Đối chiếu (eKYC) → Kiểm tra (AI Rules) → Xuất dữ liệu. '
        'Mỗi bước có log chi tiết phục vụ kiểm tra.')

    doc.save(os.path.join(sd, 'proposal.docx'))
    print(f'✅ Task 4: Section "Architecture & Wireframe" added')

if __name__ == '__main__':
    main()
```

- [ ] **Step 4: Chạy script sinh assets và section 3**

Run:
```bash
cd /run/media/sanng/New\ Volume/HACKAITHON
python3 hackaithon-de-tai-6-autocheck/generate_assets.py
python3 hackaithon-de-tai-6-autocheck/add_section3.py
```
Expected: 4 ảnh PNG + section 3 added

- [ ] **Step 5: Commit**

```bash
git add hackaithon-de-tai-6-autocheck/
git commit -m "task-4: add architecture diagram, user flow, wireframes and architecture section for AutoCheck"
```

---

## 📝 Task 5: Tính khả thi (Feasibility)

**File:** `hackaithon-de-tai-6-autocheck/proposal.docx`
**Tiêu chí:** Tính khả thi (25đ) | **Độ dài:** 2 trang

- [ ] **Step 1: Tạo `add_section4.py` với nội dung Tính khả thi**

```python
#!/usr/bin/env python3
"""Add section 4. TÍNH KHẢ THI to AutoCheck proposal."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

def sf(run, n='Times New Roman', s=14, b=False, c=None):
    run.font.name = n; run.font.size = Pt(s); run.bold = b
    run.element.rPr.rFonts.set(qn('w:eastAsia'), n)
    if c: run.font.color.rgb = c

def apb(doc):
    p = doc.add_paragraph(); r = p.add_run(); r.add_break(WD_BREAK.PAGE)

def ah(doc, t, lv=1):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    sz = {1: 18, 2: 16, 3: 14}.get(lv, 14)
    r = p.add_run(t); sf(r, s=sz, b=True, c=RGBColor(0x00, 0x66, 0xCC))
    if lv == 1:
        pPr = p._p.get_or_add_pPr()
        pBdr = parse_xml('<w:pBdr %s><w:bottom w:val="single" w:sz="8" w:space="1" w:color="0066CC"/></w:pBdr>' % nsdecls('w'))
        pPr.append(pBdr)

def ap(doc, t, ind=True):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    if ind: p.paragraph_format.first_line_indent = Cm(1.27)

def main():
    sd = os.path.dirname(os.path.abspath(__file__))
    doc = Document(os.path.join(sd, 'proposal.docx'))
    apb(doc); ah(doc, '4. TÍNH KHẢ THI')

    ah(doc, '4.1 Nguồn dữ liệu', 2)
    ap(doc, 'AutoCheck sử dụng dữ liệu từ nhiều nguồn:')
    mt(doc, ['Yếu tố', 'Mô tả'], [
        ['Hồ sơ giấy lưu trữ', 'Có sẵn tại UBND, mỗi phường ~50.000-200.000 hồ sơ.'],
        ['Dữ liệu huấn luyện', 'VNPT SmartReader đã huấn luyện sẵn tiếng Việt.'],
        ['CSDL đối chiếu', 'Cổng DVC Quốc gia, CSDL Quốc gia về dân cư.'],
    ])
    p = doc.add_paragraph(); sf(p.add_run(''), size=6)

    ah(doc, '4.2 Nhân lực', 2)
    mt(doc, ['Vai trò', 'SL', 'Kỹ năng chính'], [
        ['Project Manager', '1', 'Agile/Scrum'],
        ['AI/OCR Developer', '2', 'Python, OCR, Xử lý ảnh'],
        ['Fullstack Developer', '1', 'React, FastAPI, PostgreSQL, Docker'],
        ['UI/UX Designer', '1', 'Figma'],
        ['Business Analyst', '1', 'Nghiệp vụ lưu trữ, một cửa'],
    ])
    p = doc.add_paragraph(); sf(p.add_run(''), size=6)

    ah(doc, '4.3 Kiến trúc kỹ thuật', 2)
    ap(doc, 'Frontend: React + TypeScript. Backend: Python FastAPI. '
        'AI: VNPT API. Database: PostgreSQL, MinIO/S3, Redis. DevOps: Docker, CI/CD.')

    ah(doc, '4.4 Kế hoạch MVP 7 ngày (Vòng 2)', 2)
    mt(doc, ['Ngày', 'Công việc', 'Kết quả'], [
        ['1-2', 'Setup + SmartReader OCR', 'OCR ảnh → text'],
        ['3-4', 'SmartVision + eKYC', 'Phân loại + đối chiếu'],
        ['5-6', 'UI Scan + Dashboard', 'Giao diện hoàn chỉnh'],
        ['7', 'E2E test + Fix + Đóng gói', 'MVP deploy được'],
    ])
    p = doc.add_paragraph(); sf(p.add_run(''), size=6)

    ah(doc, '4.5 Chi phí vận hành', 2)
    mt(doc, ['Hạng mục', 'VNĐ/tháng', 'Ghi chú'], [
        ['Server (2 VPS 8GB)', '~2.000.000', 'AWS/VNPT Cloud'],
        ['API VNPT', '~1.000.000-3.000.000', 'Tùy số lượng hồ sơ'],
        ['MinIO/S3 Storage', '~500.000', 'Lưu scan + dữ liệu'],
        ['Domain + SSL', '~200.000', '.gov.vn'],
        ['DevOps tools', 'Miễn phí', 'GitHub/Docker Free'],
        ['Tổng', '~3.700.000-5.700.000', '~$150-230/tháng'],
    ])
    ap(doc, 'Chi phí setup: 20-30 triệu (máy scan ống). Tiết kiệm ~60% so với nhân công.')

    ah(doc, '4.6 An toàn bảo mật & Pháp lý', 2)
    mt(doc, ['Yêu cầu', 'Giải pháp'], [
        ['Bảo vệ dữ liệu CN', 'Nghị định 13/2023 — AES-256, TLS 1.3'],
        ['Số hóa tài liệu', 'Thông tư 01/2019/TT-BNV'],
        ['An toàn TT', 'Luật ATTT 2015 — Audit log'],
        ['Lưu trữ số', 'Luật Lưu trữ 2011'],
    ])
    p = doc.add_paragraph(); sf(p.add_run(''), size=6)

    ah(doc, '4.7 Lộ trình phát triển', 2)
    for b, n in [
        ('Tháng 1-2:', ' MVP → Pilot 1 phường, 5.000 hồ sơ'),
        ('Tháng 3-4:', ' Feedback → Scale 5-10 quận/huyện'),
        ('Tháng 5-6:', ' Tích hợp CSDL QG → Mở rộng loại giấy tờ'),
        ('Tháng 7-12:', ' Triển khai diện rộng → Hợp tác VNPT'),
    ]:
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.left_indent = Cm(1.0); p.paragraph_format.line_spacing = 1.5
        r = p.add_run(b); sf(r, s=13, b=True)
        r = p.add_run(n); sf(r, s=13)
    doc.save(os.path.join(sd, 'proposal.docx'))
    print(f'✅ Task 5: Section "Tính khả thi" added')

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Chạy script và commit**

Run:
```bash
cd /run/media/sanng/New\ Volume/HACKAITHON
python3 hackaithon-de-tai-6-autocheck/add_section4.py
git add hackaithon-de-tai-6-autocheck/add_section4.py hackaithon-de-tai-6-autocheck/proposal.docx
git commit -m "task-5: add feasibility with data, team, costs, compliance, roadmap"
```

    r = p.add_run(t); sf(r); return p

def mt(doc, hd, data):
    t = doc.add_table(rows=1+len(data), cols=len(hd))

---

## 📝 Task 6: Tính đổi mới & Khác biệt (Innovation)

**File:** `hackaithon-de-tai-6-autocheck/proposal.docx`
**Tiêu chí:** Tính đổi mới & khác biệt (20đ) | **Độ dài:** 1.5 trang

- [ ] **Step 1: Tạo `add_section5.py` với nội dung Đổi mới & Khác biệt**

```python
#!/usr/bin/env python3
"""Add section 5. ĐỔI MỚI & KHÁC BIỆT to AutoCheck proposal."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

def sf(run, n='Times New Roman', s=14, b=False, c=None):
    run.font.name = n; run.font.size = Pt(s); run.bold = b
    run.element.rPr.rFonts.set(qn('w:eastAsia'), n)
    if c: run.font.color.rgb = c

def apb(doc):
    p = doc.add_paragraph(); r = p.add_run(); r.add_break(WD_BREAK.PAGE)

def ah(doc, t, lv=1):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    sz = {1: 18, 2: 16, 3: 14}.get(lv, 14)
    r = p.add_run(t); sf(r, s=sz, b=True, c=RGBColor(0x00, 0x66, 0xCC))
    if lv == 1:
        pPr = p._p.get_or_add_pPr()
        pBdr = parse_xml('<w:pBdr %s><w:bottom w:val="single" w:sz="8" w:space="1" w:color="0066CC"/></w:pBdr>' % nsdecls('w'))
        pPr.append(pBdr)

def ap(doc, t, ind=True):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    if ind: p.paragraph_format.first_line_indent = Cm(1.27)
    r = p.add_run(t); sf(r); return p

def mt(doc, hd, data):
    t = doc.add_table(rows=1+len(data), cols=len(hd))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.style = 'Table Grid'
    for i, h in enumerate(hd):
        c = t.rows[0].cells[i]; c.text = ''; p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER; r = p.add_run(h)
        sf(r, s=11, b=True, c=RGBColor(0xFF,0xFF,0xFF))
        c._tc.get_or_add_tcPr().append(parse_xml('<w:shd %s w:fill="0066CC" w:val="clear"/>' % nsdecls('w')))
    for ri, rd in enumerate(data):
        for ci, ct in enumerate(rd):
            c = t.rows[ri+1].cells[ci]; c.text = ''; p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT; r = p.add_run(ct); sf(r, s=10)
            if ri % 2 == 1:
                c._tc.get_or_add_tcPr().append(parse_xml('<w:shd %s w:fill="E8F0FE" w:val="clear"/>' % nsdecls('w')))

def main():
    sd = os.path.dirname(os.path.abspath(__file__))
    doc = Document(os.path.join(sd, 'proposal.docx'))
    apb(doc); ah(doc, '5. TÍNH ĐỔI MỚI & KHÁC BIỆT')

    ah(doc, '5.1 So sánh với giải pháp hiện tại', 2)
    ap(doc, 'So sánh AutoCheck với các giải pháp số hóa tài liệu hiện có:')
    mt(doc, ['Tiêu chí', 'Giải pháp hiện tại', 'AutoCheck'], [
        ['Tốc độ xử lý', '30-60 phút/hồ sơ (thủ công)', '2-5 phút (AI, nhanh 10-15x)'],
        ['Độ chính xác', 'Phụ thuộc tay nghề', '>95% (AI OCR + đối chiếu)'],
        ['Phân loại', 'Thủ công', 'AI tự động (SmartVision)'],
        ['Bóc tách', 'Nhập liệu thủ công', 'AI tự động, có cấu trúc'],
        ['Đối chiếu CSDL', 'Tra cứu thủ công', 'AI tự động, real-time'],
        ['Phát hiện sai lệch', 'Mắt thường', 'AI tự động + cảnh báo'],
        ['Lưu trữ', 'Kho giấy', 'Số hóa, backup, tìm kiếm nhanh'],
    ])
    ap(doc, 'AutoCheck vượt trội 7/7 tiêu chí (~100% khác biệt), vượt xa ngưỡng 30% yêu cầu.')

    ah(doc, '5.2 Bốn điểm đổi mới cốt lõi', 2)
    ah(doc, '5.2.1 AI OCR hiểu ngữ cảnh giấy tờ', 3)
    ap(doc, 'SmartReader Doc AI hiểu cấu trúc từng loại giấy tờ, trích xuất có cấu trúc.')
    ah(doc, '5.2.2 Tự động phân loại & định tuyến', 3)
    ap(doc, 'SmartVision phân loại giấy tờ ngay sau scan, định tuyến quy trình riêng.')
    ah(doc, '5.2.3 Đối chiếu thông minh & phát hiện sai lệch', 3)
    ap(doc, 'Đối chiếu tự động với CSDL, cảnh báo từng trường sai lệch.')
    ah(doc, '5.2.4 Pipeline xử lý hàng loạt', 3)
    ap(doc, 'Kiến trúc queue-based, xử lý đến 10.000 hồ sơ/ngày.')

    doc.save(os.path.join(sd, 'proposal.docx'))
    print(f'✅ Task 6: Section "Đổi mới & Khác biệt" added')

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Chạy script và commit**

Run:
```bash
cd /run/media/sanng/New\ Volume/HACKAITHON
python3 hackaithon-de-tai-6-autocheck/add_section5.py
git add hackaithon-de-tai-6-autocheck/add_section5.py hackaithon-de-tai-6-autocheck/proposal.docx
git commit -m "task-6: add innovation analysis with comparison table and 4 USPs"
```

    t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.style = 'Table Grid'
    for i, h in enumerate(hd):
        c = t.rows[0].cells[i]; c.text = ''; p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER; r = p.add_run(h)
        sf(r, s=11, b=True, c=RGBColor(0xFF,0xFF,0xFF))

---

## 📝 Task 7: Tác động dự kiến (Expected Impact)

**File:** `hackaithon-de-tai-6-autocheck/proposal.docx`
**Tiêu chí:** Tác động dự kiến (20đ) | **Độ dài:** 2 trang

- [ ] **Step 1: Tạo `add_section6.py` với nội dung Tác động**

```python
#!/usr/bin/env python3
"""Add section 6. TÁC ĐỘNG DỰ KIẾN to AutoCheck proposal."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

def sf(run, n='Times New Roman', s=14, b=False, c=None):
    run.font.name = n; run.font.size = Pt(s); run.bold = b
    run.element.rPr.rFonts.set(qn('w:eastAsia'), n)
    if c: run.font.color.rgb = c

def apb(doc):
    p = doc.add_paragraph(); r = p.add_run(); r.add_break(WD_BREAK.PAGE)

def ah(doc, t, lv=1):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    sz = {1: 18, 2: 16}.get(lv, 14)
    r = p.add_run(t); sf(r, s=sz, b=True, c=RGBColor(0x00, 0x66, 0xCC))
    if lv == 1:
        pPr = p._p.get_or_add_pPr()
        pBdr = parse_xml('<w:pBdr %s><w:bottom w:val="single" w:sz="8" w:space="1" w:color="0066CC"/></w:pBdr>' % nsdecls('w'))
        pPr.append(pBdr)

def ap(doc, t, ind=True):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    if ind: p.paragraph_format.first_line_indent = Cm(1.27)
    r = p.add_run(t); sf(r); return p

def mt(doc, hd, data):
    t = doc.add_table(rows=1+len(data), cols=len(hd))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.style = 'Table Grid'
    for i, h in enumerate(hd):
        c = t.rows[0].cells[i]; c.text = ''; p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER; r = p.add_run(h)
        sf(r, s=11, b=True, c=RGBColor(0xFF,0xFF,0xFF))
        c._tc.get_or_add_tcPr().append(parse_xml('<w:shd %s w:fill="0066CC" w:val="clear"/>' % nsdecls('w')))
    for ri, rd in enumerate(data):
        for ci, ct in enumerate(rd):
            c = t.rows[ri+1].cells[ci]; c.text = ''; p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT; r = p.add_run(ct); sf(r, s=10)
            if ri % 2 == 1:
                c._tc.get_or_add_tcPr().append(parse_xml('<w:shd %s w:fill="E8F0FE" w:val="clear"/>' % nsdecls('w')))

def main():
    sd = os.path.dirname(os.path.abspath(__file__))
    doc = Document(os.path.join(sd, 'proposal.docx'))
    apb(doc); ah(doc, '6. TÁC ĐỘNG DỰ KIẾN')

    ah(doc, '6.1 Phân tích thị trường (TAM-SAM-SOM)', 2)
    mt(doc, ['Chỉ số', 'Giá trị', 'Cách tính', 'Nguồn'], [
        ['TAM', '~5.000 tỷ VNĐ', 'Số hóa tài liệu HC 63 tỉnh, ~80 tỷ/tỉnh/năm', 'Bộ TT&TT 2025'],
        ['SAM', '~300 tỷ VNĐ', 'OCR+AI cho hồ sơ lưu trữ cấp phường (6% TAM)', 'Phân tích nội bộ'],
        ['SOM', '~15 tỷ VNĐ', '5% SAM trong 2 năm (~50-100 UBND)', 'Dự báo thận trọng'],
    ])
    p = doc.add_paragraph(); sf(p.add_run(''), size=6)

    ah(doc, '6.2 Lợi ích xã hội', 2)
    mt(doc, ['Lợi ích', 'Chỉ số', 'Giải thích'], [
        ['Tăng tốc xử lý hồ sơ', 'Nhanh 10-15x', '30-60 phút → 2-5 phút/hồ sơ'],
        ['Tiết kiệm nhân công', 'Giảm 60%', '1 hệ thống = 3-5 nhân viên'],
        ['Giảm sai sót', 'Giảm 90%', 'AI tự động kiểm tra + cảnh báo'],
        ['Tiết kiệm không gian', 'Giảm 95%', 'Kho giấy → ổ cứng 1TB ~500.000 hồ sơ'],
        ['Tra cứu tức thì', '< 5 giây', 'Full-text search từ CSDL số hóa'],
        ['Bảo tồn dữ liệu', 'Vĩnh viễn', 'Backup tự động, không lo hư hỏng'],
    ])
    p = doc.add_paragraph(); sf(p.add_run(''), size=6)

    ah(doc, '6.3 Mô hình doanh thu (B2G)', 2)
    mt(doc, ['Gói', 'Giá', 'Dịch vụ'], [
        ['Basic', '8.000.000/tháng', '1 máy scan, 1.000 hồ sơ/tháng, hỗ trợ 8h'],
        ['Pro', '20.000.000/tháng', 'Đa máy scan, 5.000 hồ sơ/tháng, 24/7'],
        ['Enterprise', 'Theo yêu cầu', 'Không giới hạn, tích hợp CSDL riêng, SLA'],
    ])
    ap(doc, 'Phí triển khai: 40-60 triệu. Hòa vốn 12 tháng với 15 KH Basic (~120 triệu/tháng). ROI 3 năm: ~250%.')

    ah(doc, '6.4 Phân tích cạnh tranh', 2)
    ap(doc, 'Đối thủ trên thị trường số hóa tài liệu:')
    for c in [
        'FPT.eDoc: OCR cơ bản, không AI phân loại. Giá 15-30 triệu/tháng.',
        'VNPT eDoc: OCR cơ bản, chưa tích hợp SmartReader Doc AI.',
        'Google Doc AI: OCR mạnh nhưng chưa tối ưu tiếng Việt, không đạt chuẩn VN.',
        'Nhân công thủ công: 10-15 triệu/tháng/người, chậm, sai sót.',
    ]:
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(1.5); p.paragraph_format.line_spacing = 1.5
        r = p.add_run('• '); sf(r, s=13); r = p.add_run(c); sf(r, s=13)

    doc.save(os.path.join(sd, 'proposal.docx'))
    print(f'✅ Task 7: Section "Tác động dự kiến" added')

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Chạy script và commit**

Run:
```bash
cd /run/media/sanng/New\ Volume/HACKAITHON
python3 hackaithon-de-tai-6-autocheck/add_section6.py
git add hackaithon-de-tai-6-autocheck/add_section6.py hackaithon-de-tai-6-autocheck/proposal.docx
git commit -m "task-7: add expected impact with TAM-SAM-SOM, benefits, revenue"
```

        c._tc.get_or_add_tcPr().append(parse_xml('<w:shd %s w:fill="0066CC" w:val="clear"/>' % nsdecls('w')))
    for ri, rd in enumerate(data):
        for ci, ct in enumerate(rd):
            c = t.rows[ri+1].cells[ci]; c.text = ''; p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT; r = p.add_run(ct); sf(r, s=10)
            if ri % 2 == 1:
                c._tc.get_or_add_tcPr().append(parse_xml('<w:shd %s w:fill="E8F0FE" w:val="clear"/>' % nsdecls('w')))


---

## 📝 Task 8: Hoàn thiện hồ sơ & Xuất PDF

**File:** `hackaithon-de-tai-6-autocheck/proposal.docx` → `hackaithon-de-tai-6-autocheck/proposal.pdf`

- [ ] **Step 1: Tạo `finalize_proposal.py`**

```python
#!/usr/bin/env python3
"""Task 8: Finalize AutoCheck - header, footer, conclusion, PDF."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml, OxmlElement
import os, subprocess

def sf(run, n='Times New Roman', s=14, b=False, c=None):
    run.font.name = n; run.font.size = Pt(s); run.bold = b
    run.element.rPr.rFonts.set(qn('w:eastAsia'), n)
    if c: run.font.color.rgb = c

def ah(doc, t):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(t); sf(r, s=18, b=True, c=RGBColor(0x00, 0x66, 0xCC))
    pPr = p._p.get_or_add_pPr()
    pBdr = parse_xml('<w:pBdr %s><w:bottom w:val="single" w:sz="8" w:space="1" w:color="0066CC"/></w:pBdr>' % nsdecls('w'))
    pPr.append(pBdr)

def ap(doc, t, ind=True):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    if ind: p.paragraph_format.first_line_indent = Cm(1.27)
    r = p.add_run(t); sf(r); return p

def add_header_footer(doc):
    for sec in doc.sections:
        h = sec.header; h.is_linked_to_previous = False
        hp = h.paragraphs[0]; hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = hp.add_run('AutoCheck — Đội thi [Tên đội] — Hackathon ĐMST 2026')
        sf(r, s=10, c=RGBColor(0x66, 0x66, 0x66))
        f = sec.footer; f.is_linked_to_previous = False
        fp = f.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # PAGE field
        r = fp.add_run('Trang '); sf(r, s=10, c=RGBColor(0x66, 0x66, 0x66))
        for ftype in ['PAGE', 'NUMPAGES']:
            r2 = fp.add_run(); fc1 = OxmlElement('w:fldChar')
            fc1.set(qn('w:fldCharType'), 'begin'); r2._r.append(fc1)
            r3 = fp.add_run(); it1 = OxmlElement('w:instrText')
            it1.set(qn('xml:space'), 'preserve'); it1.text = f' {ftype} '; r3._r.append(it1)
            r4 = fp.add_run(); fc2 = OxmlElement('w:fldChar')
            fc2.set(qn('w:fldCharType'), 'end'); r4._r.append(fc2)
            if ftype == 'PAGE':
                r5 = fp.add_run(' / Tổng '); sf(r5, s=10, c=RGBColor(0x66, 0x66, 0x66))

def add_conclusion(doc):
    ah(doc, '7. KẾT LUẬN')
    ap(doc, 'AutoCheck là hệ thống OCR thông minh đầu tiên tại Việt Nam kết hợp 3 công nghệ AI cốt lõi của VNPT — SmartReader, SmartVision và eKYC — trong một pipeline xử lý hồ sơ lưu trữ tự động.')
    for b, n in [
        ('1. Giải quyết 3 pain-point:', ' Số hóa hồ sơ tồn đọng, tự động bóc tách & đối chiếu.'),
        ('2. Khác biệt 100%:', ' AI OCR hiểu ngữ cảnh, phân loại, đối chiếu thông minh.'),
        ('3. Tính khả thi cao:', ' Chi phí từ 8 triệu/tháng, MVP 7 ngày, TAM ~5.000 tỷ.'),
    ]:
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(1.0); p.paragraph_format.line_spacing = 1.5
        r = p.add_run(b); sf(r, s=14, b=True); r = p.add_run(n); sf(r, s=14)
    ap(doc, 'Chúng tôi kêu gọi sự hợp tác của VNPT để đưa AutoCheck đến mọi bộ phận một cửa.')
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run('\nAutoCheck\n"Số hóa hôm nay — Giá trị ngày mai."')
    sf(r, s=13, c=RGBColor(0x00, 0x66, 0xCC))

def convert_to_pdf(docx_path, pdf_path):
    try:
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf',
            '--outdir', os.path.dirname(pdf_path), docx_path],
            check=True, timeout=60, capture_output=True)
        print(f'✅ PDF exported: {pdf_path}'); return True
    except:
        print('⚠️ PDF auto-export unavailable. Export manually from Word.'); return False

def main():
    sd = os.path.dirname(os.path.abspath(__file__))
    dx = os.path.join(sd, 'proposal.docx'); px = os.path.join(sd, 'proposal.pdf')
    doc = Document(dx)
    print('📝 Adding header/footer...'); add_header_footer(doc)
    print('📝 Adding conclusion...'); add_conclusion(doc)
    doc.save(dx)
    print(f'✅ Final: {dx} ({os.path.getsize(dx)/1024:.1f} KB)')
    convert_to_pdf(dx, px)
    if os.path.exists(px): print(f'📊 PDF: {os.path.getsize(px)/1024:.1f} KB')
    print('🎯 Task 8 done!')

if __name__ == '__main__':
    main()
```


- [ ] **Step 2: Tạo `verify_content.py`**

```python
"""Verify AutoCheck proposal content."""
from docx import Document; import os
doc = Document(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'proposal.docx'))
print(f'Paragraphs: {len(doc.paragraphs)}, Tables: {len(doc.tables)}\n')
print('=== Sections Check ===')
required = ['ĐẶT VẤN ĐỀ', 'GIẢI PHÁP', 'THIẾT KẾ', 'KHẢ THI', 'ĐỔI MỚI', 'TÁC ĐỘNG', 'KẾT LUẬN']
texts = [p.text.strip().upper() for p in doc.paragraphs if p.text.strip()]
for s in required:
    print(f'  [{"✅" if any(s in t for t in texts) else "❌"}] {s}')
```

- [ ] **Step 3: Chạy finalize + verify**

Run:
```bash
cd /run/media/sanng/New\ Volume/HACKAITHON
python3 hackaithon-de-tai-6-autocheck/finalize_proposal.py
python3 hackaithon-de-tai-6-autocheck/verify_content.py
```
Expected: All 7 sections present, PDF exported

- [ ] **Step 4: Kiểm tra thủ công & sửa lỗi**

> Mở `proposal.docx` trong Word:
> - [ ] Cập nhật `[Tên đội]` bằng tên thật
> - [ ] Cập nhật `[Họ tên]` các thành viên
> - [ ] Kiểm tra font, hình ảnh
> - [ ] Ctrl+A → F9 (update fields)
> - [ ] Xuất PDF lần cuối

- [ ] **Step 5: Commit**

```bash
git add hackaithon-de-tai-6-autocheck/
git commit -m "task-8: finalize AutoCheck proposal, add conclusion and export PDF"
```

---

## 🎯 Bảng Tiêu chí Chấm điểm Vòng 1 (Tóm tắt)

| Nhóm tiêu chí | Mô tả | Điểm | Task |
|---------------|-------|:----:|:----:|
| **1. Tính phù hợp đề bài** | Bám sát đề tài, phân tích pain-point, "Vì sao AI" | 25đ | Task 2, 3 |
| **2. Tính đổi mới & khác biệt** | So sánh ≥30%, USP rõ ràng | 20đ | Task 6 |
| **3. Tính khả thi** | Dữ liệu, kỹ thuật, chi phí, pháp lý, roadmap | 25đ | Task 5 |
| **4. Tác động dự kiến** | TAM-SAM-SOM, lợi ích, cạnh tranh, doanh thu | 20đ | Task 7 |
| **5. Chất lượng hồ sơ** | Trình bày logic, sơ đồ, wireframe, ngôn ngữ | 10đ | Task 4, 8 |
| **Tổng** | | **100đ** | |

---

## 📅 Timeline

| Ngày | Công việc | Task |
|:----:|-----------|:----:|
| 11/06 | Trang bìa + Logo + Đặt vấn đề | Task 1, 2 |
| 12/06 | Giải pháp + Kiến trúc + Assets | Task 3, 4 |
| 13/06 | Tính khả thi + Đổi mới + Tác động | Task 5, 6, 7 |
| 14/06 | Hoàn thiện + Xuất PDF | Task 8 |
| **16/06** | **🚀 NỘP HỒ SƠ** | — |

---

## 🛡️ Self-Review Checklist

- [ ] **1. Spec Coverage:**
  - [ ] Bám sát đề tài 6: "nâng cao năng suất xử lý hồ sơ"
  - [ ] Đề cập 3 pain-point (tồn đọng hồ sơ giấy, tra cứu thủ công, rủi ro hư hỏng)
  - [ ] Đầy đủ cấu trúc hồ sơ Vòng 1 theo Thể lệ

- [ ] **2. Placeholder scan:**
  - [ ] Task 1: `[Tên đội]`, `[Họ tên]` — cần điền trước khi nộp
  - [ ] Không có TBD, TODO trong code

- [ ] **3. Consistency:**
  - [ ] Tên "AutoCheck", API reference đúng: SmartReader, SmartVision, eKYC
  - [ ] Section numbering: 1-7 nhất quán

- [ ] **4. Task completeness:** 8 task bao phủ tất cả yêu cầu Vòng 1

