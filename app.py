from flask import Flask, render_template, request, redirect, url_for, session, Response
from weasyprint import HTML
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route('/')
def index():
    return render_template(
        'index.html',
        subjects=session.get('subjects', []),
        student_name=session.get('student_name'),
        student_id=session.get('student_id')
    )

@app.route('/add_subject', methods=['POST'])
def add_subject():
    subject = request.form.get('subject')
    grade = request.form.get('grade')

    if subject and grade:
        subjects = session.get('subjects', [])
        subjects.append({'subject': subject, 'grade': grade})
        session['subjects'] = subjects

    return redirect(url_for('index'))

@app.route('/delete_subject/<int:index>')
def delete_subject(index):
    subjects = session.get('subjects', [])
    if 0 <= index < len(subjects):
        subjects.pop(index)
        session['subjects'] = subjects
    return redirect(url_for('index'))

@app.route('/save_info', methods=['POST'])
def save_info():
    session['student_name'] = request.form.get('student_name')
    session['student_id'] = request.form.get('student_id')
    return redirect(url_for('index'))

@app.route('/calculate_gpa')
def calculate_gpa():
    subjects = session.get('subjects', [])
    if subjects:
        total = sum(float(sub['grade']) for sub in subjects)
        gpa = round(total / len(subjects), 2)
    else:
        gpa = 0
    return str(gpa)

@app.route('/print_pdf')
def print_pdf():
    subjects = session.get('subjects', [])
    student_name = session.get('student_name', '')
    student_id = session.get('student_id', '')

    # ✅ حساب المعدل
    if subjects:
        total = sum(float(sub['grade']) for sub in subjects)
        gpa = round(total / len(subjects), 2)
    else:
        gpa = 0

    # ✅ إضافة التاريخ
    current_date = datetime.now().strftime("%Y-%m-%d")

    rendered = render_template(
        'report.html',
        subjects=subjects,
        student_name=student_name,
        student_id=student_id,
        gpa=gpa,
        current_date=current_date
    )

    pdf = HTML(string=rendered).write_pdf()
    return Response(pdf, mimetype='application/pdf')


if __name__ == "__main__":
    app.run(debug=True)
