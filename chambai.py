import os
import subprocess
import csv
import time
import threading
from datetime import datetime

try:
    import psutil
except ImportError:
    print("[LỖI NGHIÊM TRỌNG] Hệ thống yêu cầu thư viện 'psutil' để đo giới hạn bộ nhớ.")
    print("Vui lòng chạy lệnh: pip install psutil")
    exit(1)

# --- CẤU HÌNH TIÊU CHUẨN ĐÁNH GIÁ ---
STANDARD_OPS_LIMIT = 10_000_000_00 #10 triệu phép tính
STANDARD_TIME_SEC = 1.0 

# Các giới hạn khác
MEMORY_LIMIT_KB = 200000       # MLE: Giới hạn bộ nhớ (~200MB)
OUTPUT_LIMIT_BYTES = 32 * 1024 * 1024  # OLE: Giới hạn đầu ra (32MB)

# Biến toàn cục sẽ được cập nhật sau khi đo tốc độ máy
REAL_TIMEOUT_SEC = 2.0 

def calibrate_machine():
    """Đo lường tốc độ phần cứng hiện tại để thiết lập TLE chính xác"""
    global REAL_TIMEOUT_SEC
    print("[*] Đang hiệu chuẩn (Calibrate) tốc độ CPU để cân bằng máy nhanh/chậm...")
    
    bench_cpp = "benchmark_temp.cpp"
    bench_exe = "benchmark_temp.exe" if os.name == 'nt' else "benchmark_temp"
    
    # Code C++ mẫu chạy đúng 10^8 phép tính gán (dùng volatile để tránh bị compiler tối ưu bỏ qua)
    code = """
    int main() {
        volatile long long x = 0;
        for(long long i = 0; i < 100000000; i++) { // 10^8 vòng lặp
            x = x + 1;
        }
        return 0;
    }
    """
    with open(bench_cpp, "w", encoding='utf-8') as f:
        f.write(code)

    # Biên dịch
    subprocess.run(["g++", bench_cpp, "-o", bench_exe], capture_output=True)

    # Chạy và đo thời gian chính xác
    start_time = time.perf_counter()
    exe_path = bench_exe if os.name == 'nt' else f"./{bench_exe}"
    subprocess.run([exe_path], capture_output=True)
    end_time = time.perf_counter()
    
    elapsed = end_time - start_time
    if elapsed == 0: elapsed = 0.001
    
    # Máy tính hiện tại làm được bao nhiêu phép tính 1 giây?
    real_ops_per_sec = 100_000_000 / elapsed
    
    # Tính thời gian timeout thực tế để chạy được đúng 10^6 phép tính (STANDARD_OPS_LIMIT)
    REAL_TIMEOUT_SEC = STANDARD_OPS_LIMIT / real_ops_per_sec
    
    # Dọn dẹp file rác
    if os.path.exists(bench_cpp): os.remove(bench_cpp)
    if os.path.exists(bench_exe): os.remove(bench_exe)
    
    # Tránh timeout quá thấp gây lỗi ngẫu nhiên do hệ điều hành xử lý (OS Overhead)
    if REAL_TIMEOUT_SEC < 0.01:
        REAL_TIMEOUT_SEC = 0.01
        
    print(f"    -> Tốc độ CPU: ~{real_ops_per_sec:,.0f} vòng lặp/giây")
    print(f"    -> Giới hạn TLE điều chỉnh cho máy này: {REAL_TIMEOUT_SEC:.4f} giây")
    print(f"       (Mọi code chạy lâu hơn {REAL_TIMEOUT_SEC:.4f}s trên máy này sẽ bị tính là TLE)\n")


def log_result(participant_id, problem_id, passed_tests, total_tests):
    """Ghi kết quả vào file CSV"""
    file_exists = os.path.isfile('logs.csv')
    with open('logs.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Participant_ID', 'Problem_ID', 'Passed', 'Total_Tests', 'Result'])
        
        status = "Thành công" if (passed_tests == total_tests and total_tests > 0) else "Thất bại"
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), participant_id, problem_id, passed_tests, total_tests, status])


def execute_and_monitor(exe_file, input_data, expected_data):
    """Hàm chạy thực thi và giám sát TLE, MLE, OLE, RTE, IR, AC, WA"""
    try:
        process = subprocess.Popen(
            [f"./{exe_file}" if os.name != 'nt' else exe_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
    except Exception:
        return "RTE"

    output_container = {"stdout": "", "returncode": None}

    def communicate_thread():
        try:
            out, _ = process.communicate(input=input_data)
            output_container["stdout"] = out
            output_container["returncode"] = process.returncode
        except Exception:
            pass

    thread = threading.Thread(target=communicate_thread)
    thread.start()

    # Sử dụng perf_counter thay vì time() cho độ chính xác tính bằng microsecond
    start_time = time.perf_counter() 
    peak_memory_kb = 0
    status = None

    while thread.is_alive():
        elapsed_time = time.perf_counter() - start_time
        
        # Kiểm tra TLE dựa trên mức thời gian máy tính ĐÃ ĐƯỢC CÂN BẰNG
        if elapsed_time > REAL_TIMEOUT_SEC:
            process.kill()
            status = "TLE"
            break
            
        # Kiểm tra MLE
        try:
            if psutil.pid_exists(process.pid):
                p_info = psutil.Process(process.pid)
                mem_kb = p_info.memory_info().rss / 1024 
                if mem_kb > peak_memory_kb:
                    peak_memory_kb = mem_kb
                
                if peak_memory_kb > MEMORY_LIMIT_KB:
                    process.kill()
                    status = "MLE"
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
            
        time.sleep(0.001) # Sleep rất ngắn vì timeout có thể rất nhỏ

    thread.join()

    if status:
        return status

    ret_code = output_container["returncode"]
    if ret_code != 0:
        return "RTE" if ret_code < 0 else "IR"

    out_text = output_container["stdout"]
    
    if len(out_text.encode('utf-8')) > OUTPUT_LIMIT_BYTES:
        return "OLE"

    # Fix lỗi ký tự khoảng trắng thừa ở cuối output
    if out_text.strip() == expected_data.strip():
        return "AC"
    else:
        return "WA"


def cham_mot_bai(participant_id, problem_id):
    CPP_FILE = os.path.join(problem_id, f"{problem_id}.cpp")
    INPUT_DIR = os.path.join(problem_id, "input")
    EXPECTED_DIR = os.path.join(problem_id, "output")
    EXE_FILE = os.path.join(problem_id, "program.exe" if os.name == 'nt' else "program")

    if not os.path.exists(problem_id):
        print(f"\n[LỖI] Không tìm thấy thư mục '{problem_id}'.")
        return
    if not os.path.exists(CPP_FILE):
        print(f"\n[LỖI] Không tìm thấy file code '{CPP_FILE}'.")
        return

    print(f"\n[*] Đang biên dịch mã nguồn {CPP_FILE}...")
    compile_process = subprocess.run(["g++", CPP_FILE, "-o", EXE_FILE], capture_output=True, text=True)
    
    if compile_process.returncode != 0:
        print("[FAIL] CE (Compile Error) - Lỗi cú pháp.")
        total_tests = len(os.listdir(INPUT_DIR)) if os.path.exists(INPUT_DIR) else 0
        log_result(participant_id, problem_id, 0, total_tests)
        print("-" * 50)
        return

    print(f"[*] Biên dịch thành công. Đang chạy bộ Test...\n")
    
    if not os.path.exists(INPUT_DIR) or not os.path.exists(EXPECTED_DIR):
        print(f"[LỖI] Thiếu thư mục 'input' hoặc 'output' trong {problem_id}.")
        return

    test_files = sorted(os.listdir(INPUT_DIR))
    passed_tests = 0
    total_tests = len(test_files)

    if total_tests == 0:
        print("[THÔNG BÁO] Không có file test nào.")
        return

    for test_file in test_files:
        in_path = os.path.join(INPUT_DIR, test_file)
        exp_out_path = os.path.join(EXPECTED_DIR, test_file)
        
        if not os.path.exists(exp_out_path):
            print(f"  ? Test {test_file}: LỖI (Thiếu file đáp án chuẩn)")
            continue
            
        with open(in_path, 'r', encoding='utf-8') as f: 
            input_data = f.read()
        with open(exp_out_path, 'r', encoding='utf-8') as f: 
            expected_data = f.read().strip()

        status = execute_and_monitor(EXE_FILE, input_data, expected_data)

        if status == "AC":
            print(f"  + Test {test_file}: AC")
            passed_tests += 1
        else:
            print(f"  - Test {test_file}: {status}")

    print(f"\n=> KẾT QUẢ [{problem_id}]: PASS {passed_tests}/{total_tests} TEST CASES")
    log_result(participant_id, problem_id, passed_tests, total_tests)
    print("-" * 50)


def main():
    print("=" * 60)
    print("                HỆ THỐNG CHẤM TỰ ĐỘNG     ")
    print("=" * 60)
    
    # Chạy đo tốc độ máy ngay khi khởi động
    calibrate_machine()
    
    while True:
        command = input("\nGõ 'start' để bắt đầu phiên mới, hoặc 'end' để thoát: ").strip().lower()
        
        if command in ['end', 'exit', 'quit']:
            print("Đã thoát hệ thống. Cảm ơn đã tham gia!")
            break
            
        elif command == 'start':
            participant_id = input("\n[NHẬP] Nhập ID Người tham gia (VD: SV_01): ").strip()
            print(f"\n>>> Đã thiết lập ID: {participant_id}. Bắt đầu chấm. <<<")
            
            while True:
                problem_id = input(f"\n[{participant_id}] Nhập Mã bài toán (VD: bai01, bai02...): ").strip().lower()
                
                if problem_id == 'back':
                    print(f"\nĐã kết thúc phiên của {participant_id}.")
                    break
                elif problem_id in ['end', 'exit', 'quit']:
                    print("Đã thoát hệ thống. Cảm ơn đã tham gia!")
                    return 
                elif problem_id == '':
                    continue
                    
                cham_mot_bai(participant_id, problem_id)
                
        else:
            print("Lệnh không hợp lệ. Vui lòng gõ 'start' hoặc 'end'.")

if __name__ == "__main__":
    main()
