from flask import Flask, render_template, request, redirect, url_for, session
from xhtml2pdf import pisa
import io
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"  # ضروري لاستخدام session

subjects = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # جلب اسم الطالب ورقم الجلوس من الفورم
        student_name = request.form.get("student_name")
        student_id = request.form.get("student_id")
        
        # حفظ البيانات في session
        session["student_name"] = student_name
        session["student_id"] = student_id
        
        return redirect(url_for("index"))

    return render_template("index.html", 
                           student_name=session.get("student_name", ""),
                           student_id=session.get("student_id", ""),
                           subjects=subjects)

@app.route("/add_subject", methods=["POST"])
def add_subject():
    subject_name = request.form.get("subject_name")
    grade = float(request.form.get("grade"))
    subjects.append({"name": subject_name, "grade": grade})
    return redirect(url_for("index"))

@app.route("/delete_subject/<int:index>", methods=["POST"])
def delete_subject(index):
    if 0 <= index < len(subjects):
        subjects.pop(index)
    return redirect(url_for("index"))

@app.route("/print_pdf")
def print_pdf():
    # تجهيز بيانات التقرير
    student_name = session.get("student_name", "Unknown")
    student_id = session.get("student_id", "Unknown")
    gpa = round(sum([s['grade'] for s in subjects]) / len(subjects), 2) if subjects else 0

    rendered = render_template("report.html", 
                               student_name=student_name, 
                               student_id=student_id, 
                               subjects=subjects, 
                               gpa=gpa,
                               date=datetime.today().strftime('%Y-%m-%d'))

    pdf = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(rendered), dest=pdf)
    if pisa_status.err:
        return "Error generating PDF", 500

    pdf.seek(0)
    return pdf.getvalue(), 200, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'inline; filename=report.pdf'
    }

if __name__ == "__main__":
    app.run(debug=True)
