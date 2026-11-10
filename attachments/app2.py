from datetime import timedelta
from functools import wraps

from flask import (Flask, flash, redirect, render_template, request,
                   session, url_for)

from forms import RegisterForm
from user import USERS  # dùng chung USERS của Bài 4

app = Flask(__name__)
app.config["SECRET_KEY"] = "doi-khoa-bi-mat-nay"  # Flash/session/CSRF cần SECRET_KEY
# "Ghi nhớ": cookie phiên có Expires (30 ngày), đóng mở trình duyệt vẫn đăng nhập
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)



def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user" not in session:
            flash("Vui lòng đăng nhập để xem trang này.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Đã đăng nhập mà vào /login -> về /
    if "user" in session:
        return redirect(url_for("index"))

    username = ""
    remember = False
    if request.method == "POST":
        username = request.form.get("username", "").strip()  # " an" vẫn hợp lệ
        password = request.form.get("password", "")          # không strip mật khẩu
        remember = request.form.get("remember") == "on"

        # So khớp phân biệt hoa thường; để trống -> không có trong USERS / sai
        if username in USERS and USERS[username] == password:
            session["user"] = username
            session.permanent = remember  # có Expires nếu tích "Ghi nhớ"
            flash(f"Đăng nhập thành công. Xin chào {username}!", "success")
            return redirect(url_for("index"))

        flash("Sai tên đăng nhập hoặc mật khẩu.", "danger")
        # Không truyền lại password -> ô mật khẩu luôn trống
    return render_template("login.html", username=username, remember=remember)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        USERS[form.username.data] = form.password.data  # thêm vào USERS
        flash("Đăng ký thành công.", "success")
        return redirect(url_for("login"))
    return render_template("dangki.html", form=form)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Bạn đã đăng xuất.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)