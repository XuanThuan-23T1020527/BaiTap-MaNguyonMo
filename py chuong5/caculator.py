

from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def may_tinh():
    a = ""
    b = ""
    op = "+"
    ket_qua = None
    loi_a = ""
    loi_b = ""
    loi_op = ""

    if request.method == "POST":
        a = request.form.get("a", "").strip()
        b = request.form.get("b", "").strip()
        op = request.form.get("op", "")

        so_a = None
        so_b = None
        if not a:
            loi_a = "Vui lòng nhập số thứ nhất."
        else:
            try:
                so_a = float(a.replace(",", "."))
            except ValueError:
                loi_a = "Số thứ nhất không đúng định dạng."

    
        if not b:
            loi_b = "Vui lòng nhập số thứ hai."
        else:
            try:
                so_b = float(b.replace(",", "."))
            except ValueError:
                loi_b = "Số thứ hai không đúng định dạng."

        
        if op not in ["+", "-", "*", "/"]:
            loi_op = "Phép toán không hợp lệ."

        
        if not loi_a and not loi_b and not loi_op:
            if op == "/" and so_b == 0:
                loi_b = "Không thể chia cho 0."
            elif op == "+":
                ket_qua = so_a + so_b
            elif op == "-":
                ket_qua = so_a - so_b
            elif op == "*":
                ket_qua = so_a * so_b
            elif op == "/":
                ket_qua = so_a / so_b


    html = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <title>Máy tính</title>
    </head>
    <body>
        <h2>Máy tính đơn giản</h2>

        <form method="POST">
            <label>Số thứ nhất (a):</label><br>
            <input type="text" name="a" value="{{ a }}">
            <p style="color:red">{{ loi_a }}</p>

            <label>Phép toán:</label><br>
            <select name="op">
                {% for p in ['+', '-', '*', '/'] %}
                <option value="{{ p }}"
                    {% if op == p %}selected{% endif %}>
                    {{ p }}
                </option>
                {% endfor %}
            </select>
            <p style="color:red">{{ loi_op }}</p>

            <label>Số thứ hai (b):</label><br>
            <input type="text" name="b" value="{{ b }}">
            <p style="color:red">{{ loi_b }}</p>

            <button type="submit">Tính toán</button>
        </form>

        {% if ket_qua is not none %}
            <h3>Kết quả:
                {{ a|replace(',', '.') }} {{ op }}
                {{ b|replace(',', '.') }} = {{ ket_qua }}
            </h3>
        {% endif %}
    </body>
    </html>
    """

    return render_template_string(
        html,
        a=a, b=b, op=op,
        ket_qua=ket_qua,
        loi_a=loi_a,
        loi_b=loi_b,
        loi_op=loi_op
    )


if __name__ == "__main__":
    app.run(debug=True)
