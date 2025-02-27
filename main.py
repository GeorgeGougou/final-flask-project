#IMPORT ΤΩΝ ΒΙΒΛΙΟΘΗΚΩΝ ΚΑΙ ΚΛΑΣΕΩΝ ΠΟΥ ΘΑ ΧΡΗΣΙΜΟΠΟΙΗΣΟΥΜΕ
from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from forms import StudentForm, LessonForm, GradeForm, EditGradeFrom
from models import Student, DBStudent, DBLesson, Lesson, Grade, DBGrade
from database import (get_db_connection, init_db, save_student, save_lesson, save_grade, get_students, 
                      get_lessons, get_individual_student, get_individual_lesson, edit_student, edit_lesson,
                      delete_student, delete_lesson, get_grades,get_individual_grade, edit_grade, 
                      delete_grade, get_all_student_avg, get_class_avg)
from flask_bootstrap import Bootstrap5
import os
import psycopg2
import secrets


app = Flask(__name__)
bootstrap = Bootstrap5(app)

#ΠΡΟΣΘΗΚΗ ΤΟΥ CSRF Protection
csrf = CSRFProtect(app)
foo = secrets.token_urlsafe(16)
app.secret_key = foo

#ΔΗΜΙΟΥΡΓΙΑ ΤΗΣ DATABASE ΕΑΝ ΔΕΝ ΥΠΑΡΧΕΙ
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

#ΣΕΛΙΔΑ ΠΟΥ ΔΙΕΧΝΕΙ ΟΛΑ ΤΑ ΜΑΘΗΜΑΤΑ
@app.route('/showLessons')
def show_lessons():
    lessons = get_lessons()
    print(lessons)
    return render_template('Lessons/showLessons.html', lessons=lessons)


#ΣΕΛΙΔΑ ΠΟΥ ΔΙΕΧΝΕΙ ΟΛΟΥΣ ΤΟΥΣ ΒΑΘΜΟΥΣ
@app.route('/showGrades')
def show_grades():
    grades = get_grades()
    print(grades)
    return render_template('Grades/showGrades.html', grades=grades)

#ΣΕΛΙΔΑ ΠΟΥ ΠΡΟΣΘΕΤΕΙ ΕΝΑΝ ΜΑΘΗΤΗ
@app.route('/addStudent', methods=['GET', 'POST'])
def show_student_form():
    #ΕΜΦΑΝΙΣΗ ΤΗΣ ΦΟΡΜΑΣ ΣΥΜΠΛΗΡΩΣΗΣ ΣΤΟΙΧΕΙΩΝ
    if request.method == 'GET':
        form = StudentForm()
        return render_template('Students/addStudent.html', form=form)
    if request.method == 'POST':
        #ΚΑΤΑΧΩΡΗΣΗ ΤΩΝ ΣΤΟΙΧΕΙΩΝ ΜΕ ΤΟ ΠΑΤΗΜΑ ΤΟΥ SUBMIT
        form = StudentForm()
        if form.validate_on_submit():
            student=Student(form.firstname.data, form.lastname.data, form.email.data, form.birth_date.data)
            save_student(student)
            print(student)
            students=get_students()
            return render_template('Students/showStudents.html', students=students, 
                                   successMsg='Student Added')
        else:
            return render_template('Students/addStudent.html', form=form, 
                                   warningMsg='Something went wrong!')

#ΣΕΛΙΔΑ ΠΟΥ ΠΡΟΣΘΕΤΕΙ ΕΝΑ ΜΑΘΗΜΑ
@app.route('/addLesson', methods=['GET', 'POST'])
def show_lesson_form():
    if request.method == 'GET':
        #ΕΜΦΑΝΙΣΗ ΤΗΣ ΦΟΡΜΑΣ ΣΥΜΠΛΗΡΩΣΗΣ ΣΤΟΙΧΕΙΩΝ
        form = LessonForm()
        return render_template('Lessons/addLesson.html', form=form)
    if request.method == 'POST':
        #ΚΑΤΑΧΩΡΗΣΗ ΤΩΝ ΣΤΟΙΧΕΙΩΝ ΜΕ ΤΟ ΠΑΤΗΜΑ ΤΟΥ SUBMIT
        form = LessonForm()
        if form.validate_on_submit():
            lesson=Lesson(form.title.data, form.teacher.data)
            save_lesson(lesson)
            print(lesson)
            lessons=get_lessons()
            return render_template('Lessons/showLessons.html', lessons=lessons, successMsg='Lesson Added')
        else:
            return render_template('Lessons/addLesson.html', form=form, warningMsg='Something went wrong!') 

#ΣΕΛΙΔΑ ΠΟΥ ΠΡΟΣΘΕΤΕΙ ΕΝΑ ΒΑΘΜΟ
@app.route('/addGrade', methods=['GET', 'POST'])
def show_grade_form():
    #ΛΗΨΗ ΤΩΝ ΜΑΘΗΤΩΝ ΚΑΙ ΜΑΘΗΜΑΤΩΝ ΠΟΥ ΕΧΟΥΝ ΠΡΟΣΤΕΘΕΙ
    students=get_students()
    lessons=get_lessons()
    if request.method == 'GET':
        #ΕΜΦΑΝΙΣΗ ΤΗΣ ΦΟΡΜΑΣ ΣΥΜΠΛΗΡΩΣΗΣ ΣΤΟΙΧΕΙΩΝ
        form = GradeForm()
        #ΕΜΦΑΝΙΣΗ ΤΩΝ STUDENT ID ΚΑΙ LESSON ID ΠΟΥ ΕΧΟΥΝ ΚΑΤΑΧΩΡΗΘΕΙ
        form.student_id.choices=[student.id for student in students]
        form.lesson_id.choices=[lesson.id for lesson in lessons]
        return render_template('Grades/addGrade.html', form=form)
    if request.method == 'POST':
        #ΚΑΤΑΧΩΡΗΣΗ ΤΩΝ ΣΤΟΙΧΕΙΩΝ ΜΕ ΤΟ ΠΑΤΗΜΑ ΤΟΥ SUBMIT
        form = GradeForm()
        form.student_id.choices=[student.id for student in students]
        form.lesson_id.choices=[lesson.id for lesson in lessons]
        if form.validate_on_submit():
            grade=Grade(form.student_id.data, form.lesson_id.data, form.grade.data)
            #ΕΛΕΓΧΟΣ ΑΝ Ο ΜΑΘΗΤΗΣ ΕΧΕΙ ΗΔΗ ΒΑΘΜΟ ΣΤΟ ΜΑΘΗΜΑ
            try:
                save_grade(grade)
                print(grade)
            except psycopg2.errors.UniqueViolation:
                return render_template('Grades/addGrade.html', form=form, 
                                       warningMsg='Student already has a grade in this lesson')
            else:
                grades=get_grades()
                return render_template('Grades/showGrades.html', grades=grades, successMsg='Grade Added')
        else:
            return render_template('Grades/addGrade.html', form=form, warningMsg='Something went wrong')  
         
#ΣΕΛΙΔΑ ΠΟΥ ΦΕΡΝΕΙ ΣΤΗΝ ΦΟΡΜΑ StudentForm ΤΟΝ ΜΑΘΗΤΗ ΠΟΥ ΕΠΙΛΕΞΑΜΕ
@app.route('/addStudent/<int:id>')
def show_student(id):
    student = get_individual_student(id)
    if student:
        form = StudentForm(obj=student)
        return render_template('Students/addStudent.html', form=form)
    else:
        return render_template('Students/addStudent.html', warningMsg="Student not found")

#ΣΕΛΙΔΑ ΠΟΥ ΦΕΡΝΕΙ ΣΤΗΝ ΦΟΡΜΑ LessonForm ΤΟ ΜΑΘΗΜΑ ΠΟΥ ΕΠΙΛΕΞΑΜΕ
@app.route('/addLesson/<int:id>')
def show_lesson(id):
    lesson = get_individual_lesson(id)
    if lesson:
        form = LessonForm(obj=lesson)
        return render_template('Lessons/addLesson.html', form=form)
    else:
        return render_template('Lessons/addLesson.html', warningMsg="Lesson not found")   

#ΣΕΛΙΔΑ ΠΟΥ ΦΕΡΝΕΙ ΣΤΗΝ ΦΟΡΜΑ GradeForm ΤΟΝ ΒΑΘΜΟ ΠΟΥ ΕΠΙΛΕΞΑΜΕ
@app.route('/addGrade/<int:student_id>/<int:lesson_id>')
def show_grade(student_id,lesson_id):
    grade = get_individual_grade(student_id,lesson_id)
    if grade:
        form = EditGradeFrom(obj=grade)
        return render_template('Grades/addGrade.html', form=form)
    else:
        return render_template('Grades/addGrade.html', warningMsg="Grade not found")  

#ΣΕΛΙΔΑ ΠΟΥ ΜΕ ΤΟ ΠΑΤΗΜΑ ΤΟΥ SUBMIT ΑΝΑΝΕΩΝΕΙ ΤΑ ΔΕΔΟΜΕΝΑ ΤΟΥ ΜΑΘΗΤΗ
@app.route('/addStudent/<int:id>', methods=['POST'])
def edit_selected_student(id):
    form = StudentForm()
    student = get_individual_student(id)
    if student:
        print(student)
        edited_student = Student(form.firstname.data, form.lastname.data, form.email.data,
                                  form.birth_date.data)
        edit_student(edited_student,id)
        students = get_students()
        return render_template('Students/showStudents.html', students=students, successMsg="Student changed")
    else:
        students = get_students()
        return render_template('Students/showStudents.html', students=students, 
                               warningMsg="Student not found")

#ΣΕΛΙΔΑ ΠΟΥ ΜΕ ΤΟ ΠΑΤΗΜΑ ΤΟΥ SUBMIT ΑΝΑΝΕΩΝΕΙ ΤΑ ΔΕΔΟΜΕΝΑ ΤΟΥ ΜΑΘΗΜΑΤΟΣ
@app.route('/addLesson/<int:id>', methods=['POST'])
def edit_selected_lesson(id):
    form = LessonForm()
    lesson = get_individual_lesson(id)
    if lesson:
        print(lesson)
        edited_lesson = Lesson(form.title.data, form.teacher.data)
        edit_lesson(edited_lesson,id)
        lessons = get_lessons()
        return render_template('Lessons/showLessons.html', lessons=lessons, successMsg="Lesson changed")
    else:
        lessons = get_lessons()
        return render_template('Lessons/showLessons.html', lessons=lessons, warningMsg="Lesson not found")

#ΣΕΛΙΔΑ ΠΟΥ ΜΕ ΤΟ ΠΑΤΗΜΑ ΤΟΥ SUBMIT ΑΝΑΝΕΩΝΕΙ ΤΑ ΔΕΔΟΜΕΝΑ ΤΟΥ ΒΑΘΜΟΥ
@app.route('/addGrade/<int:student_id>/<int:lesson_id>', methods=['POST'])
def edit_selected_grade(student_id,lesson_id):
    form = EditGradeFrom()
    students=get_students()
    lessons=get_lessons()
    form.student_id.choices=[student.id for student in students]
    form.lesson_id.choices=[lesson.id for lesson in lessons]
    studentGrade = get_individual_grade(student_id,lesson_id)
    if studentGrade:
        print(studentGrade)
        edited_grade = Grade(form.student_id.data, form.lesson_id.data, form.grade.data)
        edit_grade(edited_grade,student_id,lesson_id)
        grades = get_grades()
        return render_template('Grades/showGrades.html', grades=grades, successMsg="Grade changed")
    else:
        grades = get_grades()
        return render_template('Grades/showGrades.html', grades=grades, warningMsg="Grade not found")

#ΣΕΛΙΔΑ ΠΟΥ ΔΙΑΓΡΑΦΕΙ ΕΝΑ ΜΑΘΗΤΗ
@app.route('/deleteStudent/<int:id>')
def delete_student_from_db(id):
    result = delete_student(id)
    print(result)
    students = get_students()
    if result:
        return render_template('Students/showStudents.html', students=students, successMsg="Student deleted")
    else:
        return render_template('Students/showStudents.html', students=students, warningMsg="Student not found")

#ΣΕΛΙΔΑ ΠΟΥ ΔΙΑΓΡΑΦΕΙ ΕΝΑ ΦΟΙΤΗΤΗ
@app.route('/deleteLesson/<int:id>')
def delete_lesson_from_db(id):
    result = delete_lesson(id)
    print(result)
    lessons = get_lessons()
    if result:
        return render_template('Lessons/showLessons.html', lessons=lessons, successMsg="Lesson deleted")
    else:
        return render_template('Lessons/showLessons.html', lessons=lessons, warningMsg="Lesson not found")

#ΣΕΛΙΔΑ ΠΟΥ ΔΙΑΓΡΑΦΕΙ ΕΝΑ ΒΑΘΜΟ
@app.route('/deleteGrade/<int:student_id>/<int:lesson_id>')
def delete_grade_from_db(student_id,lesson_id):
    result = delete_grade(student_id,lesson_id)
    print(result)
    grades = get_grades()
    if result:
        return render_template('Grades/showGrades.html', grades=grades, successMsg="Grade deleted")
    else:
        return render_template('Grades/showGrades.html', grades=grades, warningMsg="Grade not deleted")

#ΣΕΛΙΔΑ ΠΟΥ ΦΕΡΝΕΙ ΤΟΝ ΜΕΣΟ ΟΡΟ ΟΛΩΝ ΤΩΝ ΜΑΘΗΤΩΝ
@app.route('/showAvgs')
def student_averages():
    avgs=get_all_student_avg()
    return render_template('Average_Scores/showAvgs.html', avgs=avgs)

#ΣΕΛΙΔΑ ΠΟΥ ΦΕΡΝΕΙ ΤΟΝ ΜΕΣΟ ΟΡΟ ΤΗΣ ΤΑΞΗΣ  
@app.route('/showClassAvgs')
def class_averages():
    classAvg, avgs=get_class_avg()
    return render_template('Average_Scores/showClassAvgs.html', avgs=avgs, classAvg=classAvg)


