from flask import Flask, request, render_template_string

app = Flask(__name__)

def validate_and_parse_score(val_str):
    """
    Hàm kiểm tra dùng chung cho cả 3 ô điểm CC, GK, CK.
    Trả về (giá_trị_float, chuỗi_lỗi).
    """
    if not val_str or not val_str.strip():
        return None, "Vui lòng nhập một số."
    
    cleaned_str = val_str.strip().replace(',', '.')
    
    try:
        val = float(cleaned_str)
    except ValueError:
        return None, "Vui lòng nhập một số."
        
    if val < 0 or val > 10:
        return None, "Điểm phải từ 0 đến 10."
        
    return val, None

@app.route('/', methods=['GET', 'POST'])
@app.route('/diem-hoc-phan', methods=['GET', 'POST'])
def tinh_diem_hoc_phan():
    cc_raw = ''
    gk_raw = ''
    ck_raw = ''
    
    err_cc = None
    err_gk = None
    err_ck = None
    
    dtb = None
    xep_loai = None
    is_diem_liet = False

    if request.method == 'POST':
        cc_raw = request.form.get('cc', '')
        gk_raw = request.form.get('gk', '')
        ck_raw = request.form.get('ck', '')

        # Kiểm tra dữ liệu cả 3 ô
        cc_val, err_cc = validate_and_parse_score(cc_raw)
        gk_val, err_gk = validate_and_parse_score(gk_raw)
        ck_val, err_ck = validate_and_parse_score(ck_raw)

        # Tính toán nếu dữ liệu hợp lệ
        if err_cc is None and err_gk is None and err_ck is None:
            dtb = round(cc_val * 0.1 + gk_val * 0.3 + ck_val * 0.6, 1)

            if ck_val < 1:
                xep_loai = "F (điểm thi dưới 1)"
                is_diem_liet = True
            elif dtb >= 8.5:
                xep_loai = "A"
            elif dtb >= 7.0:
                xep_loai = "B"
            elif dtb >= 5.5:
                xep_loai = "C"
            elif dtb >= 4.0:
                xep_loai = "D"
            else:
                xep_loai = "F"

    html = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tính điểm học phần</title>
        <!-- Bootstrap 5 CDN -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container my-5" style="max-width: 500px;">
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white text-center">
                    <h4 class="mb-0">Tính Điểm Học Phần</h4>
                </div>
                <div class="card-body p-4">
                    <form method="POST" action="">
                        <!-- Chuyên cần -->
                        <div class="mb-3">
                            <label class="form-label fw-bold">Điểm Chuyên cần (10%):</label>
                            <input type="text" name="cc" value="{{ cc_raw }}" 
                                   class="form-control {% if err_cc %}is-invalid{% endif %}" placeholder="Ví dụ: 10 hoặc 8,5">
                            {% if err_cc %}
                                <div class="invalid-feedback">{{ err_cc }}</div>
                            {% endif %}
                        </div>

                        <!-- Giữa kỳ -->
                        <div class="mb-3">
                            <label class="form-label fw-bold">Điểm Giữa kỳ (30%):</label>
                            <input type="text" name="gk" value="{{ gk_raw }}" 
                                   class="form-control {% if err_gk %}is-invalid{% endif %}" placeholder="Ví dụ: 8">
                            {% if err_gk %}
                                <div class="invalid-feedback">{{ err_gk }}</div>
                            {% endif %}
                        </div>

                        <!-- Cuối kỳ -->
                        <div class="mb-3">
                            <label class="form-label fw-bold">Điểm Cuối kỳ (60%):</label>
                            <input type="text" name="ck" value="{{ ck_raw }}" 
                                   class="form-control {% if err_ck %}is-invalid{% endif %}" placeholder="Ví dụ: 9">
                            {% if err_ck %}
                                <div class="invalid-feedback">{{ err_ck }}</div>
                            {% endif %}
                        </div>

                        <div class="d-grid mt-4">
                            <button type="submit" class="btn btn-primary fw-bold">Tính Điểm</button>
                        </div>
                    </form>

                    <!-- Khung kết quả -->
                    {% if dtb is not none %}
                        <div class="alert {% if xep_loai == 'F' or is_diem_liet %}alert-danger{% else %}alert-success{% endif %} mt-4 mb-0 text-center" role="alert">
                            <h5 class="alert-heading mb-1">Kết quả: {{ dtb }} - {{ xep_loai }}</h5>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    return render_template_string(
        html,
        cc_raw=cc_raw,
        gk_raw=gk_raw,
        ck_raw=ck_raw,
        err_cc=err_cc,
        err_gk=err_gk,
        err_ck=err_ck,
        dtb=dtb,
        xep_loai=xep_loai,
        is_diem_liet=is_diem_liet
    )

if __name__ == '__main__':
    app.run(debug=True)