# Data Flow — Luồng Dữ liệu

GovOne có **2 luồng dữ liệu chính** hoạt động song song: Voice-first cho người dân và OCR pipeline cho cán bộ.

## Luồng 1: Citizen Voice-First

```
CÔNG DÂN
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 1: TIẾP NHẬN                                               │
│ Camera phát hiện người → SmartVoice TTS: "Xin chào! Bác cần gì?"│
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 2: VOICE INPUT                                             │
│ Người dân nói → Micro → SmartVoice STT → text (độ chính xác>95%)│
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 3: INTENT PROCESSING                                       │
│ Smartbot NLP: phân tích ý định → xác định thủ tục cần làm        │
│ Intent Engine: route đến đúng workflow xử lý                     │
└───────┬─────────────────────┬───────────────────────────────────┘
        │                     │
        ▼                     ▼
  ┌──────────┐        ┌──────────────┐
  │ Cần giấy │        │ Không cần    │
  │ tờ?      │        │ giấy tờ      │
  └────┬─────┘        └──────┬───────┘
       │                     │
       ▼                     ▼
┌──────────────────┐  ┌──────────────────┐
│ BƯỚC 4: eKYC     │  │ BƯỚC 5: TTS     │
│ Scan CCCD → OCR  │  │ TTS đọc kết quả  │
│ Face compare     │  │ tra cứu          │
│ Liveness check   │  └──────────────────┘
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 5: AUTO-FILL                                               │
│ OCR data → map vào form → hiển thị để công dân xác nhận          │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 6: SUBMIT                                                 │
│ Công dân xác nhận → Submit form → Lưu HoSo (DB)                 │
│ → Sinh mã hồ sơ → Gửi thông báo đến cán bộ                      │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 7: SENTIMENT                                               │
│ SmartVision: phân tích biểu cảm khuôn mặt → ghi nhận hài lòng   │
│ → Lưu vào DB → Dashboard cán bộ cập nhật real-time              │
└──────────────────────────────────────────────────────────────────┘
```

### Dữ liệu đầu vào/ra — Citizen Flow

| Bước | Input | Output | Công nghệ |
|---|---|---|---|
| 1 | Camera frame | Người detected + TTS greeting | SmartVision Face, SmartVoice TTS |
| 2 | Audio stream (16kHz mono) | Text tiếng Việt | SmartVoice STT |
| 3 | Text query | Intent + parameters | Smartbot NLP |
| 4 | Ảnh CCCD + face | OCR data + match score | eKYC OCR, Compare, Liveness |
| 5 | OCR fields + form template | Pre-filled form JSON | Field mapping engine |
| 6 | Form JSON | HoSo record (DB) | HoSo Service |
| 7 | Camera frame | Sentiment score (0-100) | SmartVision Sentiment |

---

## Luồng 2: Officer OCR Pipeline

```
CÁN BỘ
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 1: NẠP HỒ SƠ                                              │
│ Scan từ máy scanner / Upload file PDF, JPG, PNG                 │
│ → Lưu raw file vào MinIO → Tạo HoSoTaiLieu record               │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 2: PHÂN LOẠI                                              │
│ SmartVision Classification: nhận diện loại giấy tờ               │
│ → CCCD, CMND, sổ hộ khẩu, giấy khai sinh, bằng cấp, hóa đơn... │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 3: OCR & BÓC TÁCH                                         │
│ SmartReader OCR: nhận dạng text (>95%)                          │
│ SmartReader Doc AI: bóc tách thông tin có cấu trúc              │
│ → JSON fields: {hoten, ngaysinh, cccd, diachi...}              │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│ BƯỚC 4: ĐỐI CHIẾU                                              │
│ eKYC OCR: extract CCCD từ ảnh → so sánh với DB dân cư           │
│ Rules Engine: kiểm tra logic (họ tên khớp? ngày sinh hợp lệ?)   │
│ → Kết quả: KHOP / CANH_BAO / LOI                                │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
              ┌──────────┐    ┌──────────────┐
              │ KHOP     │    │ CANH BAO/LOI │
              └────┬─────┘    └──────┬───────┘
                   │                 │
                   ▼                 ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│ BƯỚC 5a: DUYỆT          │  │ BƯỚC 5b: SỬA / BỔ SUNG  │
│ Cán bộ kiểm tra → Duyệt │  │ Dashboard hiện cảnh báo  │
│ → HoSo status: DA_XU_LY │  │ → Sửa thủ công hoặc     │
└──────────────────────────┘  │ yêu cầu bổ sung         │
                              └──────────────────────────┘
```

### Dữ liệu đầu vào/ra — Officer Flow

| Bước | Input | Output | Công nghệ |
|---|---|---|---|
| 1 | File scan (PDF/JPG/PNG) | Raw file path (MinIO) + HoSoTaiLieu record | File upload, MinIO |
| 2 | Image byte stream | Document type label | SmartVision Classification |
| 3 | Image byte stream | Structured fields JSON | SmartReader OCR + Doc AI |
| 4 | OCR JSON + CCCD data | Match result (KHOP/CANH_BAO/LOI) | Rules Engine, eKYC |
| 5 | Match result + officer decision | Updated HoSo status (DB) | HoSo Service |

---

## Luồng 3: State Machine Hồ sơ

```
                    ┌──────────────┐
                    │ CHO_TIEP_NHAN│ ← Tạo mới
                    └──────┬───────┘
                           │ Cán bộ nhận
                           ▼
                    ┌──────────────┐
                    │  CHO_XU_LY   │
                    └──────┬───────┘
                           │ Cán bộ bắt đầu xử lý
                           ▼
                    ┌──────────────┐
              ┌─────│ DANG_XU_LY  │─────┐
              │     └──────────────┘     │
              │                         │
              ▼                         ▼
       ┌──────────────┐          ┌──────────────┐
       │  DA_XU_LY    │          │   TU_CHOI    │
       │ (Phê duyệt)  │          │ (Từ chối)    │
       └──────────────┘          └──────────────┘
                                        │
                              ┌──────────────┐
                              │ CHO_BO_SUNG  │
                              │ (Y/c bổ sung)│
                              └──────┬───────┘
                                     │ Công dân bổ sung
                                     ▼
                              ┌──────────────┐
                              │ DA_BO_SUNG   │
                              └──────┬───────┘
                                     │ Trở lại xử lý
                                     └─────────┐
                                               │
                                               ▼
                                        ┌──────────────┐
                                        │   ĐÓNG HS    │
                                        └──────────────┘
```

### Quy tắc chuyển trạng thái

| Từ | Đến | Điều kiện | Actor |
|---|---|---|---|
| CHO_TIEP_NHAN | CHO_XU_LY | Cán bộ tiếp nhận | Officer |
| CHO_XU_LY | DANG_XU_LY | Cán bộ bắt đầu xử lý | Officer |
| DANG_XU_LY | DA_XU_LY | Phê duyệt | Officer |
| DANG_XU_LY | TU_CHOI | Từ chối + lý do | Officer |
| DANG_XU_LY | CHO_BO_SUNG | Yêu cầu bổ sung | Officer |
| CHO_BO_SUNG | DA_BO_SUNG | Công dân nộp bổ sung | Citizen |
| DA_BO_SUNG | DANG_XU_LY | Cán bộ xử lý tiếp | Officer |
