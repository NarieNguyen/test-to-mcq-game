# game-kit — nhân bản game trắc nghiệm kiểu "Unit 3 Test"

Một engine chung + một script build. Mỗi game mới chỉ là **1 file nội dung (`game.json`) + ảnh/audio**.
AI không viết lại giao diện/luật chấm → game nào cũng giống hệt nhau.

```
game-kit/
  engine/engine.html        ← giao diện + luật chấm (KHÔNG sửa tay)
  tools/build_game.py       ← kiểm tra lỗi, băm đáp án, nén & nhúng media, ra 1 file .html
  tools/test_game.js        ← chạy thử như học sinh (jsdom)
  tools/preview.py          ← chụp ảnh màn hình điện thoại từng phần
  docs/GAME_SPEC.md         ← đặc tả + mặc định + công thức quy dạng bài về trắc nghiệm + checklist QC
  BRIEF_TEMPLATE.md         ← mẫu yêu cầu gửi AI
  examples/unit3_test/      ← game.json + media + file game đã build (mẫu chuẩn)
  docs/PIPELINE_PDF_AUDIO.md← quy trình làm từ PDF ảnh + audio rời (đã dùng cho GS3 Unit 7–10)
  workflow/                 ← common.py (crop/grid/quad/Q/place), asr.py (chép audio thô), sheet.py (ảnh ghép xem), examples/ (2 generator mẫu)
```

## Dùng nhanh

```bash
python3 tools/build_game.py examples/unit3_test/game.json -o Game_TA4_Unit3_Test.html   # build
cd tools && npm i && node test_game.js ../Game_TA4_Unit3_Test.html                       # test
python3 tools/preview.py Game_TA4_Unit3_Test.html preview/                               # xem giao diện
python3 tools/build_game.py --suggest-marks media/part4.mp3                              # gợi ý mốc audio
```
Cần: Python 3 (+ Pillow để nén ảnh), ffmpeg/ffprobe (audio), Node 18+ (test), Playwright (preview).

## Làm game mới
1. Tạo thư mục `GameMoi/` với `media/` (ảnh cắt từ đề, audio).
2. Gửi AI: đề + (audio) + `BRIEF_TEMPLATE.md` đã điền (hoặc 1 dòng nếu đã cài skill).
3. AI viết `GameMoi/game.json` → build → test → preview → đọc lại đáp án → giao file `.html`.
4. Gửi file `.html` cho học sinh; học sinh chụp "Bảng Vàng Chứng Nhận" gửi lại cô.

## Giữ bộ kit ở đâu để AI luôn thấy?
Đưa cả thư mục `game-kit` (hoặc file zip) vào **Project** của Claude (Project knowledge), hoặc thư mục cố định
trên máy đã kết nối. Skill `test-to-mcq-game` sẽ tìm `game-kit` ở đó; không thấy sẽ xin bạn đính kèm zip.
