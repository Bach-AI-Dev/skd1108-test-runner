# SKD1108: Công cụ Đánh giá Thực nghiệm)

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

***Minh chứng mã nguồn thuộc Phụ lục Tiểu luận cuối kỳ môn PP Nghiên cứu Khoa học.***
