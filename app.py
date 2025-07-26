from flask import Flask, render_template, request, redirect, url_for, send_file
from io import BytesIO
from weasyprint import HTML, CSS
from datetime import datetime
import os

app = Flask(__name__)

# ✅ بيانات افتراضية
subjects = []
student_name = ""
student_id = ""

@app.route("/")
def index():
    return render_template("index.html", subjects=subjects, student_name=student_name, student_id=student_id)

@app.route("/set_student", methods=["POST"])
def set_student():
    global student_name, student_id
    student_name = request.form.get("student_name")
    student_id = request.form.get("student_id")
    return redirect(url_for("index"))

@app.route("/add", methods=["POST"])
def add_subject():
    subject_name = request.form.get("subject")
    grade = float(request.form.get("grade"))
    subjects.append({"name": subject_name, "grade": grade})
    return redirect(url_for("index"))

@app.route("/delete/<int:index>", methods=["POST"])
def delete_subject(index):
    subjects.pop(index)
    return redirect(url_for("index"))

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit_subject(index):
    if request.method == "POST":
        subjects[index]["name"] = request.form.get("subject")
        subjects[index]["grade"] = float(request.form.get("grade"))
        return redirect(url_for("index"))
    return render_template("edit.html", subject=subjects[index])

@app.route("/calculate")
def calculate():
    if len(subjects) == 0:
        gpa = 0
    else:
        gpa = sum([sub["grade"] for sub in subjects]) / len(subjects)
    return render_template("index.html", subjects=subjects, student_name=student_name, student_id=student_id, gpa=gpa)

@app.route("/print_pdf")
def print_pdf():
    if len(subjects) == 0:
        gpa = 0
    else:
        gpa = sum([sub["grade"] for sub in subjects]) / len(subjects)

    # ✅ تجهيز البيانات والتاريخ
    current_date = datetime.now().strftime("%Y-%m-%d")

    # ✅ توليد HTML من القالب
    rendered_html = render_template("report.html", 
                                    subjects=subjects, 
                                    student_name=student_name, 
                                    student_id=student_id, 
                                    gpa=gpa, 
                                    date=current_date)

    # ✅ إنشاء PDF باستخدام WeasyPrint
    pdf_file = BytesIO()
    HTML(string=rendered_html, base_url=os.getcwd()).write_pdf(pdf_file)
    pdf_file.seek(0)

    return send_file(pdf_file, mimetype='application/pdf', download_name='GPA_Report.pdf')

if __name__ == "__main__":
    app.run(debug=True)
