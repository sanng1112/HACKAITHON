# Round 4: Backend - Gọi Models AI (AI/ML Integration Layer)

**Người phụ trách:** Backend Developer 3 (Người D)

---

## Mục tiêu tổng quan

Xây dựng tầng **AI Model Integration** cho hệ thống GovOne - tích hợp các mô hình AI/ML vào quy trình xử lý hồ sơ hành chính công. Round này bao gồm việc tải và chạy các mô hình OCR, STT (Voice), NLP, và các tác vụ AI khác để tự động hoá xử lý giấy tờ.

Hoàn thành Round 4 đồng nghĩa với việc **toàn bộ các tính năng AI hoạt động hoàn chỉnh**, có thể nhận diện giấy tờ, trích xuất thông tin, xử lý giọng nói, và tự động điền form.

---

## 📋 Danh sách công việc chi tiết

### 4.1 Thiết lập môi trường AI/ML

- [ ] Cài đặt thư viện: PyTorch / TensorFlow, transformers, easyocr, whisper, ...
- [ ] Cấu hình GPU (CUDA) support nếu có
- [ ] Thiết lập model cache directory
- [ ] Tạo base class cho tất cả models (load, predict, cleanup)
- [ ] Cấu hình async processing (Celery / Redis Queue) cho tác vụ nặng
- [ ] Tạo API endpoints cho AI processing

### 4.2 Tích hợp OCR (Optical Character Recognition)

**Mục tiêu:** Nhận diện chữ từ hình ảnh giấy tờ (CMND/CCCD, giấy khai sinh, bằng cấp, hoá đơn...)

- [ ] **Tải model OCR**: sử dụng **EasyOCR** hoặc **PaddleOCR** (hỗ trợ tiếng Việt tốt)
- [ ] **Tiền xử lý ảnh**: resize, grayscale, threshold, denoise, deskew
- [ ] **Nhận diện văn bản**: trích xuất text từ ảnh giấy tờ
- [ ] **Nhận diện loại giấy tờ**: phân loại ảnh (CMND, CCCD, bằng lái, ...) bằng CNN classifier
- [ ] **Trích xuất thông tin có cấu trúc**: dùng Regex hoặc NER để lấy:
  - Họ tên, ngày sinh, quê quán
  - Số CMND/CCCD
  - Ngày cấp, nơi cấp
- [ ] **API endpoint**: `POST /api/ai/ocr` (upload ảnh → trả về text + metadata)
- [ ] **Xử lý batch**: cho phép OCR nhiều ảnh cùng lúc
- [ ] **Cache kết quả**: không chạy lại OCR cho ảnh đã xử lý

### 4.3 Tích hợp STT / Voice (Speech-to-Text)

**Mục tiêu:** Chuyển đổi giọng nói thành văn bản, hỗ trợ điền form bằng giọng nói và tra cứu bằng giọng nói

- [ ] **Tải model STT**: sử dụng **OpenAI Whisper** (model `base` hoặc `small` cho tiếng Việt)
- [ ] **Xử lý audio**: kiểm tra định dạng (.wav, .mp3, .m4a), convert nếu cần
- [ ] **Chuyển giọng nói → văn bản**: ghi âm → nhận diện → trả text
- [ ] **API endpoint**: `POST /api/ai/stt` (upload audio → trả về text)
- [ ] **API WebSocket** real-time streaming STT (optional, cho kiosk)
- [ ] **Tự động điền form**: STT → text → map vào các field của form
### 4.4 Tích hợp NLP (Xử lý ngôn ngữ tự nhiên)

**Mục tiêu:** Phân tích và hiểu nội dung văn bản để hỗ trợ xử lý hồ sơ

- [ ] **Tải model NLP**: sử dụng **PhoBERT** (BERT cho tiếng Việt) hoặc **ViT5** / **GPT**
- [ ] **Phân loại nội dung hồ sơ**: tự động xác định loại thủ tục dựa trên nội dung
- [ ] **Trích xuất thực thể (NER)**: lấy thông tin quan trọng từ văn bản (tên, địa chỉ, số điện thoại, ngày tháng...)
- [ ] **Tóm tắt văn bản**: tóm tắt nội dung hồ sơ dài
- [ ] **Kiểm tra chính tả & ngữ pháp**: tự động sửa lỗi trong form
- [ ] **Phân tích cảm xúc/dự đoán**: phân loại mức độ ưu tiên của hồ sơ
- [ ] **API endpoint**: `POST /api/ai/nlp/analyze` (text → phân tích)
- [ ] **API endpoint**: `POST /api/ai/nlp/classify` (text → loại thủ tục)

### 4.5 Tự động điền Form (Auto Form Filling)

**Mục tiêu:** Kết hợp OCR + NLP để tự động điền thông tin vào form hành chính

- [ ] **Pipeline xử lý**: 
  1. Người dùng upload ảnh CMND/CCCD
  2. OCR nhận diện text từ ảnh
  3. NLP trích xuất các field (họ tên, ngày sinh, quê quán, số CCCD)
  4. Tự động điền vào form tương ứng
- [ ] **Map field thông minh**: ánh xạ thông tin trích xuất vào đúng field của form
- [ ] **Xác nhận của người dùng**: hiển thị kết quả để người dùng kiểm tra/sửa trước khi gửi
- [ ] **Fallback**: nếu AI không chắc chắn, đánh dấu và nhờ người dùng nhập tay
- [ ] **API endpoint**: `POST /api/ai/auto-fill` (ảnh → form data)

### 4.6 Xử lý bất đồng bộ (Async Task Processing)

**Mục tiêu:** Các tác vụ AI nặng không block API response

- [ ] Thiết lập **Celery** + **Redis** (Python) hoặc **BullMQ** (Node.js)
- [ ] Task queue cho OCR batch
- [ ] Task queue cho NLP analysis
- [ ] Task queue cho STT processing
- [ ] **Webhook callback**: khi task hoàn thành, gửi kết quả qua webhook
- [ ] **Polling mechanism**: API kiểm tra trạng thái task `GET /api/ai/task/:id`
- [ ] **Timeout & retry**: xử lý khi task thất bại
- [ ] **Progress tracking**: theo dõi tiến độ task (0-100%)

### 4.7 Model Management

- [ ] **Model registry**: quản lý các phiên bản model
- [ ] **Lazy loading**: chỉ load model khi có request đầu tiên
- [ ] **Model health check**: API `GET /api/ai/health` - kiểm tra model đã load chưa
- [ ] **Reload model**: API `POST /api/ai/reload` - reload model khi cập nhật
- [ ] **Model caching**: cache kết quả predict để tránh chạy lại
- [ ] **Graceful degradation**: nếu model không hoạt động, trả về fallback message
- [ ] **Model metrics**: thống kê số lượng request, thời gian xử lý, tỉ lệ thành công

### 4.8 Testing AI Pipeline

- [ ] Unit test cho từng model (load, predict, output format)
- [ ] Integration test cho pipeline (OCR → NLP → auto-fill)
- [ ] Test với ảnh mẫu (CMND, CCCD, giấy tờ các loại)
- [ ] Test với audio mẫu (giọng nói tiếng Việt)
- [ ] Performance test (thời gian xử lý, memory usage)
- [ ] Mock model cho CI/CD (không cần GPU trên CI)

---

## 🧪 Tiêu chí hoàn thành (Definition of Done)

1. ✅ OCR hoạt động với ảnh giấy tờ tiếng Việt (CMND, CCCD, bằng lái...)
2. ✅ STT hoạt động với giọng nói tiếng Việt (tỉ lệ chính xác > 70%)
3. ✅ NLP trích xuất được thông tin có cấu trúc từ văn bản
4. ✅ Auto-fill hoạt động: upload ảnh → tự động điền form
5. ✅ Async task processing không block API (queue + polling/webhook)
6. ✅ Tất cả API endpoints hoạt động với response format chuẩn
7. ✅ Model management: health check, reload, graceful degradation
8. ✅ Có ít nhất 80% unit test coverage cho model services
9. ✅ Tài liệu API (Swagger) cho tất cả AI endpoints

---

## 🚀 Tech Stack đề xuất

- **Framework:** FastAPI / Flask (Python)
- **OCR:** EasyOCR hoặc PaddleOCR (hỗ trợ tiếng Việt tốt)
- **STT:** OpenAI Whisper (small/medium cho tiếng Việt)
- **NLP:** PhoBERT (VietAI), VnCoreNLP, Underthesea
- **DL Framework:** PyTorch
- **Async Tasks:** Celery + Redis
- **Image Processing:** OpenCV, Pillow
- **Audio Processing:** librosa, pydub, ffmpeg
- **Testing:** Pytest
- **Serving:** ONNX Runtime (tối ưu inference)

---

## 🔗 Phụ thuộc (Dependencies)

- **Round 2 (Backend Logic)** cung cấp API để round này gọi khi cần
- **Round 3 (Database)** để lưu kết quả AI processing
- Cần GPU để training/inference nhanh (có thể fallback CPU)
- Có thể làm việc độc lập với mock data ban đầu

---

## 📂 File cần tạo

```
ai-service/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py          # Base class cho tất cả models
│   │   ├── ocr_model.py           # EasyOCR wrapper
│   │   ├── stt_model.py           # Whisper wrapper
│   │   └── nlp_model.py           # PhoBERT wrapper
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ocr_service.py         # Xử lý OCR pipeline
│   │   ├── stt_service.py         # Xử lý STT pipeline
│   │   ├── nlp_service.py         # Xử lý NLP pipeline
│   │   └── auto_fill_service.py   # Auto-fill pipeline
│   ├── api/
│   │   ├── __init__.py
│   │   ├── ocr_router.py
│   │   ├── stt_router.py
│   │   ├── nlp_router.py
│   │   ├── auto_fill_router.py
│   │   └── health_router.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── celery_app.py          # Celery config
│   │   ├── ocr_tasks.py
│   │   ├── stt_tasks.py
│   │   └── nlp_tasks.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── image_utils.py         # Tiền xử lý ảnh
│   │   ├── audio_utils.py         # Xử lý audio
│   │   └── text_utils.py          # Xử lý văn bản
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_ocr.py
│   ├── test_stt.py
│   ├── test_nlp.py
│   └── test_auto_fill.py
├── sample_data/
│   ├── images/                    # Ảnh mẫu cho test
│   └── audio/                     # Audio mẫu cho test
├── main.py
├── Dockerfile                     # GPU-enabled container
└── requirements.txt
```

