from flask import Flask, render_template_string, request

# Import trực tiếp hàm xử lý từ 3 file .py gốc của bạn
from caculator import may_tinh
from diemhocphan import tinh_diem_hoc_phan
from tinhBMI import tinh_bmi

app = Flask(__name__)

# --- TEMPLATE KHUNG MENU CHỦ ---
BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chương 5 - Bài Tập Tổng Hợp</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <!-- Menu Thanh Điều Hướng -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm mb-4">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">Chương 5 - Bài Tập</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link {% if active_page == 'may_tinh' %}active fw-bold{% endif %}" href="/may-tinh">
                            1. Máy Tính Cơ Bản
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if active_page == 'diem_hp' %}active fw-bold{% endif %}" href="/diem-hoc-phan">
                            2. Điểm Học Phần
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {% if active_page == 'bmi' %}active fw-bold{% endif %}" href="/bmi">
                            3. Tính BMI
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Trang chủ hiển thị danh sách lựa chọn -->
    {% if active_page == 'home' %}
    <div class="container text-center my-5" style="max-width: 600px;">
        <div class="card shadow-sm p-4">
            <h3 class="text-primary mb-4">BÀI TẬP TỔNG HỢP CHƯƠNG 5</h3>
            <p class="text-muted">Vui lòng chọn 1 trong 3 bài toán bên dưới để sử dụng:</p>
            <div class="d-grid gap-3 mt-3">
                <a href="/may-tinh" class="btn btn-outline-primary btn-lg">1. Máy Tính Cơ Bản</a>
                <a href="/diem-hoc-phan" class="btn btn-outline-primary btn-lg">2. Tính Điểm Học Phần</a>
                <a href="/bmi" class="btn btn-outline-primary btn-lg">3. Tính Chỉ Số BMI</a>
            </div>
        </div>
    </div>
    {% endif %}

    <!-- Nội dung của bài được gọi sẽ chèn vào đây -->
    {% if active_page != 'home' %}
    <div class="container my-3">
        {{ sub_content|safe }}
    </div>
    {% endif %}

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# 1. Trang chủ chính
@app.route('/', methods=['GET'])
def index():
    return render_template_string(BASE_LAYOUT, active_page='home')

# 2. Chạy bài 1 (Gọi nguyên văn hàm từ caculator.py)
@app.route('/may-tinh', methods=['GET', 'POST'])
def route_may_tinh():
    inner_html = may_tinh()
    return render_template_string(BASE_LAYOUT, active_page='may_tinh', sub_content=inner_html)

# 3. Chạy bài 2 (Gọi nguyên văn hàm từ diemhocphan.py)
@app.route('/diem-hoc-phan', methods=['GET', 'POST'])
def route_diem_hoc_phan():
    inner_html = tinh_diem_hoc_phan()
    return render_template_string(BASE_LAYOUT, active_page='diem_hp', sub_content=inner_html)

# 4. Chạy bài 3 (Gọi nguyên văn hàm từ tinhBMI.py)
@app.route('/bmi', methods=['GET', 'POST'])
def route_bmi():
    inner_html = tinh_bmi()
    return render_template_string(BASE_LAYOUT, active_page='bmi', sub_content=inner_html)

if __name__ == '__main__':
    app.run(debug=True)