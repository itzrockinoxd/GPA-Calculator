from flask import Flask, render_template, request, redirect, url_for, make_response
import pdfkit

app = Flask(__name__)

# ✅ متغيرات لتخزين بيانات الطالب والمواد
subjects = []
student_name = ""
student_id = ""

@app.route('/')
def index():
    return render_template('index.html', subjects=subjects, student_name=student_name, student_id=student_id)

# ✅ حفظ بيانات الطالب
@app.route('/set_student', methods=['POST'])
def set_student():
    global student_name, student_id
    student_name = request.form['student_name']
    student_id = request.form['student_id']
    return redirect(url_for('index'))

# ✅ إضافة مادة
@app.route('/add', methods=['POST'])
def add_subject():
    subject_name = request.form['subject']
    grade = float(request.form['grade'])
    subjects.append({'name': subject_name, 'grade': grade})
    return redirect(url_for('index'))

# ✅ حساب المعدل
@app.route('/calculate', methods=['GET'])
def calculate_gpa():
    if len(subjects) == 0:
        gpa = 0
    else:
        total = sum(sub['grade'] for sub in subjects)
        gpa = round(total / len(subjects), 2)
    return render_template('index.html', subjects=subjects, student_name=student_name, student_id=student_id, gpa=gpa)

# ✅ حذف مادة
@app.route('/delete/<int:index>', methods=['POST'])
def delete_subject(index):
    if 0 <= index < len(subjects):
        subjects.pop(index)
    return redirect(url_for('index'))

# ✅ تعديل مادة (فتح صفحة التعديل وحفظها)
@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_subject(index):
    if request.method == 'POST':
        subjects[index]['name'] = request.form['subject']
        subjects[index]['grade'] = float(request.form['grade'])
        return redirect(url_for('index'))
    return render_template('edit.html', subject=subjects[index], index=index)

# ✅ طباعة PDF
@app.route('/print_pdf')
def print_pdf():
    rendered = render_template(
        'report.html',
        subjects=subjects,
        student_name=student_name,
        student_id=student_id,
        gpa=round(sum(sub['grade'] for sub in subjects) / len(subjects), 2) if subjects else 0
    )

    # ⚠️ عدل هذا المسار حسب مكان تثبيت wkhtmltopdf في جهازك
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

    pdf = pdfkit.from_string(rendered, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=GPA_Report.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)
