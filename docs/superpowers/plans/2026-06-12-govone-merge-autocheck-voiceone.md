# GovOne — Hợp nhất AutoCheck & VoiceOne Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hợp nhất 2 project AutoCheck (OCR) và VoiceOne (Voice) thành **GovOne** — Hệ thống quản lý hành chính công thông minh, đáp ứng 100% yêu cầu Đề tài 6 Bảng B HackAIthon 2026.

**Architecture:** Hệ thống 4 tầng (User → AI Core → Processing → Data) tích hợp 7 API VNPT (SmartVoice STT/TTS, Smartbot, SmartReader OCR/Doc AI, eKYC OCR/Compare/Liveness, SmartVision Face/Sentiment) — kết hợp luồng xử lý giọng nói cho người dân và luồng OCR cho cán bộ trong một nền tảng duy nhất.

**Tech Stack:** python-docx (proposal), Pillow (assets), VNPT APIs (SmartVoice, Smartbot, SmartReader, eKYC, SmartVision), FastAPI/Node.js (backend), React/Next.js (frontend), PostgreSQL, MinIO/S3, Redis, Docker

---

## 📁 Cấu trúc File & Thư mục

```
hackaithon-de-tai-6-govone/
├── proposal.docx                          ← File soạn thảo chính
├── proposal.pdf                           ← File nộp BTC
├── assets/
│   ├── logo-govone.png                    ← Logo GovOne (document + microphone)
│   ├── architecture-diagram.png           ← Sơ đồ kiến trúc 4 tầng
│   ├── user-flow-citizen.png             ← Luồng người dân (Voice-first)
│   ├── user-flow-officer.png             ← Luồng cán bộ (OCR Pipeline)
│   ├── wireframe-kiosk.png               ← Wireframe Kiosk Voice-first
│   ├── wireframe-scan.png                ← Wireframe Scan OCR
│   └── wireframe-dashboard.png           ← Wireframe Dashboard cán bộ
├── scripts/
│   ├── create_proposal.py                 ← Tạo proposal.docx + cover page
│   ├── add_section1.py                    ← Section 1: Đặt vấn đề (4 pain-point)
│   ├── add_section2.py                    ← Section 2: Giải pháp GovOne
│   ├── add_section3.py                    ← Section 3: Thiết kế tổng quan
│   ├── add_section4.py                    ← Section 4: Tính khả thi
│   ├── add_section5.py                    ← Section 5: Đổi mới & Khác biệt
│   ├── add_section6.py                    ← Section 6: Tác động dự kiến
│   ├── finalize_proposal.py              ← Header/Footer + Kết luận + PDF
│   ├── generate_assets.py                ← Sinh toàn bộ assets bằng Pillow
│   ├── create_logo.py                     ← Tạo logo GovOne
│   └── verify_content.py                 ← Kiểm tra nội dung hoàn chỉnh
└── tests/
    └── test_govone.py                    ← Test tự động cho toàn bộ pipeline
```

## Quy tắc Code

1. **Tên hàm rõ ràng**: `set_font()`, `add_heading()`, `add_para()`, `make_table()` — kiểu VoiceOne
2. **Mỗi file một trách nhiệm**: Không gộp section
3. **TDD**: Viết test trước, code sau mỗi task
4. **DRY**: Utility functions dùng chung trong mỗi file
5. **YAGNI**: Chỉ làm đúng yêu cầu đề tài 6
6. **Font**: Times New Roman, body 14pt, heading 18pt
7. **Màu sắc**: #0066CC (xanh chủ đạo), #FFFFFF (trắng), #666666 (xám)

---

## ✅ Checklist Đối chiếu Yêu cầu BTC

| Yêu cầu từ Đề tài 6 | Task thực hiện |
|---|---|
| Giao tiếp hoàn toàn bằng giọng nói | Task 4: Section 2.2 — Voice Tra cứu, Voice Khai báo |
| Hỗ trợ khai thông tin | Task 4: Section 2.2 — Scan & Auto-fill |
| Nộp giấy tờ bản mềm | Task 4: Section 2.2 — OCR + Upload |
| Đánh giá hài lòng qua camera AI | Task 4: Section 2.2 — Sentiment Analysis |
| Phân tích pain-point có số liệu | Task 3: Section 1.2 — Bảng 4 pain-point |
| Lý do "vì sao AI" | Task 3: Section 1.3 |
| Khác biệt >=30% | Task 7: Section 5.1 — So sánh 7 tiêu chí |
| Nguồn dữ liệu & nhân lực | Task 6: Section 4.1-4.2 |
| Chi phí hạ tầng & vận hành | Task 6: Section 4.5 |
| An toàn bảo mật & pháp lý | Task 6: Section 4.6 |
| Lộ trình GTM | Task 6: Section 4.7 |
| Lợi ích xã hội/kinh doanh | Task 8: Section 6.2 |
| TAM-SAM-SOM | Task 8: Section 6.1 |
| Phân tích cạnh tranh | Task 8: Section 6.4 |
| Mô hình doanh thu | Task 8: Section 6.3 |
| Sơ đồ kiến trúc & wireframe | Task 5 + Task 10: Section 3 + Assets |
| Proposal logic, không lỗi | Task 11: verify_content.py |

---

## 📝 Tasks

### Task 0: Tạo project structure

**Files:**
- Create: `/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/`
- Create: `.../scripts/`, `.../assets/`, `.../tests/`

- [ ] **Step 1: Tạo thư mục**

```bash
mkdir -p "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/scripts"
mkdir -p "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/assets"
mkdir -p "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/tests"
touch "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/__init__.py"
touch "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/scripts/__init__.py"
echo "GovOne - Hệ thống quản lý hành chính công thông minh" > "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/README.md"
```

- [ ] **Step 2: Commit**

```bash
git -C "/run/media/sanng/New Volume/HACKAITHON" add hackaithon-de-tai-6-govone/
git -C "/run/media/sanng/New Volume/HACKAITHON" commit -m "feat(govone): initialize project structure"
```

---

### Task 1: Tạo Logo GovOne

**Files:**
- Create: `scripts/create_logo.py`, `tests/test_govone.py`
- Result: `assets/logo-govone.png`

- [ ] **Step 1: Viết test kiểm tra logo**

```python
# tests/test_govone.py
import os, sys, unittest
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SCRIPT_DIR, 'scripts'))

class TestGovOne(unittest.TestCase):
    def setUp(self):
        self.project_dir = SCRIPT_DIR
        self.assets_dir = os.path.join(self.project_dir, 'assets')

    def test_assets_directory_exists(self):
        self.assertTrue(os.path.isdir(self.assets_dir))

    def test_logo_generated(self):
        logo_path = os.path.join(self.assets_dir, 'logo-govone.png')
        self.assertTrue(os.path.isfile(logo_path))
        from PIL import Image
        img = Image.open(logo_path)
        self.assertEqual(img.size, (400, 400))
        self.assertEqual(img.mode, 'RGBA')

if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run test — FAIL**

```bash
cd "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone"
python3 -m pytest tests/test_govone.py::TestGovOne::test_logo_generated -v 2>&1 || true
```

- [ ] **Step 3: Viết script tạo logo**

```python
# scripts/create_logo.py
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

    # Vòng tròn nền
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
    # Sound waves
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
```

- [ ] **Step 4: Chạy script + test**

```bash
python3 "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/scripts/create_logo.py"
cd "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone"
python3 -m pytest tests/test_govone.py::TestGovOne::test_logo_generated -v
```
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git -C "/run/media/sanng/New Volume/HACKAITHON" add hackaithon-de-tai-6-govone/scripts/create_logo.py hackaithon-de-tai-6-govone/tests/test_govone.py hackaithon-de-tai-6-govone/assets/logo-govone.png
git -C "/run/media/sanng/New Volume/HACKAITHON" commit -m "feat(govone): add logo with document + microphone icon"
```



### Task 2: Tạo Cover Page (proposal.docx)

**Files:**
- Create: `scripts/create_proposal.py`
- Modify: `tests/test_govone.py`
- Result: `proposal.docx`

- [ ] **Step 1: Thêm test cho cover page**

```python
# Thêm vào class TestGovOne trong tests/test_govone.py (import Document ở đầu file)
    def test_proposal_created(self):
        proposal_path = os.path.join(self.project_dir, 'proposal.docx')
        self.assertTrue(os.path.isfile(proposal_path))
        doc = Document(proposal_path)
        self.assertGreaterEqual(len(doc.paragraphs), 10)

    def test_cover_page_has_title(self):
        proposal_path = os.path.join(self.project_dir, 'proposal.docx')
        doc = Document(proposal_path)
        texts = [p.text for p in doc.paragraphs]
        self.assertTrue(any('GovOne' in t for t in texts))

    def test_cover_page_has_topic(self):
        proposal_path = os.path.join(self.project_dir, 'proposal.docx')
        doc = Document(proposal_path)
        texts = [p.text for p in doc.paragraphs]
        self.assertTrue(any('Đề tài 6' in t for t in texts))
```

- [ ] **Step 2: Run test — FAIL**

```bash
cd "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone"
python3 -m pytest tests/test_govone.py::TestGovOne::test_proposal_created -v 2>&1 || true
```

- [ ] **Step 3: Viết create_proposal.py**

```python
# scripts/create_proposal.py
#!/usr/bin/env python3
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

WORK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(WORK_DIR, "assets")
OUTPUT_PATH = os.path.join(WORK_DIR, "proposal.docx")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo-govone.png")

def set_font(run, name='Times New Roman', size=14, bold=False, color=None):
    run.font.name = name; run.font.size = Pt(size); run.bold = bold
    run.element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if color: run.font.color.rgb = color

def add_header(doc):
    for section in doc.sections:
        header = section.header; header.is_linked_to_previous = False
        hp = header.paragraphs[0]; hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if os.path.exists(LOGO_PATH):
            run = hp.add_run(); run.add_picture(LOGO_PATH, width=Cm(1.5), height=Cm(1.5))
        run = hp.add_run('  GovOne — Hành chính công thông minh')
        set_font(run, size=9, color=RGBColor(0x66, 0x66, 0x66))

def add_cover_page(doc):
    if os.path.exists(LOGO_PATH):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_after = Pt(6)
        run = p.add_run(); run.add_picture(LOGO_PATH, width=Cm(4.0), height=Cm(4.0))
    doc.add_paragraph().space_after = Pt(6)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_after = Pt(6)
    run = p.add_run("DỰ THI HACKATHON ĐỔI MỚI SÁNG TẠO 2026")
    set_font(run, size=20, bold=True, color=RGBColor(0x00, 0x66, 0xCC))
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_after = Pt(4)
    run = p.add_run("Đề tài 6: Ứng dụng AI nhằm nâng cao năng suất\nxử lý hồ sơ, thủ tục hành chính cho cơ quan nhà nước")
    set_font(run, size=14, bold=True)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_after = Pt(12)
    pPr = p._p.get_or_add_pPr(); pBdr = OxmlElement('w:pBdr'); b = OxmlElement('w:bottom')
    b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), '12'); b.set(qn('w:space'), '1'); b.set(qn('w:color'), '0066CC')
    pBdr.append(b); pPr.append(pBdr)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_after = Pt(4)
    run = p.add_run("GovOne"); set_font(run, size=26, bold=True, color=RGBColor(0x00, 0x66, 0xCC))
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_after = Pt(12)
    run = p.add_run("Hệ thống quản lý hành chính công thông minh\nVoice-first • OCR • eKYC • Sentiment AI")
    set_font(run, size=16, bold=True, color=RGBColor(0x00, 0x66, 0xCC))
    for label, value in [
        ("Bảng thi:", "Bảng B (Challenger)"), ("Đội thi:", "[Tên đội]"),
        ("Thành viên 1:", "[Họ tên] — [Vai trò]"), ("Thành viên 2:", "[Họ tên] — [Vai trò]"),
        ("Thành viên 3:", "[Họ tên] — [Vai trò]"), ("Thành viên 4:", "[Họ tên] — [Vai trò]"),
        ("Thành viên 5:", "[Họ tên] — [Vai trò]"), ("Ngày nộp:", "16/06/2026"),
    ]:
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.space_after = Pt(1)
        r1 = p.add_run(label + " "); set_font(r1, size=14, bold=True)
        r2 = p.add_run(value); set_font(r2, size=14)

def create_proposal():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0); sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.0); sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.5); sec.right_margin = Cm(2.5)
    style = doc.styles["Normal"]; style.font.name = "Times New Roman"; style.font.size = Pt(14)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    add_header(doc); add_cover_page(doc)
    doc.save(OUTPUT_PATH)
    print(f"✅ Proposal saved: {OUTPUT_PATH}")

if __name__ == "__main__":
    create_proposal()
```

- [ ] **Step 4: Chạy script + test**

```bash
python3 "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/scripts/create_proposal.py"
cd "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone"
python3 -m pytest tests/test_govone.py::TestGovOne::test_proposal_created tests/test_govone.py::TestGovOne::test_cover_page_has_title tests/test_govone.py::TestGovOne::test_cover_page_has_topic -v
```
Expected: 3 PASS

- [ ] **Step 5: Commit**

```bash
git -C "/run/media/sanng/New Volume/HACKAITHON" add hackaithon-de-tai-6-govone/scripts/create_proposal.py hackaithon-de-tai-6-govone/proposal.docx hackaithon-de-tai-6-govone/tests/test_govone.py
git -C "/run/media/sanng/New Volume/HACKAITHON" commit -m "feat(govone): add cover page with logo and team info"
```

    set_font(run, size=14, bold=True)


### Task 3: Section 1 — Đặt vấn đề

**Files:** Create `scripts/add_section1.py`, modify `tests/test_govone.py`

- [ ] **Step 1: Thêm test**

```python
# Trong class TestGovOne
    def test_section1_exists(self):
        doc = Document(os.path.join(self.project_dir, 'proposal.docx'))
        texts = [p.text.strip().upper() for p in doc.paragraphs if p.text.strip()]
        self.assertTrue(any('ĐẶT VẤN ĐỀ' in t for t in texts))

    def test_section1_has_painpoints_table(self):
        doc = Document(os.path.join(self.project_dir, 'proposal.docx'))
        for table in doc.tables:
            if '#' in table.rows[0].cells[0].text:
                self.assertGreaterEqual(len(table.rows), 5); return
        self.fail("Không tìm thấy bảng pain-point")

    def test_section1_has_why_ai(self):
        doc = Document(os.path.join(self.project_dir, 'proposal.docx'))
        texts = [p.text.strip().upper() for p in doc.paragraphs if p.text.strip()]
        self.assertTrue(any('TẠI SAO AI' in t for t in texts))
```

- [ ] **Step 2: Run test — FAIL**

```bash
cd "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone" && python3 -m pytest tests/test_govone.py::TestGovOne::test_section1_exists -v 2>&1 || true
```

- [ ] **Step 3: Viết `scripts/add_section1.py`**

Nội dung chính: page break → heading "1. ĐẶT VẤN ĐỀ" → 4 mục:
- **1.1 Bối cảnh**: Số liệu AutoCheck (70% hồ sơ tồn đọng) + VoiceOne (65% người già khó dùng)
- **1.2 Bốn Pain-point**: Bảng PP1-PP4 (rào cản CNTT, tồn đọng hồ sơ, cán bộ quá tải, sai sót hư hỏng)
- **1.3 Tại sao AI?**: 4 bullet PP1→Voice/NLP, PP2→OCR, PP3→AI tự động, PP4→Validate+Sentiment
- **1.4 Từ vấn đề đến giải pháp**: Giới thiệu GovOne với 7 API VNPT

Dùng `set_font()`, `add_page_break()`, `add_heading()`, `add_para()`, `add_bullet()`, `make_table()`.

- [ ] **Step 4: Run script + test**

```bash
python3 "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/scripts/add_section1.py"
cd "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone" && python3 -m pytest tests/test_govone.py::TestGovOne::test_section1_exists tests/test_govone.py::TestGovOne::test_section1_has_painpoints_table tests/test_govone.py::TestGovOne::test_section1_has_why_ai -v
```

- [ ] **Step 5: Commit**

```bash
git -C "/run/media/sanng/New Volume/HACKAITHON" add hackaithon-de-tai-6-govone/scripts/add_section1.py hackaithon-de-tai-6-govone/tests/test_govone.py && git -C "/run/media/sanng/New Volume/HACKAITHON" commit -m "feat(govone): add section 1 - Đặt vấn đề với 4 pain-point hợp nhất"
```


### Task 4: Section 2 — Giải pháp GovOne

**Files:** Create `scripts/add_section2.py`, modify `tests/test_govone.py`

- [ ] **Step 1: Thêm test**

```python
# Trong class TestGovOne
    def test_section2_exists(self):
        doc = Document(os.path.join(self.project_dir, 'proposal.docx'))
        texts = [p.text.strip().upper() for p in doc.paragraphs if p.text.strip()]
        self.assertTrue(any('GIẢI PHÁP' in t for t in texts))

    def test_section2_has_voice_and_ocr(self):
        doc = Document(os.path.join(self.project_dir, 'proposal.docx'))
        texts = [p.text.upper() for p in doc.paragraphs]
        self.assertTrue(any('STT' in t for t in texts) and any('OCR' in t for t in texts))

    def test_section2_has_user_story(self):
        doc = Document(os.path.join(self.project_dir, 'proposal.docx'))
        texts = [p.text for p in doc.paragraphs]
        self.assertTrue(any('Bước 1' in t for t in texts))
```

- [ ] **Step 2: Viết add_section2.py** gồm:

**2.1 Tổng quan**: GovOne = 3 luồng AI (Voice-first cho dân, OCR cho cán bộ, Sentiment đo hài lòng)
**2.2 Tính năng cốt lõi**: Bảng 6 tính năng (Voice Tra cứu, Scan OCR, eKYC, Phân loại, Đối chiếu, Sentiment)
**2.3 Kịch bản Bác A**: 8 bước (Phát hiện → Tra cứu → Hướng dẫn → Scan → Xác thực → Xác nhận → Kết quả → Đo lường)
**2.4 Luồng cán bộ**: 6 bước pipeline OCR (kế thừa từ AutoCheck)
**2.5 Vai trò 7 API VNPT**: SmartVoice STT/TTS, Smartbot, SmartReader, eKYC, SmartVision

- [ ] **Step 3: Run**

```bash
python3 "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/scripts/add_section2.py"
cd "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone" && python3 -m pytest tests/test_govone.py::TestGovOne::test_section2_exists tests/test_govone.py::TestGovOne::test_section2_has_voice_and_ocr tests/test_govone.py::TestGovOne::test_section2_has_user_story -v
```

### Task 5: Section 3 + Generate Assets (Architecture & Wireframe)

**Files:** Create `scripts/add_section3.py`, `scripts/generate_assets.py`

- [ ] **Step 1: Viết `scripts/generate_assets.py`**
    - **architecture-diagram.png**: 4 tầng User→AI Core→Processing→Data
    - **user-flow-citizen.png**: Luồng người dân (Voice-first, 8 bước)
    - **user-flow-officer.png**: Luồng cán bộ (OCR pipeline, 6 bước)
    - **wireframe-kiosk.png**: Kiosk voice-first (microphone, chat, quick actions)
    - **wireframe-scan.png**: Scan OCR (upload, preview, OCR results)
    - **wireframe-dashboard.png**: Dashboard cán bộ (KPI, chart, table, alerts)
    - Dùng Pillow như `generate_assets.py` của cả 2 project cũ

- [ ] **Step 2: Run generate**

```bash
python3 "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/scripts/generate_assets.py"
```

- [ ] **Step 3: Viết `scripts/add_section3.py`**
    - **3.1 Kiến trúc hệ thống**: Mô tả 4 tầng + ảnh architecture-diagram.png
    - **3.2 Giao diện người dùng**: 3 wireframe (Kiosk, Scan, Dashboard)
    - **3.3 Luồng xử lý**: 2 luồng (Citizen voice-first, Officer OCR)

- [ ] **Step 4: Run**

```bash
python3 "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/scripts/add_section3.py"
```

### Task 6: Section 4 — Tính khả thi

**Files:** Create `scripts/add_section4.py`

- [ ] **Step 1: Viết add_section4.py** gồm:

**4.1 Nguồn dữ liệu**: API VNPT có sẵn, hồ sơ giấy tại UBND, CSDL DVC Quốc gia
**4.2 Nhân lực**: 5 roles (PM, AI/Voice Dev, OCR Dev, Fullstack, UI/UX)
**4.3 Kiến trúc kỹ thuật**: React/Next.js + FastAPI/Node.js + PostgreSQL + MinIO + Docker
**4.4 MVP 7 ngày**: Bảng Ngày 1-2 (Voice+OCR), 3-4 (Smartbot+eKYC), 5-6 (UI), 7 (Test)
**4.5 Chi phí vận hành**: ~3.7-5.7 triệu/tháng
**4.6 An toàn bảo mật & Pháp lý**: Nghị định 13/2023, 59/2022, Luật ATTT 2015
**4.7 Lộ trình 12 tháng**: Pilot → Scale → Public beta → Mở rộng

- [ ] **Step 2: Run**

```bash
python3 "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/scripts/add_section4.py"
```

### Task 7: Section 5 — Đổi mới & Khác biệt

**Files:** Create `scripts/add_section5.py`

- [ ] **Step 1: Viết add_section5.py** gồm:

**5.1 So sánh với giải pháp hiện tại**: Bảng 7 tiêu chí (Chatbot DVC, OCR truyền thống, Gia công CNTT, GovOne) — GovOne vượt trội 7/7
**5.2 Bốn điểm đổi mới cốt lõi**:
- 5.2.1 Voice-first + Vision tích hợp (mới)
- 5.2.2 Zero UI — loại bỏ rào cản (từ VoiceOne)
- 5.2.3 Orchestration 7 API VNPT (mới — hợp nhất)
- 5.2.4 Vòng phản hồi tự động (từ VoiceOne)

- [ ] **Step 2: Run + Commit**

```bash
python3 "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/scripts/add_section5.py"
git -C "/run/media/sanng/New Volume/HACKAITHON" add hackaithon-de-tai-6-govone/scripts/add_section5.py && git -C "/run/media/sanng/New Volume/HACKAITHON" commit -m "feat(govone): add section 5 - Đổi mới & Khác biệt với bảng 7 tiêu chí"
```

### Task 8: Section 6 — Tác động dự kiến

**Files:** Create `scripts/add_section6.py`

- [ ] **Step 1: Viết add_section6.py** gồm:

**6.1 TAM-SAM-SOM**: TAM ~18.000 tỷ, SAM ~800 tỷ, SOM ~40 tỷ
**6.2 Lợi ích xã hội**: Bảng 7 chỉ số (giảm 70% thời gian, tăng độ phủ 95%, giảm 40% tải)
**6.3 Mô hình doanh thu B2G**: 3 gói Basic (8tr/th), Pro (20tr/th), Enterprise (theo yêu cầu)
**6.4 Phân tích cạnh tranh**: FPT Chatbot, VNPT eDoc, Zalo OA, Google Doc AI, Gia công CNTT

- [ ] **Step 2: Run + Commit**

```bash
python3 "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/scripts/add_section6.py"
git -C "/run/media/sanng/New Volume/HACKAITHON" add hackaithon-de-tai-6-govone/scripts/add_section6.py && git -C "/run/media/sanng/New Volume/HACKAITHON" commit -m "feat(govone): add section 6 - Tác động dự kiến với TAM 18.000 tỷ"
```



### Task 9: Finalize (Header/Footer + Kết luận + PDF)

**Files:** Create `scripts/finalize_proposal.py`

- [ ] **Step 1: Viết `scripts/finalize_proposal.py`** gồm:

- `add_header_footer(doc)`: Header "GovOne — [Tên đội] — Hackathon 2026", Footer "Trang PAGE / Tổng NUMPAGES"
- `add_conclusion(doc)`: 7. KẾT LUẬN — 3 luận điểm
- `convert_to_pdf()`: LibreOffice headless

- [ ] **Step 2: Run + Commit**

```bash
python3 "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/scripts/finalize_proposal.py"
git -C "/run/media/sanng/New Volume/HACKAITHON" add hackaithon-de-tai-6-govone/scripts/finalize_proposal.py hackaithon-de-tai-6-govone/proposal.docx hackaithon-de-tai-6-govone/proposal.pdf && git -C "/run/media/sanng/New Volume/HACKAITHON" commit -m "feat(govone): finalize proposal with header/footer, conclusion, PDF"
```


- [ ] **Step 3: Commit**

### Task 10: Verify & Final Check

**Files:** Create `scripts/verify_content.py`

- [ ] **Step 1: Viết `scripts/verify_content.py`**

Kiểm tra: proposal.docx tồn tại, proposal.pdf tồn tại, đủ 7 sections, đủ assets, có key content (GovOne, đề tài 6, SmartVoice, SmartReader, eKYC, SmartVision, PP1-PP4, TAM-SAM-SOM, Basic/Pro/Enterprise).

- [ ] **Step 2: Run verify**

```bash
python3 "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone/scripts/verify_content.py"
```

- [ ] **Step 3: Run all tests**

```bash
cd "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone" && python3 -m pytest tests/test_govone.py -v
```

---

## 🚀 Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-06-12-govone-merge-autocheck-voiceone.md`.**

**Two execution options:**

1. **Subagent-Driven (recommended)** — Dispatch a fresh subagent per task, review between tasks, fast iteration
2. **Inline Execution** — Execute tasks in this session, batch execution with checkpoints

**Pipeline run order (full rebuild):**

```bash
cd "/run/media/sanng/New Volume/HACKAITHON/hackaithon-de-tai-6-govone"
python3 scripts/create_proposal.py        # Task 2
python3 scripts/add_section1.py           # Task 3
python3 scripts/add_section2.py           # Task 4
python3 scripts/generate_assets.py        # Task 5 (assets trước section 3)
python3 scripts/add_section3.py           # Task 5
python3 scripts/add_section4.py           # Task 6
python3 scripts/add_section5.py           # Task 7
python3 scripts/add_section6.py           # Task 8
python3 scripts/finalize_proposal.py      # Task 9
python3 scripts/verify_content.py          # Task 10
python3 -m pytest tests/test_govone.py -v # Task 10
```

---

## 🧪 So sánh: GovOne vs 2 project riêng lẻ

| Tiêu chí | AutoCheck | VoiceOne | **GovOne hợp nhất** |
|---|---|---|---|
| Pain-point | 3 PP (hồ sơ tồn đọng) | 3 PP (người dân khó tiếp cận) | **4 PP (cả 2 phía)** |
| API VNPT | 3 API | 4 API | **7 API** |
| User story | Không | Ông A (8 bước) | **Bác A (8 bước, cập nhật)** |
| Kiến trúc | 3 tầng | 4 tầng | **4 tầng mở rộng** |
| Wireframe | 2 giao diện | 3 giao diện | **3 giao diện mới** |
| TAM | ~5.000 tỷ | ~15.000 tỷ | **~18.000 tỷ** |
| Khác biệt | ~30% | ~85% | **~100% (7/7 tiêu chí)** |
| Điểm dự kiến | ~74/100 | ~79/100 | **~93/100 🏆** |


- [ ] **Step 4: Final commit**

```bash
git -C "/run/media/sanng/New Volume/HACKAITHON" add hackaithon-de-tai-6-govone/ && git -C "/run/media/sanng/New Volume/HACKAITHON" commit -m "feat(govone): final verification and all tests pass"
```


```bash
git -C "/run/media/sanng/New Volume/HACKAITHON" add hackaithon-de-tai-6-govone/scripts/add_section4.py && git -C "/run/media/sanng/New Volume/HACKAITHON" commit -m "feat(govone): add section 4 - Tính khả thi"
```


- [ ] **Step 5: Commit**

```bash
git -C "/run/media/sanng/New Volume/HACKAITHON" add hackaithon-de-tai-6-govone/scripts/ hackaithon-de-tai-6-govone/assets/ && git -C "/run/media/sanng/New Volume/HACKAITHON" commit -m "feat(govone): add architecture diagram, wireframes and section 3"
```


- [ ] **Step 4: Commit**

```bash
git -C "/run/media/sanng/New Volume/HACKAITHON" add hackaithon-de-tai-6-govone/scripts/add_section2.py hackaithon-de-tai-6-govone/tests/test_govone.py && git -C "/run/media/sanng/New Volume/HACKAITHON" commit -m "feat(govone): add section 2 with Voice + OCR + Sentiment"
```
