# SKD1108: Công cụ Đánh giá Thực nghiệm

Kho lưu trữ này chứa bộ công cụ tự động chạy kiểm thử và tập dữ liệu phục vụ cho Đề tài nghiên cứu khoa học: **"Nghiên cứu thực nghiệm và đánh giá hiệu quả của GitHub Copilot trong việc tối ưu hóa quy trình gỡ lỗi (Debugging) mã nguồn C++."**

- **Học phần:** Phương pháp luận Nghiên cứu khoa học (SKD1108)
- **Giảng viên hướng dẫn:** ThS. Trần Thị Tuyết Nhung
- **Nhóm thực hiện:** Nhóm 02 (Lớp SKD1108 - Nhóm 17)

## 🎯 Chức năng cốt lõi

Tập lệnh Python (`chambai.py`) được thiết kế để đảm bảo tính khách quan tối đa cho các chỉ số đo lường trong nghiên cứu định lượng:
1. **Tự động Hiệu chuẩn (CPU Calibration):** Tự động đo lường và đồng bộ tốc độ xử lý của máy tính để thiết lập giới hạn thời gian (TLE) công bằng (chuẩn 10^8 phép tính/giây).
2. **Giám sát Môi trường Động:** Bắt chính xác các lỗi tràn bộ nhớ (Memory Limit Exceeded - 200MB) bằng `psutil`.
3. **Phân loại Lỗi Tiêu chuẩn:** Tự động phân loại 7 trạng thái mã nguồn theo chuẩn lập trình thi đấu (AC, WA, TLE, MLE, OLE, RTE, CE).
4. **Tự động Ghi nhận:** Xuất kết quả chi tiết của từng đối tượng thực nghiệm ra file `logs.csv`.

## 📂 Cấu trúc Dữ liệu Thực nghiệm

Bộ dữ liệu gồm 5 bài toán C++.

Để chạy tập lệnh, hệ thống cần đáp ứng:

Trình biên dịch: g++ (GCC) đã được cấu hình trong biến môi trường PATH.

Môi trường chạy: Python 3.6+

Thư viện phụ thuộc: Script yêu cầu psutil để giám sát dung lượng RAM. Cài đặt qua lệnh:

Bash
pip install psutil

## Hướng dẫn Thực nghiệm và Vận hành

Để tái lập quá trình đánh giá thực nghiệm trên máy tính cục bộ (local machine), vui lòng thực hiện tuần tự các bước sau:

**Bước 1: Sao chép Kho lưu trữ (Clone/Download Repository)**
- Tải toàn bộ mã nguồn và tập dữ liệu về máy tính bằng cách nhấn chọn `Code` -> `Download ZIP` (hoặc sử dụng lệnh `git clone`). 
- Tiến hành giải nén thư mục.

**Bước 2: Thiết lập Môi trường Dòng lệnh (CLI)**
- Mở Giao diện dòng lệnh (Command Prompt / Terminal) trên hệ điều hành của bạn.
- Sử dụng lệnh `cd` (Change Directory) để điều hướng đường dẫn tới thư mục gốc của dự án vừa giải nén.

**Bước 3: Khởi tạo Các thành phần phụ thuộc (Dependencies)**
- Đảm bảo hệ thống đã cài đặt Python. Khởi tạo thư viện giám sát tài nguyên bộ nhớ bằng lệnh:
  `pip install psutil`

**Bước 4: Thực hiện Quy trình Gỡ lỗi (Debugging)**
- Người tham gia thực nghiệm mở các tệp mã nguồn C++ (ví dụ: `bai01.cpp`, `bai02.cpp`...) bên trong các thư mục bài toán tương ứng.
- Tiến hành phân tích và vá lỗi (fix bugs) trực tiếp trên các tệp này, sau đó lưu lại.

**Bước 5: Khởi chạy Kịch bản Đánh giá (Evaluation Script)**
- Quay trở lại Terminal, thực thi tập lệnh chấm điểm tự động bằng lệnh:
  `python chambai.py`
- Tuân thủ các chỉ dẫn trên màn hình (nhập ID Sinh viên, Mã bài toán) để hệ thống tự động biên dịch, đối chiếu kết quả (Output) và ghi nhận log thực nghiệm.

***Minh chứng mã nguồn thuộc Phụ lục Tiểu luận cuối kỳ môn PPL Nghiên cứu Khoa học.***
