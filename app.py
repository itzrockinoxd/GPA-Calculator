from flask import Flask, render_template, request, redirect, url_for, send_file
from weasyprint import HTML
import io
import datetime

app = Flask(__name__)

# بيانات مؤقتة في الذاكرة (لتجربة فقط)
student_info = {"name": "", "id": ""}
subjects = []

@app.route('/')
def index():
    return render_template('index.html', student=student_info, subjects=subjects)

@app.route('/save_student', methods=['POST'])
def save_student():
    student_info['name'] = request.form['student_name']
    student_info['id'] = request.form['student_id']
    return redirect(url_for('index'))

@app.route('/add_subject', methods=['POST'])
def add_subject():
    name = request.form['subject_name']
    grade = float(request.form['grade'])
    subjects.append({'name': name, 'grade': grade})
    return redirect(url_for('index'))

@app.route('/delete_subject/<int:index>', methods=['POST'])
def delete_subject(index):
    if 0 <= index < len(subjects):
        subjects.pop(index)
    return redirect(url_for('index'))

@app.route('/calculate_gpa')
def calculate_gpa():
    if not subjects:
        return redirect(url_for('index'))
    gpa = sum(sub['grade'] for sub in subjects) / len(subjects)
    return render_template('index.html', student=student_info, subjects=subjects, gpa=round(gpa, 2))

@app.route('/print_pdf')
def print_pdf():
    # نحسب المعدل التراكمي
    gpa = 0
    if subjects:
        gpa = sum(sub['grade'] for sub in subjects) / len(subjects)

    # نجهز HTML للطباعة
    rendered = render_template('report.html', student=student_info, subjects=subjects, gpa=round(gpa, 2), date=datetime.date.today())

    # نحول HTML إلى PDF مع base_url لقراءة static files
    pdf = HTML(string=rendered, base_url=request.root_path).write_pdf()

    # نرسل الملف PDF للمستخدم
    return send_file(io.BytesIO(pdf), download_name="gpa_report.pdf", as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)
