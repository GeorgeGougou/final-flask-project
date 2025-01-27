from flask import Flask, redirect, url_for, request, render_template
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from forms import StudentForm, LessonForm
from models import Student, DBStudent, DBLesson, Lesson
from database import (get_db_connection, init_db, save_student, save_lesson, get_students, get_lessons, get_individual_student, get_individual_lesson, 
                      edit_student, edit_lesson, delete_student, delete_lesson, delete_database)
from flask_bootstrap import Bootstrap5
import os
import psycopg2
import secrets




app = Flask(__name__)
bootstrap = Bootstrap5(app)

csrf = CSRFProtect(app)
foo = secrets.token_urlsafe(16)
app.secret_key = foo


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

@app.route('/showLessons')
def show_lessons():
    lessons = get_lessons()
    print(lessons)
    return render_template('Lessons/showLessons.html', lessons=lessons)
            
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

@app.route('/addLesson', methods=['GET', 'POST'])
def show_lesson_form():
    if request.method == 'GET':
        form = LessonForm()
        return render_template('Lessons/addLesson.html', form=form)
    if request.method == 'POST':
        form = LessonForm()
        if form.validate_on_submit():
            lesson=Lesson(form.title.data, form.teacher.data)
            save_lesson(lesson)
            print(lesson)
            return redirect(url_for("show_lessons", lesson=lesson))
        else:
            return render_template('Lessons/addLesson.html', form=form) 
   
         
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
    
@app.route('/addLesson/<int:id>')
def show_lesson(id):
    found=False
    lesson = get_individual_lesson(id)
    if lesson:
        form = LessonForm(obj=lesson)
        return render_template('Lessons/addLesson.html', form=form)
    else:
        return render_template('Lessons/addLesson.html', message="Lesson not found")   
     

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

@app.route('/addLesson/<int:id>', methods=['POST'])
def edit_selected_lesson(id):
    form = LessonForm()
    lesson = get_individual_lesson(id)
    if lesson:
        print(lesson)
        edited_lesson = Lesson(form.title.data, form.teacher.data)
        edit_lesson(edited_lesson,id)
        lessons = get_lessons()
        return render_template('Lessons/showLessons.html', lessons=lessons, message="Lesson changed")
    else:
        lessons = get_lessons()
        return render_template('Lessons/showLessons.html', lessons=lessons, message="Lesson not changed")


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
    
@app.route('/deleteLesson/<int:id>')
def delete_lesson_from_db(id):
    found=False
    result = delete_lesson(id)
    print(result)
    lessons = get_lessons()
    if result:
        return render_template('Lessons/showLessons.html', lessons=lessons, message="Lesson deleted")
    else:
        return render_template('Lessons/showLessons.html', lessons=lessons, message="Lesson not deleted")



    
@app.route('/deleteDatabase')
def delete_the_database():
    delete_database()
    return render_template('home.html')