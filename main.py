from flask import Flask, redirect, url_for, request, render_template
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from forms import StudentForm
from models import Student, DBStudent, DBLesson, Lesson
from database import (get_db_connection, init_db, save_student, get_students, get_individual_student, edit_student, delete_student, delete_database)
from flask_bootstrap import Bootstrap5
import os
import psycopg2
import secrets
#import os
#from dotenv import load_dotenv

#dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
#if os.path.exists(dotenv_path):
#   load_dotenv(dotenv_path)
#   print('APP_NAME is {}'.format(os.environ.get('APP_NAME')))
#else:
#   raise RuntimeError('Not found application configuration')

app = Flask(__name__)
bootstrap = Bootstrap5(app)

csrf = CSRFProtect(app)
foo = secrets.token_urlsafe(16)
app.secret_key = foo



studentsss=[]

init_db()

#ΑΡΧΙΚΗ ΣΕΛΙΔΑ
@app.route('/')
def index():
    return render_template('home.html')

#ΣΕΛΙΔΑ ΠΟΥ ΔΕΙΧΝΕΙ ΟΛΟΥΣ ΤΟΥΣ ΜΑΘΗΤΕΣ
@app.route('/showStudents')
def show_students():
    students = get_students()
    print(students)
    return render_template('Students/showStudents.html', students=students)
            
#ΣΕΛΙΔΑ ΠΟΥ ΠΡΟΣΘΕΤΕΙ ΕΝΑΝ ΜΑΘΗΤΗ
@app.route('/addStudent', methods=['GET', 'POST'])
def show_student_form():
    if request.method == 'GET':
        form = StudentForm()
        return render_template('Students/addStudent.html', form=form)
    if request.method == 'POST':
        form = StudentForm()
        if form.validate_on_submit():
            student=Student(form.firstname.data, form.lastname.data, form.email.data, form.birth_date.data)
            save_student(student)
            print(student)
            return redirect(url_for("show_students", student=student))
        else:
            return render_template('Students/addStudent.html', form=form)   
         
#ΣΕΛΙΔΑ ΠΟΥ ΦΕΡΝΕΙ ΣΤΗΝ ΦΟΡΜΑ StudentForm ΤΟ ΧΡΗΣΤΗ ΠΟΥ ΕΠΙΛΕΞΑΜΕ
@app.route('/addStudent/<int:id>')
def show_student(id):
    found=False
    student = get_individual_student(id)
    if student:
        form = StudentForm(obj=student)
        return render_template('Students/addStudent.html', form=form)
    else:
        return render_template('Students/addStudent.html', message="Student not found")

#ΣΕΛΙΔΑ ΠΟΥ ΜΕ ΤΟ ΠΑΤΗΜΑ ΤΟΥ SUBMIT ΑΝΑΝΕΩΝΕΙ ΤΑ ΔΕΔΟΜΕΝΑ ΤΟΥ ΜΑΘΗΤΗ
@app.route('/addStudent/<int:id>', methods=['POST'])
def edit_selected_student(id):
    form = StudentForm()
    student = get_individual_student(id)
    if student:
        print(student)
        edited_student = Student(form.firstname.data, form.lastname.data, form.email.data, form.birth_date.data)
        edit_student(edited_student,id)
        students = get_students()
        return render_template('Students/showStudents.html', students=students, message="Student changed")
    else:
        students = get_students()
        return render_template('Students/showStudents.html', students=students, message="Student not changed")

@app.route('/deleteStudent/<int:id>')
def delete_student_from_db(id):
    found=False
    result = delete_student(id)
    print(result)
    students = get_students()
    if result:
        return render_template('Students/showStudents.html', students=students, message="Student deleted")
    else:
        return render_template('Students/showStudents.html', students=students, message="Student not found")
    
@app.route('/deleteDatabase')
def delete_the_database():
    delete_database()
    return render_template('home.html')