# ANTIGRAVITY AGENT RULES FOR GAME-KIT

## 1. QUY TẮC THỰC THI (EXECUTION RULES)
- **CẤM TỰ TRỊ**: Tuyệt đối KHÔNG tự động chạy các script Python (`build_game.py`, v.v.), KHÔNG tự động gõ lệnh terminal, và KHÔNG khởi động server khi chưa có lệnh "Xác nhận" từ người dùng.
- **NEO NGỮ CẢNH**: BẮT BUỘC cập nhật tiến độ vào file `STATE.md` sau mỗi bước xử lý thành công. 
- **ĐỌC TRƯỚC KHI LÀM**: BẮT BUỘC đọc lại `STATE.md` và file `RULES.md` này trước khi thực thi bất kỳ yêu cầu mới nào.

## 2. QUY TẮC KIẾN TRÚC CODE (ARCHITECTURE RULES)
- **SINGLE-FILE HTML**: Bắt buộc viết toàn bộ cấu trúc (HTML), giao diện (CSS trong thẻ `<style>`) và logic (JavaScript trong thẻ `<script>`) vào MỘT FILE `.html` duy nhất. Không sử dụng kiến trúc đa tệp.
- **NO EXTERNAL LIBRARIES**: Chỉ sử dụng Vanilla JavaScript (ES6+), DOM API thuần, và Web Audio API (`window.AudioContext`). Tuyệt đối không dùng jQuery, React, Vue, hay kéo thư viện từ CDN nếu không được yêu cầu cụ thể.
    
## 3. QUY TẮC DỮ LIỆU & TRẠNG THÁI (DATA & STATE RULES)
- **DATA-DRIVEN DESIGN**: Phân lập toàn bộ nội dung câu hỏi, cấu hình game vào một hằng số JSON duy nhất (ví dụ: `const WORKSHEET = {...};`) đặt ở đầu thẻ `<script>`.
- **CENTRALIZED STATE**: Gom toàn bộ trạng thái đang chạy của game (câu hỏi hiện tại, điểm số, thời gian) vào một object duy nhất (ví dụ: `let CUR = {...};`).
- **ANTI-CHEAT (MÃ HÓA CƠ BẢN)**: Bắt buộc mã hóa Base64 cho các trường chứa đáp án đúng (`full`) và giải thích (`e`) trong dữ liệu JSON. (Sử dụng `btoa()` khi tạo data và `atob()` khi giải mã hiển thị).
