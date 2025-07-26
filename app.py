from flask import Flask, render_template, request, redirect, url_for, send_file
from weasyprint import HTML
import os

app = Flask(__name__)

# 📌 بيانات مؤقتة في الذاكرة (بدل قاعدة البيانات حالياً)
student_info = {"name": "", "id": ""}
subjects = []

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", student=student_info, subjects=subjects)

# ✅ حفظ بيانات الطالب
@app.route("/save_student", methods=["POST"])
def save_student():
    name = request.form.get("student_name")
    student_id = request.form.get("student_id")

    if not name or not student_id:
        return "❌ Missing name or ID", 400  # Bad Request إذا لم يرسل الحقول

    student_info["name"] = name
    student_info["id"] = student_id

    return redirect(url_for("index"))

# ✅ إضافة مادة
@app.route("/add_subject", methods=["POST"])
def add_subject():
    subject_name = request.form.get("subject_name")
    grade = request.form.get("subject_grade")

    if not subject_name or not grade:
        return "❌ Missing subject name or grade", 400

    subjects.append({"name": subject_name, "grade": float(grade)})
    return redirect(url_for("index"))

# ✅ حذف مادة
@app.route("/delete_subject/<int:index>", methods=["POST"])
def delete_subject(index):
    if 0 <= index < len(subjects):
        subjects.pop(index)
    return redirect(url_for("index"))

# ✅ حساب GPA
@app.route("/calculate_gpa", methods=["POST"])
def calculate_gpa():
    if not subjects:
        return "❌ No subjects to calculate GPA", 400

    total = sum(sub["grade"] for sub in subjects)
    gpa = round(total / len(subjects), 2)
    return f"<h1>📊 Final GPA: {gpa}</h1>"

# ✅ توليد PDF
@app.route("/print_pdf", methods=["GET"])
def print_pdf():
    html = render_template("report.html", student=student_info, subjects=subjects)
    pdf_file = "report.pdf"
    HTML(string=html).write_pdf(pdf_file)
    return send_file(pdf_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
