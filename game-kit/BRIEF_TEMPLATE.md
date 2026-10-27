# Mẫu yêu cầu làm game mới (copy – điền – gửi kèm file đề)

Chỉ cần **1 trong 2** cách. Với cả hai, AI tự làm đúng chuẩn trong `docs/GAME_SPEC.md`, không cần nhắc thêm.

## Cách 1 — Một dòng (khi đã cài skill `test-to-mcq-game` hoặc đã đính kèm game-kit)

```
Làm game mới y như game Unit 3 Test. Đề đính kèm: <file đề>. Audio: <file audio, nếu có>.
```

## Cách 2 — Điền thông tin (khi muốn kiểm soát từng chỗ)

```
Làm game mới theo game-kit (chuẩn Unit 3 Test).

Tên game / title : Unit 4 Test: My Day (Global Success 4)
Dòng badge       : Luyện Thi Học Kỳ · Tiếng Anh 4 · <tên cô>
Nhãn tag         : Global Success 4 · Unit 4
Mã id (không dấu): ta4_u4

File đề          : <đính kèm PDF/ảnh/Word>
Audio            : part4.mp3, part5.mp3 ...   (hoặc "không có")
Đáp án / script nghe: <đính kèm nếu có; nếu không có, AI tự giải và hỏi lại phần nghe>

Khác với mặc định (chỉ ghi nếu muốn đổi):
- Thời gian mỗi câu: 90s
- Môn không phải tiếng Anh: đổi giọng đọc sang ...
- Bỏ phần nào / chỉ làm Part nào: ...
```

Mọi thứ không ghi = dùng mặc định trong `docs/GAME_SPEC.md` mục 1.
