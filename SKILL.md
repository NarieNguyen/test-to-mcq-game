---
name: test-to-mcq-game
description: >-
  Kỹ năng tự động tạo game ôn tập trắc nghiệm HTML tương tác All-in-One chuẩn Unit 3 Test bằng bộ công cụ game-kit. Kích hoạt ngay lập tức khi người dùng yêu cầu "làm game", "tạo game", "làm game mới", "game-kit", hoặc gửi kèm file đề bài kiểm tra. Tự động xử lý ảnh/audio, tạo game.json, biên dịch qua build_game.py, kiểm thử 0 lỗi và lưu sao lưu vào thư mục 3/.
---

# Kỹ Năng Tự Động Tạo Game Trắc Nghiệm Tương Tác chuẩn `game-kit`

## 🎯 CÂU LỆNH KÍCH HOẠT NHANH (TRIGGER):
Khi người dùng chỉ cần nhắn ngắn gọn:
- **"làm game"**
- **"tạo game"**
- **"làm game mới"**
- hoặc gửi file đề (PDF, Word, ảnh, audio) kèm lời nhắn ngắn gọn

👉 **AI TỰ ĐỘNG THỰC HIỆN TOÀN BỘ QUY TRÌNH DƯỚI ĐÂY MÀ KHÔNG CẦN HỎI LẠI BẤT KỲ ĐIỀU GÌ.**

---

## ⚡ NGUYÊN TẮC CỐT LÕI (BẤT BIẾN)
1. **KHÔNG BAO GIỜ sửa tay file `game-kit/engine/engine.html`**. Khung giao diện, CSS màu xanh Sky Blue, thanh ray xe đua 🚗, đồng hồ tròn SVG 90s, modal bắt buộc nhập tên học sinh và Bảng vàng VIP Certificate đã được đóng băng cố định.
2. Mọi game mới chỉ gồm:
   - Thư mục chứa bài (ví dụ `De_Moi/` hoặc thư mục làm việc).
   - File `game.json` tuân theo chuẩn schema trong [game-kit/docs/GAME_SPEC.md](file:///c:/Users/Admin/Downloads/Game/game-kit/docs/GAME_SPEC.md).
   - Thư mục `media/` chứa ảnh WebP/PNG/JPG cắt từ đề và audio MP3.
3. Trình biên dịch [game-kit/tools/build_game.py](file:///c:/Users/Admin/Downloads/Game/game-kit/tools/build_game.py) tự động:
   - Kiểm tra lỗi dữ liệu.
   - Băm đáp án bằng thuật toán `cyrb53` + muối `wtg_v2_2026`.
   - Mã hóa Base64 UTF-8 cho lời giải thích (`e`) và đáp án mẫu (`full`).
   - Nén ảnh sang WebP ($\le 900px, quality 82$).
   - Nhúng audio MP3 Base64 và ráp vào `engine.html`.
   - Sinh ra **1 FILE HTML DUY NHẤT** (All-in-One).
4. **Nguyên tắc nội dung**: Cách làm (giao diện, luật chấm, quy trình) giữ nguyên chuẩn `game-kit`; nhưng **toàn bộ nội dung** (tiêu đề, câu hỏi, đáp án, giải thích, bài đọc, ảnh, audio, mốc nghe) **chỉ lấy từ file đề mới được giao**. Ví dụ mẫu `unit3_test` chỉ để tham khảo cấu trúc định dạng, tuyệt đối không sao chép nội dung câu hỏi sang đề mới.

---

## 🛠️ WORKFLOW CHUYÊN DỤNG CHO ĐỀ PDF TOÀN ẢNH & AUDIO RỜI

Khi người dùng gửi **đề dạng PDF toàn ảnh scan/chụp** + **file nghe rời**:
👉 Xem chi tiết tại [game-kit/docs/PIPELINE_PDF_AUDIO.md](file:///c:/Users/Admin/Downloads/Game/game-kit/docs/PIPELINE_PDF_AUDIO.md) và sử dụng bộ công cụ hỗ trợ tại `game-kit/workflow/`:

1. **Xuất các trang PDF ra ảnh độ phân giải cao**:
   - `pdftoppm -r 100 -png de.pdf $WORK/pages/p` (xem nội dung & toạ độ 100dpi)
   - `pdftoppm -r 200 -png de.pdf $WORK/hi/p` (cắt ảnh sắc nét gấp đôi)
2. **Phân tích Audio**:
   - Chạy `python workflow/asr.py '*Part_4*.mp3'` hoặc `build_game.py --suggest-marks` để lấy bản chép lời thô và mốc giây.
   - Mục nào chưa chắc chắn, ghi lại danh sách để người dùng nghe xác nhận.
3. **Viết script generator tự động với `game-kit/workflow/common.py`** (tham khảo `workflow/examples/mk_unit_mau.py`):
   - `u.crop(trang, (x0, y0, x1, y1), 'ten')`: cắt ảnh câu hỏi/bài đọc.
   - `u.grid(trang, [box...], 'ten', cols=3)`: ghép nhiều ô tranh nhỏ thành 1 ảnh lưới.
   - `u.quad(trang, y0, y1, x0, x1, 'ten')`: ghép hàng 4 tranh nhỏ thành lưới 2×2 cho bài "odd one out".
   - `u.audio('*Part_4*.mp3', 'part4')`: chuẩn hoá audio mono 64k.
   - `place(dung, [sai...])`: tự động xáo trộn và phân bổ đều đáp án đúng vào A, B, C, D (~25%).
   - `u.save({'sections': sec})`: tự động xuất file `game.json` chuẩn schema.
4. **Thẩm định thị giác với `workflow/sheet.py`**:
   - Chạy `python workflow/sheet.py <Unit> 1 3 4 5 8 10 12` để tạo ảnh ghép toàn diện các phần thi, duyệt trực quan đảm bảo không lỗi cắt tranh, không lộ đáp án.

---

## 📋 QUY TRÌNH THỰC HIỆN TỰ ĐỘNG

### Bước 1: Khảo sát đề bài & Chuẩn bị tài nguyên
- Đọc nội dung đề bài (từ PDF, Word docx, hoặc văn bản người dùng cung cấp).
- Cắt và trích xuất ảnh câu hỏi vào thư mục `media/` (ảnh sắc nét, tối ưu dung lượng).
- Nếu có file audio bài nghe:
  - Sao chép vào thư mục `media/`.
  - Có thể chạy: `python game-kit/tools/build_game.py --suggest-marks media/audio.mp3` để lấy gợi ý các mốc thời gian quãng lặng cho từng câu hỏi.

### Bước 2: Soạn thảo `game.json` chuẩn schema
Soạn `game.json` với cấu trúc:
```jsonc
{
  "id": "ma_bai_viet_thuong_khong_dau",
  "title": "Tên Đề Bài Đầy Đủ (Ví dụ: Unit 4 Test: My Day)",
  "badge": "Luyện Thi Học Kỳ · Tiếng Anh 4 · Windy Bui",
  "tag": "Tiếng Anh 4 · Unit 4",
  "mascot": "Cú Giáo Sư",
  "champTitle": "Thần Đồng Tiếng Anh",
  "settings": {
    "secondsPerQuestion": 90,
    "basePoints": 100,
    "maxSpeedBonus": 50,
    "speechLang": "en-US"
  },
  "sections": [
    {
      "id": "part1",
      "icon": "📝",
      "title": "Part 1. Look and choose the correct answer",
      "desc": "Mô tả phần thi",
      "items": [
        {
          "prompt": "1. Look at picture a...",
          "img": "media/img01.webp",
          "options": ["A. Monday", "B. Tuesday", "C. Wednesday", "D. Thursday"],
          "answer": "A. Monday",
          "explain": "Lời giải thích chi tiết bằng tiếng Việt."
        }
      ]
    }
  ]
}
```

### Bước 3: Quy đổi các dạng bài tập về Trắc nghiệm (2–4 lựa chọn)
Tuân thủ tuyệt đối bảng quy đổi tại Mục 5 của [GAME_SPEC.md](file:///c:/Users/Admin/Downloads/Game/game-kit/docs/GAME_SPEC.md):
- **Nhìn tranh tick ô**: Cung cấp `img` + 4 đáp án (đáp án đúng + 3 nhiễu hợp lý).
- **Điền từ vào câu có khung từ**: Cung cấp `wordBank: ["word1", "word2", ...]` + 4 options chọn từ khung.
- **Đúng / Sai (True / False)**: 2 lựa chọn `["True (✓)", "False (✗)"]`.
- **Đoạn văn đọc hiểu**: Dùng `passage: { "kind": "reading", "header": "...", "paragraphs": [...] }`.
- **Điền từ vào đoạn văn**: Dùng `passage: { "kind": "blanks", "header": "...", "paragraphs": ["... {1} ... {2} ..."] }` kèm `wordBank`.
- **Hội thoại**: Dùng `passage: { "kind": "dialogue", "lines": [{"who": "Nam", "text": "..."}, ...] }`.
- **Sắp xếp câu**: 1 câu đúng trật tự + 3 câu xáo trộn sai kiểu học sinh hay mắc.
- **Nghe**: Gắn `audio: "media/partX.mp3"`, mốc `audioMarks`, và `audioAt` theo từng câu.

### Bước 4: Biên dịch Game HTML
Chạy lệnh biên dịch:
```bash
python game-kit/tools/build_game.py <duong_dan_game.json> -o <Ten_File_Game>.html
```
- Phải đảm bảo kết quả in ra: **0 LỖI (✘)**.
- Phân bổ đáp án A, B, C, D phải cân đối đều (~25%), không bị lệch dồn cục $>50\%$.

### Bước 5: Tự động sao lưu & Kiểm thử
1. **Sao lưu**: Luôn luôn tự động copy 1 bản sang thư mục sao lưu:
   ```powershell
   Copy-Item "<Ten_File_Game>.html" -Destination "3/<Ten_File_Game>.html" -Force
   ```
2. **Kiểm tra**:
   - File tồn tại ở cả thư mục gốc và `3/` với kích thước byte bằng nhau.
   - Thử nghiệm chức năng chạy mượt mà.

### Bước 6: Báo cáo kết quả cho người dùng
Gửi bảng tóm tắt:
- Tên bài thi, số lượng câu hỏi, số phần thi, file ảnh & audio nhúng.
- Xác nhận trạng thái sao lưu tại thư mục `3/`.
- Link trực tiếp đến file HTML để người dùng mở xem ngay.
