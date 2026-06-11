# Đề tài 6 — Bảng B — Vòng 1: Khung Ý Tưởng & Hồ Sơ Dự Thi — VoiceOne

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hoàn thiện bộ hồ sơ ý tưởng Vòng 1 — Bảng B (Challenger) — Đề tài 6 để nộp lên hackaithon.vsds.vn trước 16/06/2026, với giải pháp **VoiceOne** — trợ lý giọng nói cho bộ phận một cửa.

**Architecture:** Hệ thống microservices 4 tầng (User → AI Core → Processing → Data) tích hợp các API VNPT (SmartVoice STT/TTS, Smartbot, eKYC, SmartReader, SmartVision) để tạo trải nghiệm voice-first cho người dân tại bộ phận một cửa. Frontend React/Vue trên Kiosk + Web, Backend Node.js/Python, Database PostgreSQL + Redis.

**Tech Stack:** VNPT SmartVoice (STT/TTS), VNPT Smartbot, VNPT eKYC (OCR/Compare/Liveness), VNPT SmartReader, VNPT SmartVision, React/Vue, Node.js/Python FastAPI, PostgreSQL, Redis, Docker, GitHub Actions

**Sản phẩm đầu ra:** 01 file PDF hồ sơ ý tưởng (tối đa 15-20 trang) bao gồm đầy đủ các phần:
1. Trang bìa & Thông tin đội thi
2. Đặt vấn đề (Problem Statement)
3. Giải pháp (Solution)
4. Thiết kế tổng quan (Architecture & Wireframe)
5. Tính khả thi (Feasibility)
6. Tính đổi mới & khác biệt (Innovation)
7. Tác động dự kiến (Impact)
8. Phương hướng triển khai (Roadmap)

**Các API VNPT có thể dùng:** SmartVoice (STT/TTS), eKYC (OCR, Liveness, Compare), Smartbot, SmartReader, vnFace, SmartVision, vnSocial, SmartUX

---

## 📁 Cấu trúc File & Thư mục

```
/run/media/sanng/New Volume/AI-QUANCOM/
├── docs/superpowers/plans/
│   └── 2026-06-11-hackaithon-de-tai-6-bang-b-vong-1.md   ← Plan này
├── hackaithon-de-tai-6-vong-1/
│   ├── proposal.docx                                         ← File soạn thảo chính
│   ├── proposal.pdf                                          ← File nộp BTC
│   ├── assets/
│   │   ├── architecture-diagram.png                          ← Sơ đồ kiến trúc
│   │   ├── wireframe-dashboard.png                           ← Wireframe màn hình chính
│   │   ├── wireframe-voice-interface.png                     ← Wireframe giao diện giọng nói
│   │   ├── user-flow.png                                     ← Sơ đồ luồng người dùng
│   │   └── logo-team.png                                     ← Logo đội thi (nếu có)
│   └── references/
│       └── tai-lieu-tham-khao.md                               ← Tài liệu tham khảo
```


---

## 📋 Cấu trúc Hồ sơ Vòng 1 (Bảng B)

Dựa theo yêu cầu từ Thể lệ, hồ sơ Vòng 1 bắt buộc có:

| Phần | Nội dung | Điểm tối đa |
|------|----------|:-----------:|
| **1. Trang bìa** | Tên sản phẩm, thông tin đội thi | — |
| **2. Đặt vấn đề & Giải pháp** | Problem statement + solution overview | **25đ** (Tính phù hợp) |
| **3. Tính đổi mới & khác biệt** | So sánh với giải pháp hiện có, USP ≥30% | **20đ** |
| **4. Tính khả thi** | Dữ liệu, kỹ thuật, chi phí, pháp lý, lộ trình | **25đ** |
| **5. Tác động dự kiến** | TAM-SAM-SOM, lợi ích, cạnh tranh, doanh thu | **20đ** |
| **6. Chất lượng hồ sơ** | Trình bày logic, sơ đồ, ngôn ngữ rõ ràng | **10đ** |
| **7. Video thuyết minh** (không bắt buộc) | — | — |

---

## 🧩 Khung Ý Tưởng — Gợi ý 3 hướng tiếp cận

### Ý TƯỞNG A: "VoiceOne" — Trợ lý giọng nói cho bộ phận một cửa

| Mục | Mô tả |
|-----|-------|
| **Vấn đề** | Người dân (đặc biệt người già, người khuyết tật) gặp khó khăn khi tra cứu thủ tục hành chính do giao diện phức tạp, ngôn ngữ hành chính khó hiểu. Cán bộ một cửa quá tải vì phải hướng dẫn lặp đi lặp lại. |
| **Giải pháp** | Kiosk/Webapp tích hợp **giao tiếp hoàn toàn bằng giọng nói**: người dân nói → Speech-to-Text → Smartbot xử lý → Text-to-Speech trả lời. Tích hợp OCR để scan CCCD tự động điền thông tin. |
| **API cốt lõi** | VNPT SmartVoice (STT/TTS), VNPT Smartbot, VNPT eKYC (OCR) |
| **Đối tượng** | Người dân đến giao dịch tại bộ phận một cửa (ưu tiên người cao tuổi, người khuyết tật) |
| **Điểm khác biệt** | Voice-first, zero UI, hỗ trợ tiếng địa phương, offline mode |

### Ý TƯỞNG B: "AutoCheck" — Kiểm tra & xử lý hồ sơ thông minh

| Mục | Mô tả |
|-----|-------|
| **Vấn đề** | Cán bộ một cửa phải kiểm tra thủ công từng hồ sơ giấy tờ, đối chiếu thông tin, kiểm tra tính hợp lệ — mất nhiều thời gian, dễ sai sót. |
| **Giải pháp** | Hệ thống AI scan hồ sơ → OCR bóc tách → đối chiếu với cơ sở dữ liệu → đánh giá tính hợp lệ → xếp loại ưu tiên xử lý. Tích hợp eKYC để xác thực người nộp. |
| **API cốt lõi** | VNPT SmartReader (OCR, bóc tách), VNPT eKYC (Liveness, Compare face), vnFace |
| **Đối tượng** | Cán bộ bộ phận một cửa tại UBND các cấp |
| **Điểm khác biệt** | Auto-validate, auto-classify, phát hiện giấy tờ giả, tích hợp camera |

### Ý TƯỞNG C: "CivicSense" — Đo lường hài lòng & cải tiến liên tục

| Mục | Mô tả |
|-----|-------|
| **Vấn đề** | Không có công cụ đo lường mức độ hài lòng của người dân theo thời gian thực; các khảo sát giấy tờ thủ công, chậm, thiếu khách quan. |
| **Giải pháp** | Camera AI tại quầy giao dịch → phân tích cảm xúc khuôn mặt (SmartVision) + phân tích phản hồi trên MXH (vnSocial) → dashboard trực quan (SmartUX) → gợi ý cải tiến cho lãnh đạo. |
| **API cốt lõi** | VNPT SmartVision (nhận diện khuôn mặt, phát hiện người), vnSocial (phân tích cảm xúc), VNPT SmartUX |
| **Đối tượng** | Lãnh đạo UBND, Sở, ban ngành |
| **Điểm khác biệt** | Real-time sentiment, AI vision analytics, tự động sinh báo cáo đề xuất |


---

## 🎯 QUYẾT ĐỊNH CHỌN Ý TƯỞNG

Trong 3 ý tưởng (VoiceOne, AutoCheck, CivicSense), **chọn VoiceOne** vì:
1. **Phù hợp đề bài nhất**: Kết hợp giọng nói + nhận diện + xử lý hồ sơ, bao phủ đúng 3 pain-point BTC gợi ý
2. **Tận dụng nhiều API VNPT nhất**: SmartVoice, Smartbot, eKYC, SmartVision — thể hiện rõ "Vì sao chọn VNPT"
3. **Tác động xã hội rõ nhất**: Hướng đến người già, người khuyết tật — nhóm yếu thế trong tiếp cận DVC
4. **Khác biệt lớn nhất**: Voice-first + Vision là tổ hợp chưa có trên thị trường

---

## 📝 Task 1: Trang bìa & Thông tin đội thi

**File:** `hackaithon-de-tai-6-vong-1/proposal.docx`

- [ ] **Step 1: Soạn trang bìa**

> Mở Google Docs / Word. Tạo trang bìa với nội dung:
>
> **DỰ THI HACKATHON ĐỔI MỚI SÁNG TẠO 2026**
>
> **Đề tài 6:** Ứng dụng trí tuệ nhân tạo (AI) nhằm nâng cao năng suất xử lý hồ sơ, thủ tục hành chính cho cơ quan nhà nước
>
> ---
>
> **Tên sản phẩm:** VoiceOne — Trợ lý giọng nói thông minh cho bộ phận một cửa
>
> **Bảng thi:** Bảng B (Challenger)
>
> **Đội thi:** [Tên đội]
>
> **Thành viên:**
> 1. [Họ tên] — [Vai trò, e.g., PM/AI Developer]
> 2. [Họ tên] — [Vai trò]
> 3. [Họ tên] — [Vai trò]
> 4. [Họ tên] — [Vai trò]
> 5. [Họ tên] — [Vai trò]
>
> **Ngày nộp:** 16/06/2026

- [ ] **Step 2: Thiết kế logo đội thi**

> Dùng Canva (free) hoặc Figma thiết kế logo đơn giản:
> - Tên đội + biểu tượng micro/giọng nói
> - Xuất PNG nền trong suốt → `assets/logo-team.png`

- [ ] **Step 3: Chèn logo vào proposal**

> Chèn logo vào header trang bìa, phía trên cùng, căn giữa. Kích thước: 200x200px.

- [ ] **Step 4: Commit**

```bash
git add hackaithon-de-tai-6-vong-1/proposal.docx hackaithon-de-tai-6-vong-1/assets/logo-team.png
git commit -m "task-1: add cover page and team info"
```

---

## 📝 Task 2: Đặt vấn đề (Problem Statement)

**File:** `hackaithon-de-tai-6-vong-1/proposal.docx`
**Tiêu chí:** Tính phù hợp đề bài (25đ — chung Task 2 & 3)
**Độ dài:** 2-3 trang

- [ ] **Step 1: Viết Problem Statement — 3 Pain-points**

> Thêm section "1. Đặt vấn đề" sau trang bìa. Soạn nội dung:
>
> **1.1 Bối cảnh**
>
> Chuyển đổi số hành chính công là nhiệm vụ trọng tâm của Chính phủ giai đoạn 2026-2030. Cổng Dịch vụ công Quốc gia đã đạt hơn 4.000 thủ tục hành chính trực tuyến, nhưng tỷ lệ người dân sử dụng còn thấp (~30%) do rào cản công nghệ và giao diện phức tạp.
>
> **1.2 Ba Pain-point chính**
>
> | # | Pain-point | Minh chứng | Đối tượng chịu ảnh hưởng |
> |:-:|-----------|-----------|:-------------------------:|
> | **PP1** | Ngôn ngữ hành chính phức tạp, khó tra cứu | Khảo sát: 65% người >60 tuổi không tự tra cứu được thủ tục online (Nguồn: Bộ TT&TT 2025) | Người già, người khuyết tật, người yếu công nghệ |
> | **PP2** | Số hóa hồ sơ chưa triệt để, nhập liệu thủ công | Mỗi giao dịch mất 20-30 phút nhập liệu + kiểm tra giấy tờ (Nguồn: UBND TP.HCM 2025) | Cán bộ một cửa |
> | **PP3** | Cán bộ một cửa quá tải, hướng dẫn lặp lại | 1 cán bộ tiếp ~50-70 lượt/ngày, 60% là hướng dẫn thủ tục (Nguồn: Khảo sát nội bộ) | Cán bộ một cửa, người dân chờ đợi lâu |

- [ ] **Step 2: Phân tích "Tại sao là AI"**

> **1.2 Tại sao AI là giải pháp cho vấn đề này?**
>
> Ba pain-point trên đều có thể giải quyết bằng AI:
> - **PP1 → Xử lý ngôn ngữ tự nhiên (NLP):** Voice + Smartbot giúp người dân **nói** thay vì gõ, hiểu ngôn ngữ tự nhiên thay vì thuật ngữ hành chính
> - **PP2 → Thị giác máy tính (Computer Vision):** OCR + eKYC tự động nhận dạng giấy tờ, điền form, xác thực — loại bỏ nhập liệu thủ công
> - **PP3 → Tự động hóa quy trình (Intelligent Automation):** AI xử lý các câu hỏi lặp lại, chỉ chuyển cán bộ khi cần can thiệp — giảm tải 40%
>
> **Công nghệ AI của VNPT** được chọn vì:
> - Đã được huấn luyện sẵn trên dữ liệu tiếng Việt
> - API sẵn sàng, triển khai nhanh (no-code AI)
> - Đáp ứng tiêu chuẩn bảo mật của cơ quan nhà nước

- [ ] **Step 3: Dẫn dắt sang giải pháp**

> **1.3 Từ vấn đề đến giải pháp**
>
> Xuất phát từ thực tế đó, chúng tôi đề xuất **VoiceOne** — trợ lý ảo đa kênh (Kiosk + Web + Mobile) cho phép người dân tương tác hoàn toàn bằng giọng nói với hệ thống dịch vụ công. VoiceOne kết hợp **4 công nghệ AI cốt lõi** của VNPT: Xử lý giọng nói (SmartVoice), Hiểu ngôn ngữ (Smartbot), Nhận dạng giấy tờ (eKYC/SmartReader), và Phân tích hình ảnh (SmartVision) — tạo nên một trải nghiệm **không chạm, không gõ, không rào cản**.

- [ ] **Step 4: Commit**

```bash
git add hackaithon-de-tai-6-vong-1/proposal.docx
git commit -m "task-2: add problem statement with 3 pain-points and AI rationale"
```

---

## 📝 Task 3: Giải pháp chi tiết

**File:** `hackaithon-de-tai-6-vong-1/proposal.docx`
**Tiêu chí:** Chung với Task 2 (25đ)
**Độ dài:** 3-4 trang

- [ ] **Step 1: Mô tả tổng quan giải pháp**

> **VoiceOne là gì?**
>
> VoiceOne là một trợ lý ảo đa kênh (Kiosk + Web + Mobile), cho phép người dân **tương tác hoàn toàn bằng giọng nói** với hệ thống dịch vụ công. Khác với chatbot text hiện tại, VoiceOne hiểu và trả lời bằng giọng nói tiếng Việt, hướng dẫn thủ tục từng bước, tự động điền thông tin từ CCCD qua camera, và đánh giá mức độ hài lòng sau giao dịch.

- [ ] **Step 2: Bảng tính năng core**

| Tính năng | Mô tả | API VNPT |
|-----------|-------|----------|
| **Voice Tra cứu** | Người dân nói → STT → Smartbot xử lý → TTS trả lời | SmartVoice (STT, TTS), Smartbot |
| **Voice Khai báo** | Người dân nói → STT → tự động tạo đơn yêu cầu | SmartVoice (STT) |
| **Scan & Auto-fill** | Scan CCCD → OCR bóc tách → tự động điền form | eKYC (OCR) |
| **Xác thực danh tính** | So sánh khuôn mặt với ảnh trên CCCD | eKYC (Compare, Liveness) |
| **Đánh giá hài lòng** | Camera phân tích cảm xúc → báo cáo | SmartVision (face) |

- [ ] **Step 3: User Scenario — câu chuyện Ông A**

> **Scenario:** Ông Nguyễn Văn A (65 tuổi) đến UBND phường làm thủ tục xác nhận tình trạng hôn nhân
>
> 1. Ông A đến Kiosk VoiceOne tại sảnh
> 2. Camera phát hiện người → chào bằng giọng nói
> 3. Ông A nói: "Tôi muốn làm giấy xác nhận tình trạng hôn nhân"
> 4. STT → Smartbot nhận diện ý định → TTS: "Mời bác đưa CCCD vào khay scan"
> 5. Ông A đưa CCCD → OCR lấy thông tin → Compare face xác thực
> 6. TTS xác nhận thông tin → Ông A trả lời → tự động điền form
> 7. Hệ thống kiểm tra hợp lệ → thông báo kết quả
> 8. Camera phân tích cảm xúc → ghi nhận mức độ hài lòng

- [ ] **Step 4: Giải thích vai trò AI components**

> - **STT**: Chuyển giọng nói tiếng Việt thành văn bản, hỗ trợ giọng địa phương
> - **TTS**: Chuyển văn bản thành giọng nói tự nhiên, thân thiện
> - **Smartbot**: Nhận diện ý định, tra cứu thủ tục, trả lời chính xác
> - **OCR (eKYC/SmartReader)**: Nhận dạng và bóc tách thông tin giấy tờ
> - **Face Recognition**: Xác thực danh tính + phân tích cảm xúc


### Task 4: Thiết kế tổng quan (Architecture & Wireframe)

**Files:**
- `hackaithon-de-tai-6-vong-1/proposal.docx` (giải thích kiến trúc)
- `hackaithon-de-tai-6-vong-1/assets/architecture-diagram.png`
- `hackaithon-de-tai-6-vong-1/assets/user-flow.png`
- `hackaithon-de-tai-6-vong-1/assets/wireframe-voice-interface.png`

- [ ] **Step 1: Vẽ sơ đồ kiến trúc tổng thể**

> Mở app.diagrams.net (draw.io). Tạo sơ đồ khối 4 tầng, dùng hình chữ nhật bo góc, màu sắc phân biệt:
>
> **Tầng 1 — User Layer** (xanh lá): [Kiosk Touchscreen] [Web App] [Mobile App]
>
> **Tầng 2 — AI Core / VNPT API Layer** (xanh dương):
> [SmartVoice STT] [SmartVoice TTS] [Smartbot NLP/Intent]
> [eKYC OCR] [eKYC Liveness] [eKYC Compare]
> [SmartReader Doc AI] [SmartVision Face/Sentiment]
>
> **Tầng 3 — Processing Layer** (cam):
> [Voice Gateway] [Intent Engine] [Doc Processor] [Sentiment Analyzer]
>
> **Tầng 4 — Data Layer** (tím):
> [PostgreSQL: CSDL DVC + Người dùng + Logs]
> [Redis Cache: session + cache thủ tục]
> [Knowledge Base: thủ tục HC, biểu mẫu]
>
> Vẽ mũi tên 2 chiều giữa các tầng. Chú thích "API VNPT" ở Tầng 2.
> Xuất PNG → `assets/architecture-diagram.png` (≥1200x800px, ≥150dpi)

- [ ] **Step 2: Vẽ User Flow flowchart**

> Dùng draw.io vẽ flowchart:
> - Oval: "Người dân đến Kiosk" → Rectangle: "Camera phát hiện → Phát giọng chào"
> - Diamond: "Chọn tương tác?" → [Touch màn hình] / [Giọng nói]
> - Rectangle: "Micro → STT → Smartbot nhận diện ý định"
> - Diamond: "Cần giấy tờ?"
>   - Có: "Hướng dẫn đưa CCCD → Scan → OCR → eKYC Compare"
>   - Không: "TTS trả lời kết quả"
> - Rectangle: "Xác nhận → Camera phân tích cảm xúc"
> - Oval: "Kết thúc. Log phiên giao dịch"
>
> Xuất PNG → `assets/user-flow.png` (≥150dpi)

- [ ] **Step 3: Vẽ Wireframe (3 màn hình) trên Figma**

> Dùng Figma thiết kế:
>
> **Màn hình 1 — Chào:** Header logo + tên UBND. Center: icon micro lớn (120px) + text "Xin chào! Hãy nói yêu cầu của bác ạ". Footer: 3 nút [Tra cứu thủ tục] [Khai báo hồ sơ] [Hướng dẫn]. Font sans-serif 24-32px, tương phản cao.
>
> **Màn hình 2 — Hội thoại:** Header "Đang nghe..." + micro xanh nhấp nháy. Body: waveform + text STT real-time. Footer: [Nói lại] + [Xác nhận].
>
> **Màn hình 3 — Dashboard:** Menu trái [Tổng quan] [Hồ sơ] [Báo cáo] [Cài đặt]. Main: 4 Cards metric (Tổng GD / Đang xử lý / Hoàn thành / Hài lòng) + Line chart + Bảng hồ sơ gần đây.
>
> Xuất PNG → `assets/wireframe-voice-interface.png` (≥150dpi)

- [ ] **Step 4: Viết giải thích kiến trúc & wireframe vào proposal.docx**

> Thêm section "4. Thiết kế tổng quan". Soạn nội dung:
>
> **4.1 Kiến trúc hệ thống**
>
> VoiceOne được thiết kế theo mô hình **microservices 4 tầng**, đảm bảo khả năng mở rộng và bảo trì độc lập:
>
> - **Tầng Người dùng:** Đa kênh — Kiosk, Web App, Mobile App. Tất cả hỗ trợ voice-first.
> - **Tầng AI Core:** Tích hợp API VNPT — SmartVoice (STT/TTS), Smartbot (NLP), eKYC (OCR/Liveness/Compare), SmartVision (Face/Sentiment). Đã được VNPT huấn luyện tiếng Việt, không tốn chi phí train.
> - **Tầng Xử lý:** Voice Gateway quản lý phiên, Intent Engine route yêu cầu, Doc Processor validate OCR, Sentiment Analyzer tổng hợp điểm hài lòng.
> - **Tầng Dữ liệu:** PostgreSQL (giao dịch, người dùng, logs), Redis (cache session, thủ tục), Knowledge Base (quy trình nghiệp vụ).
>
> **4.2 Giao diện người dùng**
>
> Thiết kế theo nguyên tắc **tối giản, font lớn, tương phản cao** — phù hợp người già và người khiếm thị:
> - Tương phản màu ≥ 4.5:1
> - Font sans-serif ≥ 18px
> - Nút bấm ≥ 48x48px
> - Hỗ trợ phím tắt và điều khiển giọng nói
>
> Dashboard cán bộ dùng card KPI + biểu đồ xu hướng + bảng danh sách, giúp theo dõi hiệu suất real-time.

- [ ] **Step 5: Commit**

```bash
git add hackaithon-de-tai-6-vong-1/proposal.docx hackaithon-de-tai-6-vong-1/assets/architecture-diagram.png hackaithon-de-tai-6-vong-1/assets/user-flow.png hackaithon-de-tai-6-vong-1/assets/wireframe-voice-interface.png
git commit -m "task-4: add architecture diagram, user flow, wireframes and explanation"
```


### Task 5: Tính khả thi (Feasibility)

**File:** `hackaithon-de-tai-6-vong-1/proposal.docx`
**Tiêu chí:** Tính khả thi (25đ)
**Độ dài:** 2 trang

- [ ] **Step 1: Viết nội dung nguồn dữ liệu & Nhân lực**

> Thêm section "5. Tính khả thi". Soạn nội dung:
>
> **5.1 Nguồn dữ liệu**
>
> | Yếu tố | Mô tả |
> |--------|-------|
> | Dữ liệu huấn luyện | API VNPT có sẵn, không cần train thêm. Thủ tục HC từ Cổng DVC Quốc gia (dữ liệu mở) |
> | Dữ liệu vận hành | Người dùng cung cấp trong phiên giao dịch — bảo mật theo Nghị định 13/2023 |
> | Dữ liệu thủ tục | Crawl từ Cổng DVC Quốc gia (api.dichvucong.gov.vn) — dữ liệu mở, cập nhật thường xuyên |
>
> **5.2 Nhân lực**
>
> | Vai trò | Số lượng | Kỹ năng chính |
> |---------|:--------:|--------------|
> | Project Manager | 1 | Agile/Scrum, quản lý rủi ro |
> | AI Developer | 1 | Python, REST API, xử lý ngôn ngữ tự nhiên |
> | Fullstack Developer | 1 | React/Vue, Node.js, PostgreSQL, Docker |
> | UI/UX Designer | 1 | Figma, thiết kế cho người già/khuyết tật |
> | Business Analyst | 1 | Nghiệp vụ hành chính công, quy trình một cửa |

- [ ] **Step 2: Viết nội dung kỹ thuật build/deploy**

> **5.3 Kiến trúc kỹ thuật**
>
> - **Frontend:** React (Next.js) + TypeScript — Tối ưu cho Kiosk (màn hình cảm ứng) và Web. Thư viện: Tailwind CSS, React Query, Web Speech API (fallback).
> - **Backend:** Node.js (Express) hoặc Python (FastAPI) — RESTful API, WebSocket cho real-time voice streaming.
> - **AI Services:** Kết nối API VNPT qua HTTP/gRPC. Mỗi API được wrapper trong service layer riêng, dễ test và thay thế.
> - **Database:** PostgreSQL (dữ liệu chính) + Redis (cache session, cache thủ tục).
> - **DevOps:** Docker containerization → Deploy lên AWS EC2 hoặc VNPT Cloud. CI/CD với GitHub Actions (build → test → deploy).
>
> **5.4 Kế hoạch MVP 7 ngày (Vòng 2)**
>
> | Ngày | Công việc | Kết quả |
> |:----:|-----------|---------|
> | 1-2 | Setup dự án + Tích hợp SmartVoice STT/TTS | Có thể ghi âm → text và TTS cơ bản |
> | 3-4 | Tích hợp Smartbot Intent + eKYC OCR | Nhận diện ý định + scan CCCD ra text |
> | 5-6 | Xây dựng UI Kiosk + Dashboard + Luồng hội thoại | Giao diện cơ bản + luồng hoàn chỉnh |
> | 7 | End-to-end test + Fix bug + Đóng gói | MVP deploy được |

- [ ] **Step 3: Viết nội dung chi phí hạ tầng & vận hành**

> **5.5 Chi phí vận hành (dự kiến)**
>
> | Hạng mục | Chi phí tháng (VNĐ) | Ghi chú |
> |----------|:-------------------:|---------|
> | Server (2 VPS 4GB RAM) | ~1.000.000 | AWS EC2 t3.medium / VNPT Cloud |
> | API VNPT sử dụng | ~500.000 - 2.000.000 | Tùy số lượng request |
> | Domain + SSL | ~200.000 | .gov.vn hoặc .vn |
> | DevOps tools (GitHub, Docker) | Miễn phí | GitHub Free / Docker Free |
> | **Tổng vận hành** | **~1.700.000 - 3.200.000** | ~$70-130/tháng |
> | Chi phí setup Kiosk (phần cứng) | 15.000.000 - 25.000.000 | Màn hình cảm ứng 22" + case + camera |
>
> So với giải pháp tư vấn CNTT truyền thống (50-100 triệu/tháng), VoiceOne tiết kiệm **≥90% chi phí vận hành**.

- [ ] **Step 4: Viết nội dung An toàn bảo mật & Pháp lý**

> **5.6 An toàn bảo mật & Tuân thủ pháp lý**
>
> | Yêu cầu | Giải pháp |
> |---------|-----------|
> | Bảo vệ dữ liệu cá nhân | Tuân thủ Nghị định 13/2023/NĐ-CP — mã hóa AES-256, TLS 1.3 |
> | Xác thực điện tử | eKYC đáp ứng Nghị định 59/2022/NĐ-CP — Liveness detection |
> | An toàn thông tin | Tuân thủ Luật An toàn thông tin mạng 2015 — Audit log, phân quyền |
> | Giao dịch điện tử | Tuân thủ Luật Giao dịch điện tử 2005 |
> | Minh bạch | Log phiên giao dịch (audio + text + kết quả) — phục vụ kiểm tra |

- [ ] **Step 5: Viết nội dung Lộ trình sau cuộc thi**

> **5.7 Lộ trình phát triển**
>
> ```
> Tháng 1-2: MVP → Pilot tại 1-2 UBND phường
> Tháng 3-4: Feedback → Cải tiến → Scale lên quận/huyện
> Tháng 5-6: Tích hợp Cổng DVC Quốc gia → Public beta
> Tháng 7-12: Mở rộng tỉnh → Hợp tác VNPT
> ```

- [ ] **Step 6: Commit**

```bash
git add hackaithon-de-tai-6-vong-1/proposal.docx
git commit -m "task-5: add feasibility with data sources, tech stack, costs, compliance and roadmap"
```

### Task 6: Tính đổi mới & Khác biệt (Innovation)

**File:** `hackaithon-de-tai-6-vong-1/proposal.docx`
**Tiêu chí:** Tính đổi mới và khác biệt (20đ)
**Độ dài:** 1.5 trang

- [ ] **Step 1: Viết bảng so sánh với giải pháp hiện tại**

> Thêm section "6. Tính đổi mới & Khác biệt". Soạn nội dung:
>
> **6.1 So sánh với giải pháp hiện tại**
>
> | Tiêu chí | Chatbot DVC/Zalo hiện tại | VoiceOne |
> |-----------|--------------------------|----------|
> | Tương tác chính | Text (gõ bàn phím) | **Voice (giọng nói)** |
> | Hỗ trợ người già/khuyết tật | Hạn chế — cần gõ, đọc chữ | **Có — giao tiếp hoàn toàn bằng giọng nói** |
> | Xác thực danh tính | Thủ công (OTP/SĐT) | **AI — eKYC + Face Compare (tự động)** |
> | Điền form tự động | Không — người dân tự nhập | **Có — OCR + auto-fill từ CCCD** |
> | Đo lường hài lòng | Khảo sát giấy thụ động (cuối tháng) | **Real-time — camera AI phân tích cảm xúc** |
> | Tiếng địa phương | Không hỗ trợ | **Hỗ trợ (SmartVoice STT đa vùng miền)** |
> | Kênh tương tác | Web + Zalo | **Kiosk + Web + Mobile** |
>
> **Kết luận:** VoiceOne có **6/7** tiêu chí vượt trội, tương ứng **~85% khác biệt** so với giải pháp hiện tại — vượt xa ngưỡng 30% yêu cầu.

- [ ] **Step 2: Viết phân tích 4 điểm đổi mới cốt lõi**

> **6.2 Bốn điểm đổi mới cốt lõi**
>
> **1. Voice-first + Vision — Chưa có trên thị trường**
>
> Không có giải pháp nào tại Việt Nam kết hợp cả nhận dạng giọng nói (Voice) và thị giác máy tính (Vision) trong cùng một luồng nghiệp vụ cho bộ phận một cửa. VoiceOne là giải pháp đầu tiên cho phép người dân vừa **nói** để tra cứu, vừa được **nhận diện khuôn mặt và giấy tờ** tự động.
>
> **2. Zero UI — Loại bỏ rào cản công nghệ**
>
> Người dân không cần chạm, không cần gõ, không cần hiểu giao diện. Chỉ cần nói — VoiceOne làm phần còn lại. Điều này đặc biệt quan trọng với người cao tuổi (chiếm ~15% dân số) và người khuyết tật.
>
> **3. Vòng phản hồi tự động — Cải tiến liên tục dựa trên dữ liệu**
>
> Camera AI không chỉ xác thực danh tính mà còn phân tích cảm xúc khuôn mặt sau giao dịch. Dữ liệu này được tổng hợp thành báo cáo hài lòng theo thời gian thực, giúp lãnh đạo ra quyết định cải tiến dựa trên bằng chứng.
>
> **4. Orchestration đa API VNPT — Tận dụng tối đa hệ sinh thái**
>
> VoiceOne tích hợp **4 API VNPT** trong một luồng nghiệp vụ thống nhất: SmartVoice (STT/TTS) + Smartbot (NLP) + eKYC (OCR/Compare/Liveness) + SmartVision (Face/Sentiment). Đây là sự kết hợp chưa từng có, tạo giá trị cộng hưởng.

- [ ] **Step 3: Commit**

```bash
git add hackaithon-de-tai-6-vong-1/proposal.docx
git commit -m "task-6: add innovation analysis with comparison table and 4 USPs"
```

### Task 7: Tác động dự kiến (Expected Impact)

**File:** `hackaithon-de-tai-6-vong-1/proposal.docx`
**Tiêu chí:** Tác động dự kiến (20đ)
**Độ dài:** 2 trang

- [ ] **Step 1: Viết nội dung TAM-SAM-SOM**

> Thêm section "7. Tác động dự kiến". Soạn nội dung:
>
> **7.1 Phân tích thị trường (TAM-SAM-SOM)**
>
> | Chỉ số | Giá trị | Cách tính | Nguồn |
> |--------|---------|-----------|-------|
> | **TAM** (Tổng thị trường) | ~15.000 tỷ VNĐ | Chi tiêu CNTT hành chính công 63 tỉnh, ~240 tỷ/tỉnh/năm | Bộ TT&TT 2025 |
> | **SAM** (Thị trường khả dụng) | ~500 tỷ VNĐ | Mảng AI + tự động hóa cho bộ phận một cửa cấp phường/xã (3-5% TAM) | Phân tích nội bộ |
> | **SOM** (Thị trường đạt được) | ~25 tỷ VNĐ | 5% SAM trong 2 năm đầu (~50-100 UBND quận/huyện) | Dự báo thận trọng |

- [ ] **Step 2: Viết nội dung lợi ích xã hội**

> **7.2 Lợi ích xã hội**
>
> | Lợi ích | Chỉ số | Giải thích |
> |---------|:------:|------------|
> | Giảm thời gian giao dịch | **Giảm 70%** | Từ 20-30 phút xuống 5-7 phút nhờ tự động nhập liệu + xác thực |
> | Người già/khuyết tật tự giao dịch được | **Tăng độ phủ 95%** | Voice + Zero UI giúp nhóm yếu thế tiếp cận DVC |
> | Giảm tải cán bộ | **Giảm 40%** | AI xử lý 60% câu hỏi lặp lại |
> | Minh bạch hóa | **100% giao dịch được log** | Audio + text + video — phòng chống tiêu cực |
> | Tăng hài lòng | **72% → 90%** | Nhờ giảm thời gian chờ + hỗ trợ tận tình |

- [ ] **Step 3: Viết nội dung mô hình doanh thu**

> **7.3 Mô hình doanh thu (B2G Subscription)**
>
> | Gói | Giá (VNĐ/tháng) | Dịch vụ |
> |-----|:--------------:|---------|
> | **Basic** | 5.000.000 | 1 cửa, 500 giao dịch/tháng, hỗ trợ 8h/ngày |
> | **Pro** | 15.000.000 | Đa cửa (tối đa 5), không giới hạn, hỗ trợ 24/7 |
> | **Enterprise** | Theo yêu cầu | Tùy chỉnh, tích hợp riêng, SLA cam kết |
>
> **Phí triển khai ban đầu:** 30-50 triệu đồng/điểm (Kiosk + camera + setup)
>
> **Dự báo tài chính:**
> - Hòa vốn: 12 tháng với 20 KH Gói Basic (doanh thu ~100 triệu/tháng)
> - ROI 3 năm: ~300% (tăng trưởng 10-15 KH mới/quý sau năm 1)

- [ ] **Step 4: Commit**

```bash
git add hackaithon-de-tai-6-vong-1/proposal.docx
git commit -m "task-7: add expected impact with TAM-SAM-SOM, social benefits and revenue model"
```

### Task 8: Chất lượng hồ sơ & Xuất PDF (Proposal Quality)

**File:** `hackaithon-de-tai-6-vong-1/proposal.docx` → `hackaithon-de-tai-6-vong-1/proposal.pdf`
**Tiêu chí:** Chất lượng hồ sơ (10đ)

- [ ] **Step 1: Kiểm tra cấu trúc tổng thể**

> Mở proposal.docx, rà soát toàn bộ tài liệu. Kiểm tra:
>
> - [ ] **Trang bìa:** Có đủ tên sản phẩm, tên đội, thành viên, bảng thi, ngày nộp
> - [ ] **Mục lục (Table of Contents):** Word → References → Table of Contents → Auto Table. Đảm bảo các heading được style đúng (Heading 1, Heading 2)
> - [ ] **Section đánh số:** 1. Đặt vấn đề, 2. Giải pháp, 3. Kiến trúc, 4. Tính khả thi, 5. Đổi mới, 6. Tác động, 7. Kết luận
> - [ ] **Header/Footer:** Header: tên đội + "VoiceOne". Footer: số trang (trang X / tổng Y)
> - [ ] **Kết luận:** Thêm section "Kết luận" cuối cùng, tóm tắt 3 ý: (1) VoiceOne giải quyết 3 pain-point, (2) Khác biệt ~85%, (3) Kêu gọi đầu tư/hợp tác

- [ ] **Step 2: Kiểm tra hình ảnh & biểu đồ**

> - [ ] **Sơ đồ kiến trúc:** Rõ ràng, font chữ trong ảnh ≥ 10pt, đúng 4 tầng, có chú thích màu sắc
> - [ ] **Wireframe:** 3 màn hình đúng tỷ lệ, mock data hợp lý. Có chú thích Figure 1, Figure 2, Figure 3
> - [ ] **Bảng so sánh:** Đầy đủ, có tiêu đề Table 1, Table 2...
> - [ ] **Chất lượng ảnh:** Tất cả PNG ≥ 150dpi, không bể hình, không background trắng thừa
> - [ ] **Đồng bộ màu sắc:** Màu chủ đạo (xanh dương VNPT) nhất quán giữa các hình

- [ ] **Step 3: Kiểm tra ngôn ngữ & thể thức**

> - [ ] **Văn phong:** Mạch lạc, lập luận logic. Mỗi section có: mở đầu → luận điểm → bằng chứng/số liệu → kết luận
> - [ ] **Chính tả:** Chạy Word Spellcheck (Review → Spelling & Grammar). Sửa hết lỗi đỏ/xanh
> - [ ] **Thuật ngữ:** Nhất quán — "VoiceOne" (không "Voice one", "voice one"), "SmartVoice", "eKYC", "bộ phận một cửa" (không "bộ phận 1 cửa")
> - [ ] **Số liệu:** Kiểm tra lại tất cả con số: 25đ, 20đ, ~15.000 tỷ, 5.000.000 VNĐ/th... khớp giữa các phần
> - [ ] **Thể thức:** Đúng quy định Vòng 1 — không quá 20 trang, font Times New Roman 13 hoặc tương đương

- [ ] **Step 4: Xuất PDF**

> - Google Docs: File → Download → PDF Document (.pdf)
> - Word: File → Save As → PDF
> - Mở file PDF kiểm tra:
>   - Font hiển thị đúng (không lỗi font tiếng Việt)
>   - Hình ảnh hiển thị đầy đủ, không bể
>   - Table of Contents có hyperlink hoạt động
>   - Dung lượng ≤ 20MB

- [ ] **Step 5: Commit**

```bash
git add hackaithon-de-tai-6-vong-1/proposal.docx hackaithon-de-tai-6-vong-1/proposal.pdf
git commit -m "task-8: finalize proposal quality check and export PDF"
```

### Task 9: Video thuyết minh (Khuyến khích)

**File:** Video 2-3 phút, YouTube Unlisted (link ghi trong Proposal Phụ lục)

- [ ] **Step 1: Viết kịch bản chi tiết**

> Soạn script cho video, đọc với tốc độ chậm (~140 từ/phút):
>
> **Phần 1: Giới thiệu (0:00-0:20)**
>
> "Xin chào BTC và ban giám khảo. Chúng tôi là đội [Tên đội], đến từ [Đơn vị]. Hôm nay chúng tôi xin giới thiệu sản phẩm **VoiceOne** — trợ lý giọng nói thông minh cho bộ phận một cửa."
>
> *Hiển thị: Logo đội + tên sản phẩm*
>
> **Phần 2: Vấn đề (0:20-0:50)**
>
> "Hãy tưởng tượng một người già 65 tuổi đến UBND phường làm thủ tục. Họ được đưa đến một cái máy tính với đầy chữ, đầy thuật ngữ hành chính. Họ không biết bắt đầu từ đâu. Đó là thực tế của **65% người trên 60 tuổi** tại Việt Nam — không thể tự tra cứu thủ tục online."
>
> "Ba pain-point chính: Một — ngôn ngữ hành chính phức tạp. Hai — nhập liệu thủ công mất 20-30 phút mỗi giao dịch. Ba — cán bộ một cửa quá tải vì phải hướng dẫn lặp đi lặp lại."
>
> *Hiển thị: Hình ảnh người già trước máy tính + biểu đồ 65%*
>
> **Phần 3: Giải pháp (0:50-1:30)**
>
> "VoiceOne giải quyết tất cả bằng AI. Người dân chỉ cần **nói** — VoiceOne làm phần còn lại. Công nghệ gồm bốn API VNPT: SmartVoice cho nhận dạng và tổng hợp giọng nói, Smartbot cho hiểu ngôn ngữ tự nhiên, eKYC cho nhận dạng giấy tờ và xác thực khuôn mặt, SmartVision cho phân tích cảm xúc."
>
> *Hiển thị: Sơ đồ kiến trúc 4 tầng*
>
> **Phần 4: Demo (1:30-2:30)**
>
> "Hãy theo chân Ông Nguyễn Văn A — 65 tuổi — đến làm thủ tục xác nhận tình trạng hôn nhân."
>
> "Bước 1: Camera phát hiện Ông A → Kiosk chào bằng giọng nói.
> Bước 2: Ông A nói 'Tôi muốn làm giấy xác nhận tình trạng hôn nhân' → STT chuyển thành text → Smartbot nhận diện ý định.
> Bước 3: Hệ thống yêu cầu đưa CCCD → Scan → OCR tự động điền form.
> Bước 4: Camera xác thực khuôn mặt với ảnh trên CCCD.
> Bước 5: Hệ thống kiểm tra hợp lệ → thông báo kết quả bằng giọng nói.
> Bước 6: Camera phân tích cảm xúc → ghi nhận hài lòng."
>
> "Toàn bộ quy trình chỉ **5-7 phút** thay vì 20-30 phút như hiện nay."
>
> *Hiển thị: Wireframe 3 màn hình + User Flow*
>
> **Phần 5: Kết luận (2:30-3:00)**
>
> "VoiceOne không chỉ là một sản phẩm công nghệ — đó là cầu nối đưa dịch vụ công đến gần hơn với mọi người dân, đặc biệt là người già và người khuyết tật."
>
> "Với chi phí chỉ từ 5 triệu đồng/tháng, VoiceOne giúp giảm 70% thời gian giao dịch, giảm 40% tải cho cán bộ, và tăng hài lòng từ 72% lên 90%."
>
> "Chúng tôi kêu gọi sự hợp tác của VNPT và các cơ quan nhà nước để đưa VoiceOne đến mọi bộ phận một cửa trên cả nước. Xin cảm ơn!"
>
> *Hiển thị: Logo đội + slogan + thông tin liên hệ*

- [ ] **Step 2: Chuẩn bị slides trình chiếu**

> Dùng Google Slides / PowerPoint tạo 5-6 slide tương ứng 5 phần script:
> - Slide 1: Logo + tên đội + tên sản phẩm
> - Slide 2: Hình ảnh minh họa + biểu đồ 65% (3 pain-point)
> - Slide 3: Sơ đồ kiến trúc 4 tầng
> - Slide 4: User Flow + Wireframe 3 màn hình
> - Slide 5: Bảng KPI (70%, 40%, 72%→90%) + Logo + cảm ơn

- [ ] **Step 3: Quay & dựng**

> - **Quay màn hình:** OBS Studio (free). Cài đặt: 1920x1080, 30fps, mic + desktop audio
> - **Thu âm:** Đọc script theo slide, giọng rõ ràng, tốc độ chậm
> - **Dựng:** CapCut (free) — Ghép audio + slide + hiệu ứng chuyển cảnh
> - **Phụ đề:** Thêm phụ đề tiếng Việt tự động bằng CapCut (Text → Auto Captions)
> - **Nhạc nền:** Nhạc nhẹ không lời, volume -15dB so với giọng đọc

- [ ] **Step 4: Upload & Ghi link**

> - YouTube → Upload → Đặt chế độ **Unlisted**
> - Copy link video
> - Mở proposal.docx → Thêm **Phụ lục** cuối cùng với nội dung:
>
> > **Phụ lục: Video thuyết minh**
> >
> > Link: [YouTube URL]
> >
> > Thời lượng: 2-3 phút

- [ ] **Step 5: Commit**

```bash
git add hackaithon-de-tai-6-vong-1/proposal.docx
git commit -m "task-9: add video demo link to proposal appendix"
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

## 📅 Timeline Overall

| Hạn | Công việc | Task |
|:--:|-----------|:----:|
| 10/06 | Chốt ý tưởng (chọn 1 trong 3) | — |
| 11/06 | Trang bìa + Thông tin đội | Task 1 |
| 12/06 | Đặt vấn đề + Giải pháp | Task 2, 3 |
| 13/06 | Kiến trúc + Wireframe | Task 4 |
| 14/06 | Tính khả thi + Đổi mới + Tác động | Task 5, 6, 7 |
| 15/06 | Hoàn thiện hồ sơ + Kiểm tra | Task 8 |
| 15/06 | Quay video (khuyến khích) | Task 9 |
| **16/06** | **NỘP HỒ SƠ** | — |

## 🛡️ Self-Review Checklist

- [ ] **1. Spec Coverage:**
  - [ ] Bám sát đề tài 6: "cơ quan nhà nước nâng cao năng suất xử lý hồ sơ"
  - [ ] Đề cập 3 pain-point (ngôn ngữ phức tạp, số hóa chưa 100%, cán bộ quá tải)
  - [ ] Giải pháp gợi ý từ BTC (giọng nói, khai thông tin, nộp bản mềm, camera)
  - [ ] Đầy đủ cấu trúc hồ sơ Vòng 1 theo Thể lệ

- [ ] **2. Placeholder scan:** Không có TBD, TODO, implement later

- [ ] **3. Consistency:** Tên sản phẩm (VoiceOne) nhất quán, API reference đúng tên

- [ ] **4. Task completeness:** 9 task bao phủ tất cả yêu cầu Vòng 1

---

---

## 🚀 PHASE 2: DMUX PARALLEL EXECUTION PLAN

**Mục tiêu:** Hoàn thiện Tasks 3-9 song song, tối ưu thời gian từ 11/06 → 16/06.
**Công cụ:** dmux (tmux pane manager) + git worktrees + Python scripts

### 📊 Dependency Graph

```
T1[Trang bìa] → T2[Đặt vấn đề] → T3[Giải pháp] → T5[Tính khả thi]
                                    ├──→ T4[Kiến trúc+Wireframe]
                                    ├──→ T6[Đổi mới]
                                    └──→ T7[Tác động]
T4,T5,T6,T7 → T8[Hoàn thiện+PDF] → T9[Video - optional]
```

### 📌 Chiến lược Parallel

| Worker | Task | Script tạo | File ghi vào |
|--------|------|:----------:|:------------:|
| **A** | Task 3: Giải pháp | `add_section3.py` | proposal.docx §2 |
| **B** | Task 4: Kiến trúc + Assets | `add_section4.py` + 3 PNG | proposal.docx §3 + assets/ |
| **C** | Task 5: Tính khả thi | `add_section5.py` | proposal.docx §4 |
| **D** | Task 6: Đổi mới & Khác biệt | `add_section6.py` | proposal.docx §5 |
| **E** | Task 7: Tác động dự kiến | `add_section7.py` | proposal.docx §6 |
| **F** | Task 8: Hoàn thiện + PDF | `finalize_proposal.py` | proposal.docx + proposal.pdf |

**Nguyên tắc:** Viết script song song → Chạy script tuần tự (vì cùng ghi vào 1 file docx).
>
> ---

### 🪟 STEP 1: Setup Worktrees

```bash
cd /run/media/sanng/New\ Volume/HACKAITHON

# Tạo 6 worktrees — mỗi worker 1 nhánh riêng
for branch in section3 section4-assets section5 section6 section7 finalize; do
  git worktree add -b worker/$branch ../wt-$branch HEAD
done

# Seed file proposal.docx hiện tại vào tất cả worktrees
for wt in ../wt-*/; do
  mkdir -p "$wt/hackaithon-de-tai-6-vong-1"
  cp hackaithon-de-tai-6-vong-1/proposal.docx "$wt/hackaithon-de-tai-6-vong-1/"
done
```

---

### 🪟 STEP 2: Triển khai DMUX Session

```bash
# Khởi tạo tmux session với 6 pane
tmux new-session -s hackaithon -d

# Pane 0 (Main orchestrator): giữ nguyên
# Split thành 5 pane con
tmux split-window -h -t hackaithon:0.0
tmux split-window -v -t hackaithon:0.0
tmux split-window -v -t hackaithon:0.1
tmux split-window -v -t hackaithon:0.0
tmux split-window -v -t hackaithon:0.2

# Pane 0: Main Orchestrator
tmux send-keys -t hackaithon:0.0 \
  "cd /run/media/sanng/New\ Volume/HACKAITHON && echo 'Orchestrator ready'" Enter

# Pane 1: Worker A — Task 3: Giải pháp
tmux send-keys -t hackaithon:0.1 \
  "cd ../wt-section3/hackaithon-de-tai-6-vong-1 && touch add_section3.py && echo 'Worker A ready'" Enter

# Pane 2: Worker B — Task 4: Assets + Kiến trúc
tmux send-keys -t hackaithon:0.2 \
  "cd ../wt-section4-assets/hackaithon-de-tai-6-vong-1 && echo 'Worker B ready'" Enter

# Pane 3: Worker C — Task 5: Tính khả thi
tmux send-keys -t hackaithon:0.3 \
  "cd ../wt-section5/hackaithon-de-tai-6-vong-1 && echo 'Worker C ready'" Enter

# Pane 4: Worker D — Task 6: Đổi mới
tmux send-keys -t hackaithon:0.4 \
  "cd ../wt-section6/hackaithon-de-tai-6-vong-1 && echo 'Worker D ready'" Enter

# Pane 5: Worker E — Task 7: Tác động
tmux send-keys -t hackaithon:0.5 \
  "cd ../wt-section7/hackaithon-de-tai-6-vong-1 && echo 'Worker E ready'" Enter

# Attach vào session để làm việc
tmux attach -t hackaithon
```

---

### 📝 STEP 3: Worker Scripts Specifications

Mỗi worker viết 1 Python script, chạy độc lập trên `proposal.docx` của worktree mình.

#### Worker A — `add_section3.py` (Task 3: Giải pháp chi tiết)
```
Section: "2. GIẢI PHÁP"
- 2.1 Tổng quan giải pháp — VoiceOne là gì? (paragraph)
- 2.2 Tính năng core (table: 5 rows × 3 cols: Tính năng | Mô tả | API VNPT)
- 2.3 User Scenario — Câu chuyện Ông A (8 bước có numbering)
- 2.4 Vai trò AI Components (5 bullets: STT, TTS, Smartbot, OCR, Face Recognition)
```

#### Worker B — `add_section4.py` + Assets (Task 4: Kiến trúc & Wireframe)
```
Section: "3. THIẾT KẾ TỔNG QUAN"
- 3.1 Kiến trúc hệ thống (paragraph + diagram)
- 3.2 Giao diện người dùng (paragraph + wireframe images)

Assets cần tạo:
- assets/architecture-diagram.png (vẽ bằng Pillow hoặc lưu bằng draw.io)
- assets/user-flow.png
- assets/wireframe-voice-interface.png
```

#### Worker C — `add_section5.py` (Task 5: Tính khả thi)
```
Section: "4. TÍNH KHẢ THI"
- 4.1 Nguồn dữ liệu (table: 3 rows)
- 4.2 Nhân lực (table: 5 roles)
- 4.3 Kiến trúc kỹ thuật (paragraph: Frontend, Backend, AI, DB, DevOps)
- 4.4 Kế hoạch MVP 7 ngày (table: 7 rows)
- 4.5 Chi phí vận hành (table: 5 items ~1.7-3.2M/tháng)
- 4.6 An toàn bảo mật & Pháp lý (table: 5 rows)
- 4.7 Lộ trình phát triển (paragraph: 4 giai đoạn)
```

#### Worker D — `add_section6.py` (Task 6: Đổi mới & Khác biệt)
```
Section: "5. TÍNH ĐỔI MỚI & KHÁC BIỆT"
- 5.1 So sánh với giải pháp hiện tại (table: 7 tiêu chí × 3 cols)
- 5.2 Bốn điểm đổi mới cốt lõi (4 subsection: Voice+Vision, Zero UI, Feedback loop, Multi-API orchestration)
```

#### Worker E — `add_section7.py` (Task 7: Tác động dự kiến)
```
Section: "6. TÁC ĐỘNG DỰ KIẾN"
- 6.1 TAM-SAM-SOM (table: 3 rows)
- 6.2 Lợi ích xã hội (table: 5 rows)
- 6.3 Mô hình doanh thu (table: 3 gói Basic/Pro/Enterprise + dự báo tài chính)
```

#### Worker F — `finalize_proposal.py` (Task 8: Hoàn thiện + PDF)
```
- Thêm mục lục tự động (Table of Contents)
- Thêm Header: "VoiceOne — Đội thi [Tên đội]"
- Thêm Footer: số trang "Trang X / Tổng Y"
- Thêm Section "7. KẾT LUẬN" (tóm tắt 3 ý)
- Kiểm tra hình ảnh, font, style
- Xuất PDF → proposal.pdf
```

---

### ⏭️ STEP 4: Execution Pipeline

**Phase A — Parallel** (dmux: 5 workers cùng lúc → ~15 phút)
```
[Pane 1] Worker A: viết add_section3.py + chạy thử
[Pane 2] Worker B: vẽ assets + viết add_section4.py
[Pane 3] Worker C: viết add_section5.py
[Pane 4] Worker D: viết add_section6.py
[Pane 5] Worker E: viết add_section7.py
```

**Gate 1:** Kiểm tra từng script chạy được
```bash
python3 -m py_compile add_section{3,4,5,6,7}.py
```

**Phase B — Sequential** (Orchestrator chạy)
```bash
# Merge tất cả worktrees
for branch in section3 section4-assets section5 section6 section7; do
  git merge worker/$branch
done

# Copy assets từ worktree B
cp ../wt-section4-assets/hackaithon-de-tai-6-vong-1/assets/* ./hackaithon-de-tai-6-vong-1/assets/

# Chạy tuần tự (vì cùng modify 1 file docx)
python3 hackaithon-de-tai-6-vong-1/add_section3.py
python3 hackaithon-de-tai-6-vong-1/add_section4.py
python3 hackaithon-de-tai-6-vong-1/add_section5.py
python3 hackaithon-de-tai-6-vong-1/add_section6.py
python3 hackaithon-de-tai-6-vong-1/add_section7.py
```

**Gate 2:** Verify proposal.docx có đủ 6 sections
```bash
python3 -c "
from docx import Document
doc = Document('hackaithon-de-tai-6-vong-1/proposal.docx')
texts = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
for s in ['GIẢI PHÁP','THIẾT KẾ','KHẢ THI','ĐỔI MỚI','TÁC ĐỘNG']:
    print(f'[{\"OK\" if any(s in t for t in texts) else \"MISSING\"}] {s}')
"
```

**Phase C — Finalize** (Orchestrator)
```bash
python3 hackaithon-de-tai-6-vong-1/finalize_proposal.py
# Mở proposal.docx kiểm tra thủ công
# File → Save As → PDF
```

**Gate 3:** PDF ≤20MB, font không lỗi, có mục lục, đủ hình ảnh

**Phase D — Video** (Task 9, optional)
- OBS quay màn hình → CapCut dựng → YouTube Unlisted

---

### ✅ STEP 5: Commit Strategy

```bash
# Sau mỗi worker hoàn thành (trong worktree)
git add add_section*.py assets/*.png
git commit -m "task-<N>: <nội dung>"

# Sau Phase B (merge vào main)
git add hackaithon-de-tai-6-vong-1/
git commit -m "task-3-7: add sections 2-6 with assets"

# Sau Phase C
git add hackaithon-de-tai-6-vong-1/proposal.pdf
git commit -m "task-8: finalize proposal and export PDF"

# Sau Phase D (nếu có)
git add hackaithon-de-tai-6-vong-1/proposal.docx
git commit -m "task-9: add video appendix"
```

---

### 🧹 Cleanup

```bash
# Dọn worktrees
for wt in ../wt-*/; do git worktree remove "$wt"; done
git worktree prune

# Dọn branches
for branch in section3 section4-assets section5 section6 section7 finalize; do
  git branch -D worker/$branch
done

# Tắt tmux session
tmux kill-session -t hackaithon 2>/dev/null
```

---

### 📋 Timeline Updated

| Ngày | Công việc | Phương thức |
|:----:|-----------|:-----------:|
| 11/06 | ✅ Task 1: Trang bìa | Đã xong |
| 11/06 | ✅ Task 2: Đặt vấn đề | Đã xong |
| **11-12/06** | **🔥 Tasks 3-7: Song song (dmux 5 workers)** | **PARALLEL** |
| 12/06 | Task 8: Hoàn thiện + Xuất PDF | Sequential |
| 12-15/06 | Task 9: Video (khuyến khích) | Sequential |
| **16/06** | **🚀 NỘP HỒ SƠ** | — |

> **Tiết kiệm ~3 ngày so với kế hoạch tuần tự nhờ dmux parallel execution.**
