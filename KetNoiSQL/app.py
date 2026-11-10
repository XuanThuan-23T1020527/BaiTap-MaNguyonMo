import os
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 1. Khởi tạo Base Class và SQLAlchemy
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-chi-dung-khi-phat-trien"

# Cấu hình đường dẫn lưu file qlsv.db trong thư mục KetNoiSQL
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "qlsv.db")

db.init_app(app)

# 2. Khai báo Model Student (Bước 3)
class Student(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    mssv: Mapped[str] = mapped_column(String(10), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    gpa: Mapped[float] = mapped_column(default=0.0)

    def __repr__(self):
        return f"<Student {self.mssv} {self.name}>"

# 3. Tạo bảng tự động
with app.app_context():
    db.create_all()

# 4. Các Route xử lý
@app.get("/")
def index():
    students = db.session.scalars(db.select(Student)).all()
    # Gọi trực tiếp file giao diện index.html
    return render_template("index.html", students=students)

@app.post("/them")
def add_student():
    mssv = request.form.get("mssv", "").strip()
    name = request.form.get("name", "").strip()
    gpa_raw = request.form.get("gpa", "").strip()

    if db.session.scalar(db.select(Student).where(Student.mssv == mssv)):
        flash(f"Mã sinh viên {mssv} đã tồn tại!", "danger")
        return redirect(url_for("index"))

    try:
        gpa = float(gpa_raw) if gpa_raw else 0.0
    except ValueError:
        gpa = 0.0

    new_sv = Student(mssv=mssv, name=name, gpa=gpa)
    db.session.add(new_sv)
    db.session.commit()
    flash(f"Thêm sinh viên '{name}' thành công!", "success")
    return redirect(url_for("index"))

@app.get("/them-mau")
def add_sample():
    total = db.session.scalar(db.select(func.count(Student.id)))
    if total > 0:
        flash(f"Đã có {total} sinh viên, không thêm mẫu nữa.", "warning")
        return redirect(url_for("index"))

    db.session.add_all([
        Student(mssv="23T1020001", name="Nguyễn Văn An", gpa=8.5),
        Student(mssv="23T1020002", name="Trần Thị Bình", gpa=6.8),
        Student(mssv="23T1020003", name="Lê Hoàng Cường", gpa=9.1),
        Student(mssv="23T1020004", name="Phạm Minh Dũng", gpa=4.5),
        Student(mssv="23T1020005", name="Hoàng Thu Hà", gpa=7.4),
    ])
    db.session.commit()
    flash("Đã thêm 5 sinh viên mẫu!", "success")
    return redirect(url_for("index"))

TEXT = {"Content-Type": "text/plain; charset=utf-8"}
@app.get("/thu-truy-van")
def try_queries():
    if db.session.scalar(db.select(func.count(Student.id))) == 0:
        return "Chưa có dữ liệu, hãy mở /them-mau trước."
    
    lines = []
    lines.append(f"1. get(3): {db.session.get(Student, 3)}")
    lines.append(f"2. get(99): {db.session.get(Student, 99)}")
    
    everyone = db.session.execute(db.select(Student)).scalars().all()
    lines.append(f"3. Tất cả: {len(everyone)} sinh viên")
    
    stmt = db.select(Student).where(Student.gpa >= 8).order_by(Student.gpa.desc())
    good = db.session.execute(stmt).scalars().all()
    lines.append(f"4. Điểm >= 8: {good}")
    
    binh = db.session.scalar(db.select(Student).filter_by(mssv="23T1020002"))
    lines.append(f"5. MSSV 23T1020002: {binh}")
    
    count = db.session.scalar(db.select(func.count(Student.id)))
    avg = db.session.scalar(db.select(func.avg(Student.gpa)))
    lines.append(f"6. Số SV: {count}, điểm TB: {avg:.2f}")
    
    return "\n".join(lines), TEXT

if __name__ == "__main__":
    app.run(debug=True)