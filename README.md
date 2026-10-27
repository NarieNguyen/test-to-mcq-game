# Test to MCQ Game (Skill)

Kỹ năng tự động hóa tạo Game ôn tập trắc nghiệm tương tác HTML All-in-One chuẩn **Unit 3 Test** bằng bộ công cụ **`game-kit`**.

Mọi game được tạo ra đều chạy độc lập 100% offline, tích hợp đầy đủ giao diện Sky Blue, thanh ray xe đua 🚗, đồng hồ SVG đếm ngược 90s, cơ chế chấm điểm bảo mật băm `cyrb53`, kiểm tra phân bổ đáp án đều A-D, modal bắt buộc nhập tên học sinh và Bảng vàng VIP Certificate vinh danh.

---

## 🌟 Tính Năng Nổi Bật

1. **Khóa cứng Engine chuẩn mực (`game-kit/engine/engine.html`)**:
   - Giao diện Cú Giáo Sư 🦉 hiện đại, chuẩn EdTech, tối ưu điện thoại di động (`max-width: 680px`).
   - Thanh ray tiến độ xe đua 🚗 di chuyển theo từng câu hỏi.
   - Đồng hồ đếm ngược SVG 90s đổi 3 sắc thái (Xanh $>50\%$ $\rightarrow$ Vàng $>20\%$ $\rightarrow$ Đỏ nhấp nháy $<20\%$) và thưởng tốc độ tối đa $+50\%$.
   - Modal bắt buộc học sinh điền Họ tên mới được làm bài, hiển thị pill `👤 Họ tên (Lớp)` trên Header để đổi nhanh.

2. **Trình biên dịch All-in-One (`game-kit/tools/build_game.py`)**:
   - Nhận file cấu hình `game.json` và thư mục `media/`.
   - Băm đáp án bằng thuật toán `cyrb53` kết hợp mã muối bí mật `wtg_v2_2026`.
   - Mã hóa Base64 UTF-8 cho lời giải thích chi tiết tiếng Việt và đáp án mẫu.
   - Tự động nén ảnh sang WebP ($\le 900px$, chất lượng 82).
   - Tự động nhúng âm thanh MP3 Base64 và phân tích mốc quãng lặng (`--suggest-marks`).
   - Tự động kiểm tra và cảnh báo nếu đáp án đúng bị lệch quá $50\%$ ở một vị trí.
   - Xuất ra 1 file `.html` duy nhất dung lượng tối ưu (~2–4 MB).

3. **Bộ kiểm thử tự động (`game-kit/tools/test_game.js`)**:
   - Chạy mô phỏng học sinh chơi thật qua `jsdom` với 4 kịch bản ngặt nghèo (làm đúng 100%, làm sai, hết giờ, kiểm tra media và chống lộ đáp án).

---

## 🚀 Hướng Dẫn Sử Dụng Nhanh

### 1. Kích hoạt bằng câu lệnh ngắn gọn
Khi giao việc cho AI Agent, chỉ cần đính kèm file đề bài (PDF / Word / ảnh) và gõ:
```
làm game
```
Hoặc:
```
Làm game mới y như game Unit 3 Test. Đề: <file đề>. Audio: <file audio>.
```

### 2. Biên dịch thủ công qua CLI
```bash
# Gợi ý mốc thời gian audio
python game-kit/tools/build_game.py --suggest-marks media/part4.mp3

# Biên dịch ra file Game HTML
python game-kit/tools/build_game.py game.json -o Game_TA4_Unit4_Test.html

# Kiểm thử với jsdom
cd game-kit/tools && npm i && node test_game.js ../../Game_TA4_Unit4_Test.html
```

### 3. Pipeline xử lý Đề PDF ảnh + Audio rời (`game-kit/workflow/`)
Khi xử lý đề dạng PDF toàn ảnh kèm các đoạn audio nghe:
```bash
# 1. Trích xuất trang PDF (xem ở 100dpi, cắt ở 200dpi)
pdftoppm -r 100 -png de.pdf work/pages/p
pdftoppm -r 200 -png de.pdf work/hi/p

# 2. Phân tích audio thô & mốc thời gian
python game-kit/workflow/asr.py '*Part_4*.mp3'

# 3. Chạy script generator tự động sinh game.json & cắt ảnh media
python work/mk_unit.py

# 4. Ghép ảnh thẩm định thị giác các phần
python game-kit/workflow/sheet.py <Unit_Number> 1 3 4 5 8 10 12
```

---

## 📂 Cấu Trúc Thư Mục

```
test-to-mcq-game/
├── SKILL.md                 # Chỉ dẫn cốt lõi dành cho AI Agent
├── README.md                # Tài liệu tổng quan & hướng dẫn CLI
└── game-kit/
    ├── engine/
    │   └── engine.html      # Khung giao diện & âm thanh đóng băng (không sửa tay)
    ├── tools/
    │   ├── build_game.py    # Compiler: băm cyrb53, nén WebP, nhúng MP3
    │   ├── test_game.js     # Runner kiểm thử jsdom
    │   ├── preview.py       # Chụp ảnh viewport di động Playwright
    │   └── package.json
    ├── docs/
    │   ├── GAME_SPEC.md     # Đặc tả kỹ thuật, schema game.json & quy đổi bài tập
    │   └── PIPELINE_PDF_AUDIO.md # Pipeline chuẩn từ đề PDF ảnh + audio rời
    ├── workflow/
    │   ├── common.py        # Module hỗ trợ: crop, grid, quad, Q, place, Unit
    │   ├── asr.py           # Phân tích audio thô & bắt mốc thời gian
    │   ├── sheet.py         # Ghép ảnh các phần thi để kiểm tra thị giác
    │   └── examples/        # Script generator mẫu (mk_unit_mau.py, mk_unit_mau_2.py)
    ├── BRIEF_TEMPLATE.md    # Mẫu yêu cầu gửi đề
    └── examples/
        └── unit3_test/      # Mẫu chuẩn vàng (game.json + media + HTML)
```

---

## 👤 Tác Giả & Bản Quyền
- Phát triển và đóng gói bởi **NarieNguyen**
- Chuẩn mực EdTech Review Game 2026
