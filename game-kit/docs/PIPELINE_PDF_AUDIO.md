# PIPELINE — từ file đề PDF (ảnh) + audio → game (quy trình đã chạy cho GS3 Unit 7–10)

Dùng khi người dùng gửi **đề dạng PDF toàn ảnh** + **file nghe rời** và nói "làm game theo các file này".
Chuẩn mẫu: Unit 3 (`examples/unit3_test`). Cách làm giữ nguyên; **nội dung chỉ lấy từ file mới**
(không copy từ game cũ/Unit 3; game cũ chỉ để đối chiếu đáp án nghe, không để chép).

## 0. Quy tắc cố định
- Tiêu đề: `GLOBAL SUCCESS - UNIT N: TOPIC`; badge `Luyện Thi · Global Success`; tag `Global Success 3 · Unit N`. **Không ghi "Tiếng Anh 3"**.
- Mỗi game 12 phần theo đề; mọi dạng quy về trắc nghiệm 2–4 đáp án (xem GAME_SPEC §5). Có ô nhập họ tên bắt buộc ở màn đầu (engine lo, đừng sửa).
- Tên file: `Game_GS3_Unit<N>_Test.html`.

## 1. Chuẩn bị
```bash
export SRC=/đường/dẫn/thư_mục_file_người_dùng/  WORK=/đường/dẫn/work
pdftoppm -r 100 -png de.pdf $WORK/uN/pages/p     # xem (tọa độ cắt tính theo 100dpi, ~827x1170)
pdftoppm -r 200 -png de.pdf $WORK/uN/hi/p        # cắt ảnh (x2 độ nét)
```
Đọc từng trang bằng Read (xem ảnh). Ghi lại: câu hỏi, khung từ, bảng nối, bài đọc.

## 2. Audio (không có Whisper)
`python3 workflow/asr.py '*Part_4_U10.mp3'` → pocketsphinx cho bản chép **thô** + mốc giây (gom theo quãng lặng).
Suy đáp án bằng: bản chép thô + loại trừ theo tranh + câu hỏi trong đề. Nếu có game cũ cùng unit → chỉ đối chiếu.
Đặt `audioAt` từ mốc ASR (xấp xỉ). **Mục nào không chắc → ghi vào danh sách báo người dùng nghe lại.**
Part "Listen and number": đánh số tranh theo thứ tự đọc **trái→phải, hàng trên rồi hàng dưới**; câu hỏi dạng "nội dung thứ k trong bài nghe ↔ Tranh ?".

## 3. Viết generator (mỗi unit 1 file `mk_uN.py`, xem `workflow/examples/`)
`from common import *` rồi `u=Unit(N)`:
- `u.crop(trang,(x0,y0,x1,y1),'tên')` cắt ảnh (toạ độ 100dpi) → `media/tên.webp`
- `u.grid(trang,[box…],'tên',cols=3)` ghép nhiều ô nhỏ thành 1 ảnh to (nối tranh, đánh số)
- `u.quad(trang,y0,y1,x0,x1,'tên')` hàng 4 tranh nhỏ → lưới 2×2 (Part "odd one out")
- `u.audio('*Part_4*.mp3','part4')` nén audio mono 64k
- `Q(prompt,options,answer,explain,img=,audioAt=)`; `place(đúng,[sai…])` xoay vị trí đáp án A–D cho đều
- `u.save({...,'sections':sec})` → `game.json`

Mẫu 12 phần chuẩn: P1 nối từ–tranh (lưới + đáp án A–E) · P2 khác loại (quad) · P3 điền từ (wordBank + ảnh) · P4 nghe chọn (audio+marks) · P5 nghe đánh số (lưới + "Tranh k") · P6 đọc nối câu–tranh · P7 chọn câu trả lời · P8 bài đọc (`passage.kind=reading` + ảnh) · P9 ngữ pháp chọn · P10 nhìn tranh hoàn thành (cắt từng ô) · P11 sắp xếp từ (1 đúng + 3 sai cùng bộ từ) · P12 nói/nhìn tranh (cùng 1 ảnh cho cả phần).
Câu mơ hồ trong đề (vd "two children at the table" khi có 2 bàn) → làm rõ trong prompt, và báo người dùng.

## 4. Build → test → xem
```bash
python3 -I tools/build_game.py $WORK/uN/game.json -o $WORK/out_UN.html        # 0 lỗi
JSDOM_PATH=<đường dẫn node_modules/jsdom> node tools/test_game.js $WORK/out_UN.html
python3 workflow/sheet.py N 1 3 4 5 8 10 12     # ảnh ghép các phần → $WORK/prevN/sheet.png, xem bằng Read
```
Kiểm: ảnh không cắt lỗi/không lộ đáp án (vd ảnh chứa chữ đáp án), chữ không tràn, đáp án A–D phân bố đều, đọc lại toàn bộ đáp án như giáo viên.

## 5. Giao
Gửi 4 file `.html` + báo ngắn (tiếng Việt): số phần/câu, dung lượng, **danh sách mục suy luận/không chắc** (đáp án nghe, mốc audio, câu mơ hồ) để người dùng nghe xác nhận.

## 6. Lỗi đã gặp
- Chạy generator **không** dùng `python3 -I` (cần import `common`); `build_game.py` thì dùng `-I`.
- `test_game.js` cần `JSDOM_PATH`; thiếu sẽ "Cannot find module".
- `preview.py` đánh số phần 0-based, file ra `secNN` 1-based (sheet.py đã xử lý: nhập số phần 1-based).
- Ảnh nhiều tranh nhỏ → dùng `grid/quad` thay vì cắt cột dài.
