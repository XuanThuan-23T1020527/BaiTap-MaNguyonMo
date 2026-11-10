from flask import Flask, request, render_template_string

app = Flask(__name__)

def parse_float(val_str):
    """Ép kiểu chuỗi sang float, hỗ trợ dấu phẩy thập phân."""
    if not val_str or not val_str.strip():
        return None, "Vui lòng nhập một số."
    
    cleaned_str = val_str.strip().replace(',', '.')
    try:
        val = float(cleaned_str)
        return val, None
    except ValueError:
        return None, "Vui lòng nhập một số."

@app.route('/', methods=['GET', 'POST'])
@app.route('/bmi', methods=['GET', 'POST'])
def tinh_bmi():
    height_raw = ''
    weight_raw = ''
    
    err_height = None
    err_weight = None
    
    bmi = None
    category = None
    alert_class = ''
    weight_range_str = ''

    if request.method == 'POST':
        height_raw = request.form.get('height', '')
        weight_raw = request.form.get('weight', '')

        h_val, err_h = parse_float(height_raw)
        w_val, err_w = parse_float(weight_raw)

        # Kiểm tra khoảng giá trị hợp lệ cho Chiều cao (50 - 250 cm)
        if err_h is None:
            if h_val < 50 or h_val > 250:
                err_height = "Giá trị phải từ 50 đến 250. (nhập mét thay vì cm)"
        else:
            err_height = err_h

        # Kiểm tra khoảng giá trị hợp lệ cho Cân nặng (10 - 300 kg)
        if err_w is None:
            if w_val < 10 or w_val > 300:
                err_weight = "Giá trị phải từ 10 đến 300."
        else:
            err_weight = err_w

        # Tính toán nếu không có lỗi
        if err_height is None and err_weight is None:
            h_m = h_val / 100.0  # Đổi cm sang m
            bmi = round(w_val / (h_m ** 2), 1)

            # Phân loại theo chuẩn châu Á & gán màu sắc
            if bmi < 18.5:
                category = "Thiếu cân"
                alert_class = "alert-warning"  # Nền vàng
            elif bmi < 23.0:
                category = "Bình thường"
                alert_class = "alert-success"  # Nền xanh lá
            elif bmi < 25.0:
                category = "Thừa cân"
                alert_class = "alert-warning"  # Nền vàng
            else:
                category = "Béo phí"
                alert_class = "alert-danger"   # Nền đỏ

            # Tính cân nặng nên có (BMI từ 18.5 đến 22.9)
            w_min = round(18.5 * (h_m ** 2), 1)
            w_max = round(22.9 * (h_m ** 2), 1)
            weight_range_str = f"nên có {w_min} – {w_max} kg"

    html = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tính chỉ số BMI</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container my-5" style="max-width: 500px;">
            <div class="card shadow-sm">
                <div class="card-header bg-primary text-white text-center">
                    <h4 class="mb-0">Tính Chỉ Số BMI</h4>
                </div>
                <div class="card-body p-4">
                    <form method="POST" action="">
                        <!-- Ô nhập Chiều cao -->
                        <div class="mb-3">
                            <label class="form-label fw-bold">Chiều cao (cm):</label>
                            <input type="text" name="height" value="{{ height_raw }}" 
                                   class="form-control {% if err_height %}is-invalid{% endif %}" 
                                   placeholder="Ví dụ: 170">
                            {% if err_height %}
                                <div class="invalid-feedback">{{ err_height }}</div>
                            {% endif %}
                        </div>

                        <!-- Ô nhập Cân nặng -->
                        <div class="mb-3">
                            <label class="form-label fw-bold">Cân nặng (kg):</label>
                            <input type="text" name="weight" value="{{ weight_raw }}" 
                                   class="form-control {% if err_weight %}is-invalid{% endif %}" 
                                   placeholder="Ví dụ: 65 hoặc 65,5">
                            {% if err_weight %}
                                <div class="invalid-feedback">{{ err_weight }}</div>
                            {% endif %}
                        </div>

                        <div class="d-grid mt-4">
                            <button type="submit" class="btn btn-primary fw-bold">Tính BMI</button>
                        </div>
                    </form>

                    <!-- Khung kết quả hiển thị -->
                    {% if bmi is not none %}
                        <div class="alert {{ alert_class }} mt-4 mb-0 text-center" role="alert">
                            <h5 class="alert-heading mb-1">{{ bmi }} - {{ category }}
                            {% if category == "Bình thường" %}
                                ; {{ weight_range_str }}
                            {% endif %}
                            </h5>
                            {% if category != "Bình thường" %}
                                <div class="fw-bold mt-1">; {{ weight_range_str }}</div>
                            {% endif %}
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
        height_raw=height_raw,
        weight_raw=weight_raw,
        err_height=err_height,
        err_weight=err_weight,
        bmi=bmi,
        category=category,
        alert_class=alert_class,
        weight_range_str=weight_range_str
    )

if __name__ == '__main__':
    app.run(debug=True)