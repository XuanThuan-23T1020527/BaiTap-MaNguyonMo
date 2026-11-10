# from flask import Flask, jsonify, url_for
# from werkzeug.routing import BaseConverter
# class ListConverter(BaseConverter):
#     regex = r"-?\d+(?:,-?\d+)*"

#     def to_python(self, value):
#         return [int(x) for x in value.split(",")]

#     def to_url(self, value):
#         return ",".join(str(int(x)) for x in value)


# app = Flask(__name__)
# app.url_map.converters["list"] = ListConverter  # đăng ký trước khi khai báo route


# @app.route("/")
# @app.route("/home")
# @app.route("/index")
# def hello():
#     return "hello, world!"


# @app.route("/chia-nhom")
# def chia_nhom():
#     so_bai = 12
#     so_nhom = 4 
#     rs = f"Mỗi nhóm làm {so_bai / so_nhom} bài"
#     return rs


# @app.route("/user/<username>")
# def user_profile(username):
#     rs = f"Xin chao ban {username}"
#     return rs


# @app.route("/square/<float:n>")
# def square(n):
#     rs = f"Bình phương của {n} là {n * n}"
#     return rs


# @app.route("/sum/<list:numbers>")
# def sum_numbers(numbers):
#     return jsonify(numbers=numbers, sum=sum(numbers))




from datetime import date

from flask import Flask, render_template, request

app = Flask(__name__)


@app.context_processor
def inject_globals():
    return {
        "site_name": "MiniBlog",
        "current_year": date.today().year,
    }


@app.context_processor
def inject_helpers():
    def is_active(endpoint):
        return "active" if request.endpoint == endpoint else ""
    return {"is_active": is_active}


@app.route("/")
def home():
    return render_template("about.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    thong_tin = [
        ("Đơn vị", "MiniBlog - Blog minh hoạ học phần"),
        ("Người phụ trách", "Nhóm 1"),
        ("Email", "miniblog@example.com"),
        ("Điện thoại", "0123 456 789"),
        ("Địa chỉ", "Khoa Công nghệ Thông tin, Trường Đại học Khoa học, Đại học Huế"),
        ("Giờ làm việc", "Thứ 2 - Thứ 6, 7:30 - 17:00"),
    ]
    return render_template("contact.html", thong_tin=thong_tin)


@app.route("/hello/<name>")
def hello(name):
    return render_template("hello.html", name=name, skills=["Python", "Flask"])


if __name__ == "__main__":
    app.run(debug=True)