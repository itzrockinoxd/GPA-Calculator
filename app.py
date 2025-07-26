from flask import Flask, render_template, request, redirect, url_for, send_file
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

# -------- Temporary Data Storage --------
student_info = {"name": "", "id": ""}
subjects = []  # Each subject will be stored as {"name": "Math", "grade": 95}


# -------- Home Route --------
@app.route('/')
def index():
    return render_template('index.html', student=student_info, subjects=subjects)


# -------- Save Student Info --------
@app.route('/save_student', methods=['POST'])
def save_student():
    student_info["name"] = request.form.get("student_name")
    student_info["id"] = request.form.get("student_id")
    return redirect(url_for('index'))


# -------- Add Subject --------
@app.route('/add_subject', methods=['POST'])
def add_subject():
    subject_name = request.form.get("subject_name")
    grade = request.form.get("grade")

    if subject_name and grade:
        subjects.append({"name": subject_name, "grade": float(grade)})
    return redirect(url_for('index'))


# -------- Delete Subject --------
@app.route('/delete_subject/<int:index>')
def delete_subject(index):
    if 0 <= index < len(subjects):
        subjects.pop(index)
    return redirect(url_for('index'))


# -------- Edit Subject (optional future feature) --------
@app.route('/edit_subject/<int:index>', methods=['POST'])
def edit_subject(index):
    if 0 <= index < len(subjects):
        subjects[index]["name"] = request.form.get("subject_name")
        subjects[index]["grade"] = float(request.form.get("grade"))
    return redirect(url_for('index'))


# -------- Calculate GPA --------
@app.route('/calculate_gpa')
def calculate_gpa():
    if len(subjects) == 0:
        gpa = 0
    else:
        gpa = sum(sub["grade"] for sub in subjects) / len(subjects)

    return render_template('index.html', student=student_info, subjects=subjects, gpa=round(gpa, 2))


# -------- Generate PDF --------
@app.route('/print_pdf')
def print_pdf():
    if len(subjects) == 0:
        return "⚠️ لا توجد مواد لحساب المعدل."

    gpa = sum(sub["grade"] for sub in subjects) / len(subjects)

    # Render the HTML Template
    rendered = render_template('report.html',
                               student_name=student_info["name"],
                               student_id=student_info["id"],
                               subjects=subjects,
                               gpa=gpa,
                               today=datetime.today().strftime('%Y-%m-%d'))

    # Convert HTML to PDF
    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(rendered, dest=pdf_file)

    if pisa_status.err:
        return "❌ Error generating PDF", 500

    pdf_file.seek(0)
    return send_file(pdf_file, download_name="gpa_report.pdf", as_attachment=True)


# -------- Run the Flask App --------
if __name__ == '__main__':
    app.run(debug=True)
