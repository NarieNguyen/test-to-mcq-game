# GAME_SPEC — đặc tả game trắc nghiệm (bản chuẩn "Unit 3 Test")

Mục tiêu: mọi game mới đều **cùng engine, cùng giao diện, cùng luật chấm**. AI chỉ viết `game.json`
(nội dung) + chuẩn bị `media/`; mọi thứ còn lại do `tools/build_game.py` lo. **Không sửa `engine/engine.html`
trừ khi người dùng yêu cầu đổi tính năng cho mọi game.**

> **Nguyên tắc nội dung:** cách làm (giao diện, luật chấm, quy trình) giữ nguyên; **toàn bộ nội dung** (tiêu đề, câu hỏi, đáp án, giải thích, bài đọc, ảnh, audio, mốc nghe, khung từ) chỉ lấy từ file đề MỚI. `examples/unit3_test` chỉ là mẫu về định dạng — tuyệt đối không copy chữ, ảnh, audio hay cách đặt tên phần của nó sang game mới.

## 1. Mặc định cố định (không cần người dùng nhắc lại)

| Hạng mục | Quy định |
|---|---|
| Sản phẩm | 1 file `.html` mở offline, tối ưu điện thoại, nhúng sẵn ảnh/audio |
| Màn hình | Nhập họ tên (bắt buộc) + lớp → chọn "làm toàn bộ" hoặc "vào Mục lục" → làm bài → Bảng Vàng Chứng Nhận |
| Dạng câu | Mọi câu đều quy về **trắc nghiệm 2–4 đáp án** (A–D), kể cả bài "viết từ", "sắp xếp", "điền chỗ trống" |
| Thời gian | 90 giây/câu, vòng tròn đếm ngược xanh → vàng → đỏ; hết giờ = sai + hiện đáp án |
| Điểm | Đúng = 100 + thưởng tốc độ tối đa 50 (theo thời gian còn lại). Điểm hệ 10 = số câu đúng/tổng × 10 |
| Xếp loại | ≥85% 3 sao · ≥65% 2 sao · còn lại 1 sao |
| Sau mỗi câu | Hiện đúng/sai + **đáp án + giải thích tiếng Việt** |
| Tiến độ | Thanh tiến độ có xe 🚗, chạy theo tổng số câu |
| Nghe | Phần có audio: trình phát (±5s, thanh trượt, về đầu), chip nhảy mốc, nút "Nghe đoạn câu N", tự phát khi vào phần |
| Hỗ trợ | Nút 🔊 đọc câu hỏi (giọng máy), khay từ gợi ý (word bank), khối bài đọc / điền khuyết / hội thoại |
| Kết quả | Tên, lớp, ngày giờ, điểm hệ 10, số câu đúng, tổng điểm, **danh sách câu cần ôn** (đề + đáp án + giải thích), nhắc chụp màn hình gửi cô |
| Bảo mật | Đáp án chỉ lưu dạng **băm**, lời giải mã hoá base64 → không đọc được bằng "View Source" thông thường. Không chống được người cố tình viết code (nói rõ khi bàn giao) |
| Tên file | `Game_<Môn><Lớp>_<Unit/Chủ đề>_<Loại>.html` (vd `Game_TA4_Unit3_Test.html`) |

Đổi mặc định cho **một game** → khai trong `settings` của `game.json`. Đổi cho **mọi game** → sửa engine + cập nhật tài liệu này.

## 2. Cấu trúc thư mục một game

```
GameMoi/
  game.json            ← AI viết
  media/               ← ảnh cắt từ đề (png/jpg/webp), audio (mp3/wav/m4a)
```
Build: `python3 tools/build_game.py GameMoi/game.json -o Game_XXX.html`

## 3. Schema `game.json`

```jsonc
{
  "id": "ta4_u3",                          // chữ thường/số/_ ; dùng làm khoá lưu tên HS (localStorage)
  "title": "Unit 3 Test: My Week (Global Success 4)",
  "badge": "Luyện Thi Học Kỳ · Tiếng Anh 4 · Windy Bui",   // dòng nhỏ trên tiêu đề
  "tag": "Global Success 4 · Unit 3",      // nhãn ở màn nhập tên
  "mascot": "Cú Giáo Sư",                  // tuỳ chọn
  "champTitle": "Thần Đồng Tiếng Anh",     // tuỳ chọn: "Xuất Sắc! <champTitle>"
  "settings": { "secondsPerQuestion": 90, "basePoints": 100, "maxSpeedBonus": 50, "speechLang": "en-US" },
  "sections": [ {
      "id": "part4", "icon": "🎧", "title": "Part 4. Listen and tick. Then write", "desc": "6 câu nghe chọn đáp án",
      "audio": "media/part4.mp3",                       // tuỳ chọn
      "markLabel": "Nhảy đến câu:",                     // tuỳ chọn
      "audioMarks": [ {"label":"Câu 1","t":0}, {"label":"Câu 2","t":18} ],   // chip nhảy mốc (giây)
      "wordBank": ["Monday","Friday"],                  // tuỳ chọn: khay từ gợi ý
      "imgStyle": "framed",                             // tuỳ chọn: ảnh có khung (bảng/thời khoá biểu lớn)
      "passage": { ... },                               // tuỳ chọn, xem mục 4
      "items": [ {
          "prompt": "Listen to audio #1. Tick the correct picture: 'It is ____.'",
          "img": "media/img01.webp",                    // tuỳ chọn
          "options": ["a (Monday)", "b (Tuesday)", "Wednesday", "Thursday"],   // 2–4 đáp án
          "answer": "a (Monday)",                       // PHẢI trùng 1 option (không phân biệt hoa/thường, dấu câu)
          "explain": "Bài nghe: 'Today is Monday.' → chọn a.",   // giải thích tiếng Việt, bắt buộc
          "audioAt": 0,                                 // tuỳ chọn: giây bắt đầu đoạn nghe của câu này
          "fullAnswer": "..."                           // tuỳ chọn: chữ hiện ở "Đáp án đúng" (mặc định = answer)
      } ]
  } ]
}
```
- Chữ trong `prompt/options/explain/header/...` là **văn bản thường**; chỉ cho phép thẻ `<b> <i> <u> <br>` (vd gạch chân từ cần hỏi: `<u>Monday</u>`). Ký tự `< > &` khác được tự thoát.
- Không đánh số đầu `prompt` cũng được (engine tự thêm "1.", "2."...). Nếu có "1. " sẵn vẫn ổn.
- Trong 1 câu, các đáp án **không được trùng nhau sau khi bỏ dấu câu/hoa thường** (`True (✓)` và `True (t)` là 2 đáp án khác nhau; `Friday` và `friday.` là trùng → lỗi).

## 4. `passage` (khối đọc kèm theo, hiện trên mọi câu của phần)

| `kind` | Dùng cho | Trường |
|---|---|---|
| `reading` | Đoạn đọc để trả lời đúng/sai hoặc câu hỏi | `header`, `img` (tuỳ chọn), `paragraphs[]`, `theme` (`amber` mặc định / `blue`) |
| `blanks` | Điền khuyết: đoạn văn có chỗ trống `{1}`…`{N}`; mỗi câu = 1 chỗ trống, chỗ đang làm nhấp nháy vàng | `header`, `img`, `paragraphs[]` chứa `{1}..{N}` (N = số câu), `note` (tuỳ chọn, `{n}` = số chỗ trống đang làm) |
| `dialogue` | Hội thoại hai người | `header`, `lines[]` = `{who, text}` (người nói đầu tiên màu hồng, người thứ hai màu xanh lá) |

## 5. Công thức quy mọi dạng bài về trắc nghiệm

| Dạng trong đề gốc | Cách làm |
|---|---|
| Nhìn tranh, tick ô đúng | `img` = ảnh câu đó; options = 4 lựa chọn (đáp án + 3 nhiễu hợp lý) |
| Nhìn tranh, viết từ (có khung từ) | `wordBank` = khung từ của đề; options = đáp án + 3 từ **lấy từ khung** |
| Đúng / Sai (✓ ✗, T/F) | options = `["True (✓)","False (✗)"]` hoặc `["true","false"]` (2 đáp án → bố cục 2 cột) |
| Nghe và chọn / nghe và điền | `audio` + `audioMarks` + `audioAt` theo từng câu; giải thích trích lại **lời trong bài nghe** |
| Đọc đoạn và trả lời | `passage.kind="reading"`; câu hỏi lấy từ đề |
| Điền từ vào đoạn văn | `passage.kind="blanks"` + `wordBank`; options = đáp án + 3 nhiễu từ khung từ |
| Bài hội thoại | `passage.kind="dialogue"` + audio nếu đề có |
| Sắp xếp từ thành câu | options = 1 câu đúng + 3 câu sai trật tự **cùng bộ từ** (sai kiểu học sinh hay mắc) |
| Đọc bảng/thời khoá biểu | `img` = ảnh bảng, `imgStyle:"framed"` ở phần |
| Viết câu / tự luận | Không có trong mẫu này → chuyển thành chọn câu đúng nhất; nếu đề cần học sinh **tự gõ** thì dùng skill `worksheet-to-game` |

Đáp án nhiễu: sai nhưng **có thể hiểu nhầm** (cùng loại từ, cùng chủ đề, sai trật tự phổ biến). Không nhiễu vô lý, không "tất cả đều đúng". Vị trí đáp án đúng phân bố đều A–D (build sẽ cảnh báo nếu lệch).

## 6. Nguồn đáp án và audio

1. Đề có đáp án/đáp án in đậm/script bài nghe → dùng, **nhưng giải lại độc lập**; nếu lệch đáp án đề → báo người dùng, không âm thầm đổi.
2. Không có đáp án → tự giải bằng kiến thức; bài **nghe** mà không có script/đáp án và không có công cụ nhận dạng giọng nói → **hỏi 1 câu** (xin script hoặc đáp án), không đoán.
3. Mốc audio: chạy `python3 tools/build_game.py --suggest-marks media/partX.mp3` lấy ứng viên (quãng lặng ≥1.2s), nghe/đối chiếu script rồi mới đặt nhãn. Không biết chắc thì bỏ `audioAt` (chip đầu bài vẫn dùng được).
4. Ảnh: cắt từ PDF/ảnh đề đúng vùng của câu (PyMuPDF/pdftoppm → Pillow), mỗi file chỉ chứa nội dung câu đó. Build tự nén về ≤900px webp.

## 7. Quy trình kiểm tra (bắt buộc trước khi giao)

1. `python3 tools/build_game.py ...` → **0 lỗi** (✘). Mọi ⚠ phải xử lý hoặc nêu rõ lý do.
2. `cd tools && npm i && node test_game.js ../Game_XXX.html` → "Tất cả kiểm tra đạt" (đúng hết = 10.0; sai/hết giờ vào danh sách ôn; media đủ; không lộ đáp án).
3. `python3 tools/preview.py Game_XXX.html preview/` → xem ít nhất: màn nhập tên, mục lục, 1 câu mỗi **loại** phần (có audio, có passage, có ảnh, chỉ chữ), màn tổng kết. Không chữ tràn/ảnh vỡ/đáp án bị cắt.
4. Đọc lại **toàn bộ đáp án và giải thích** như một giáo viên khó tính: đúng kiến thức, đúng với đề gốc, giải thích khớp đáp án, không có đáp án nhiễu cũng đúng.
5. Báo người dùng: số phần/số câu, lỗi đề gốc đã phát hiện (nếu có), mục đã suy luận thay vì lấy từ đề.
