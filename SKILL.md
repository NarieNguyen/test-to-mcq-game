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

1. **KHÔNG BAO GIỜ sửa tay file `game-kit/engine/engine.html`**: Khung giao diện, CSS màu xanh Sky Blue, thanh ray xe đua 🚗, đồng hồ tròn SVG 90s, modal bắt buộc nhập tên học sinh và Bảng vàng VIP Certificate đã được đóng băng cố định.
2. **Tiêu chuẩn 4 đáp án (A/B/C/D)**: 
   - Bài test được thiết kế chuẩn hóa 4 lựa chọn (A/B/C/D) cho mọi khối lớp (theo nội dung tài liệu yêu cầu để đảm bảo tính phân hóa học sinh).
   - Bắt buộc dùng hàm `place(dung, [sai1, sai2, sai3])` trong `common.py` để phân bố đều đáp án đúng vào các vị trí A, B, C, D (~25% mỗi vị trí), tuyệt đối không để vị trí nào lệch dồn cục $>50\%$.
3. **Khai thác đầy đủ tính năng Audio Player (`audioMarks` & `audioAt`)**:
   - Ở cấp phần thi nghe (`section`): Bắt buộc khai báo `audioMarks` chứa mốc thời gian bắt đầu của từng câu/số (vd: `[{"label": "Câu 1", "t": 5}, {"label": "Câu 2", "t": 18}, ...]`).
   - Ở từng câu hỏi (`items`): Bắt buộc gán `audioAt: t` tương ứng. Khi học sinh bấm vào câu nào, trình phát audio tự động tua đúng đến phân đoạn đó.
4. **Nén âm thanh chuẩn MP3 — Kiểm soát dung lượng file `< 2.5MB`**:
   - Audio nhúng bắt buộc phải là **MP3 mono 64kbps** (hoặc dùng các file `.mp3` có sẵn trong thư mục).
   - Tuyệt đối không để lọt audio `.wav` thô vào bản build (tránh làm file game phình to lên 4–8MB).
   - Tổng dung lượng file HTML thành phẩm phải luôn **dưới 2.5MB**.
5. **Cấu trúc bài đọc hiểu chuẩn (`passage`)**:
   - Ở các phần đọc hiểu (Part 8...): Bắt buộc sử dụng cấu trúc `passage: { "kind": "reading", "header": "...", "paragraphs": [...], "img": "..." }`.
   - Engine sẽ hiển thị khung đọc cố định song song (Split View) chuyên nghiệp. Tuyệt đối **không copy-paste lặp lại đoạn văn dài vào từng câu hỏi**.
6. **Xử lý hình ảnh trực quan (Kể cả Part 2 Odd One Out)**:
   - Các bài tìm từ khác loại (Odd one out) có tranh: Phải cắt ảnh dạng thẻ hoặc lưới 4 ô bằng `u.quad()` hoặc `u.grid()` để học sinh nhìn tranh chữ trực quan.
7. **Độ trung thực nội dung 100% (Không Hallucination)**:
   - Toàn bộ nội dung (tiêu đề, câu hỏi, đáp án, bài đọc, tranh, audio) lấy trung thực từ file đề được giao. Tuyệt đối không tự bịa bài đọc mới hay câu hỏi suy diễn phức tạp ngoài tài liệu.

---

## 🛠️ WORKFLOW CHUYÊN DỤNG CHO ĐỀ PDF TOÀN ẢNH & AUDIO RỜI

Khi người dùng gửi **đề dạng PDF toàn ảnh scan/chụp** + **file nghe rời**:
👉 Xem chi tiết tại [game-kit/docs/PIPELINE_PDF_AUDIO.md](file:///c:/Users/Admin/Downloads/Game/game-kit/docs/PIPELINE_PDF_AUDIO.md) và sử dụng bộ công cụ hỗ trợ tại `game-kit/workflow/`:

1. **Xuất các trang PDF ra ảnh độ phân giải cao**:
   - `pdftoppm -r 100 -png de.pdf $WORK/pages/p` (xem nội dung & toạ độ 100dpi)
   - `pdftoppm -r 200 -png de.pdf $WORK/hi/p` (cắt ảnh sắc nét gấp đôi)
2. **Phân tích Audio**:
   - Quét tìm file `.mp3` có sẵn hoặc chạy `python workflow/asr.py '*Part_4*.mp3'` hoặc `build_game.py --suggest-marks` để lấy bản chép lời thô và mốc giây.
3. **Viết script generator tự động với `game-kit/workflow/common.py`** (tham khảo `workflow/examples/mk_unit_mau.py`):
   - `u.crop(trang, (x0, y0, x1, y1), 'ten')`: cắt ảnh câu hỏi/bài đọc.
   - `u.grid(trang, [box...], 'ten', cols=3)`: ghép nhiều ô tranh nhỏ thành 1 ảnh lưới.
   - `u.quad(trang, y0, y1, x0, x1, 'ten')`: ghép hàng 4 tranh nhỏ thành lưới 2×2 cho bài "odd one out".
   - `u.audio('*Part_4*.mp3', 'part4')`: chuẩn hoá audio mono 64k (tự động phát hiện và ưu tiên MP3).
   - `place(dung, [sai1, sai2, sai3])`: tự động xáo trộn và phân bổ đều 4 đáp án A, B, C, D (~25%).
   - `u.save({'sections': sec})`: tự động xuất file `game.json` chuẩn schema.
4. **Biên dịch & Thẩm định thị giác**:
   - Chạy `python game-kit/tools/build_game.py $WORK/uX/game.json -o Game_GSX_UnitX_Test.html`
   - Kiểm tra dung lượng file xuất xưởng bảo đảm `< 2.5MB` và 0 lỗi.

---

## 📋 QUY TRÌNH THỰC HIỆN TỰ ĐỘNG (6 BƯỚC KHÉP KÍN)

### Bước 1: Khảo sát đề bài & Chuẩn bị tài nguyên
- Đọc nội dung đề bài (từ PDF, Word docx, hoặc văn bản người dùng cung cấp).
- Cắt và trích xuất ảnh câu hỏi vào thư mục `media/` (ảnh WebP sắc nét, tối ưu dung lượng).
- Lấy file audio MP3 (hoặc nén từ WAV sang MP3 64k), xác định các mốc giây `audioMarks`.

### Bước 2: Soạn thảo `game.json` chuẩn schema
Soạn `game.json` với cấu trúc:
```jsonc
{
  "id": "gs3_u7",
  "title": "GLOBAL SUCCESS - UNIT 7: CLASSROOM INSTRUCTIONS",
  "badge": "Luyện Thi · Global Success",
  "tag": "Global Success 3 · Unit 7",
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
      "id": "part4",
      "icon": "🎧",
      "title": "Part 4. Listening – Listen and tick",
      "desc": "Nghe đoạn hội thoại và chọn bức tranh đúng",
      "audio": "media/part4.mp3",
      "markLabel": "Nhảy đến câu:",
      "audioMarks": [
        {"label": "Câu 1", "t": 3.5},
        {"label": "Câu 2", "t": 11.2}
      ],
      "items": [
        {
          "prompt": "1. Nghe và chọn bức tranh đúng:",
          "img": "media/p4_1.webp",
          "audioAt": 3.5,
          "options": ["A. Stand up", "B. Sit down", "C. Open your book", "D. Close your book"],
          "answer": "A. Stand up",
          "explain": "Bài nghe nói: 'Stand up, please.' → Chọn A."
        }
      ]
    }
  ]
}
```

### Bước 3: Quy đổi các dạng bài tập về Trắc nghiệm 4 lựa chọn (A/B/C/D)
- **Nhìn tranh tick ô**: Cung cấp `img` + 4 đáp án (1 đúng + 3 sai).
- **Điền từ vào câu có khung từ**: Cung cấp `wordBank: ["word1", "word2", ...]` + 4 options chọn từ khung.
- **Đoạn văn đọc hiểu**: Dùng `passage: { "kind": "reading", "header": "...", "paragraphs": [...] }` + 4 options.
- **Điền từ vào đoạn văn**: Dùng `passage: { "kind": "blanks", "header": "...", "paragraphs": ["... {1} ... {2} ..."] }` kèm `wordBank`.
- **Sắp xếp câu**: 1 câu đúng trật tự + 3 câu xáo trộn sai kiểu học sinh hay mắc.
- **Nghe**: Gắn `audio: "media/partX.mp3"`, mốc `audioMarks`, và `audioAt` theo từng câu.

### Bước 4: Biên dịch Game HTML
Chạy lệnh biên dịch:
```bash
python game-kit/tools/build_game.py <duong_dan_game.json> -o <Ten_File_Game>.html
```
- Phải đảm bảo kết quả in ra: **0 LỖI (✘)**.
- Dung lượng file HTML: **< 2.5 MB**.
- Phân bổ đáp án A, B, C, D phải cân đối đều (~25%), không bị lệch dồn cục $>50\%$.

### Bước 5: Tự động sao lưu & Kiểm thử
1. **Sao lưu**: Luôn luôn tự động copy 1 bản sang thư mục sao lưu:
   ```powershell
   Copy-Item "<Ten_File_Game>.html" -Destination "3/<Ten_File_Game>.html" -Force
   ```
2. **Kiểm tra**:
   - File tồn tại ở cả thư mục gốc và `3/` với kích thước byte bằng nhau.
   - Thử nghiệm chức năng chạy mượt mà offline 100%.

### Bước 6: Báo cáo kết quả cho người dùng
Gửi bảng tóm tắt:
- Tên bài thi, số lượng câu hỏi (chuẩn 4 đáp án), số phần thi, file ảnh & audio nhúng.
- Dung lượng file tối ưu (< 2.5MB).
- Xác nhận trạng thái sao lưu tại thư mục `3/`.
- Link trực tiếp đến file HTML để người dùng mở xem ngay.
