from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from xhtml2pdf import pisa

app = Flask(__name__)

# ================== بيانات الطلاب ==================
student_info = {"name": "", "id": ""}
subjects = []

# ================ المسار الأساسي ====================
basedir = os.path.abspath(os.path.dirname(__file__))

# ================== الصفحات ==================
@app.route("/")
def index():
    return render_template("index.html", student=student_info, subjects=subjects)

# ============= حفظ معلومات الطالب =============
@app.route("/save_student", methods=["POST"])
def save_student():
    student_info["name"] = request.form.get("student_name")
    student_info["id"] = request.form.get("student_id")
    return redirect(url_for("index"))

# ============= إضافة مادة =============
@app.route("/add_subject", methods=["POST"])
def add_subject():
    subject_name = request.form.get("subject_name")
    grade = request.form.get("grade")

    if subject_name and grade:
        subjects.append({"name": subject_name, "grade": float(grade)})
    return redirect(url_for("index"))

# ============= حذف مادة =============
@app.route("/delete_subject/<int:index>", methods=["POST"])
def delete_subject(index):
    if 0 <= index < len(subjects):
        subjects.pop(index)
    return redirect(url_for("index"))

# ============= تعديل مادة =============
@app.route("/edit_subject/<int:index>", methods=["POST"])
def edit_subject(index):
    if 0 <= index < len(subjects):
        new_name = request.form.get("new_name")
        new_grade = request.form.get("new_grade")
        if new_name:
            subjects[index]["name"] = new_name
        if new_grade:
            subjects[index]["grade"] = float(new_grade)
    return redirect(url_for("index"))

# ============= حساب المعدل التراكمي =============
@app.route("/calculate_gpa", methods=["POST"])
def calculate_gpa():
    if not subjects:
        gpa = 0
    else:
        gpa = sum(sub["grade"] for sub in subjects) / len(subjects)
    return render_template("index.html", student=student_info, subjects=subjects, gpa=gpa)

# ============= طباعة PDF =============
@app.route("/print_pdf")
def print_pdf():
    # احسب المعدل
    gpa = sum(sub["grade"] for sub in subjects) / len(subjects) if subjects else 0

    # جهز الـ HTML مع مسار الخط
    rendered = render_template(
        "report.html",
        student=student_info,
        subjects=subjects,
        gpa=gpa,
        font_path=os.path.join(basedir, "static/fonts/Amiri-Regular.ttf")
    )

    # أنشئ ملف PDF
    pdf_path = os.path.join(basedir, "report.pdf")
    with open(pdf_path, "w+b") as pdf_file:
        pisa.CreatePDF(rendered, dest=pdf_file)

    return send_file(pdf_path, as_attachment=True)

# ================== تشغيل السيرفر ==================
if __name__ == "__main__":
    app.run(debug=True)
