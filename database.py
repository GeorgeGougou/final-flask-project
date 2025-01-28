import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
from models import Student, DBStudent, Lesson, DBLesson, Grade

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
   load_dotenv(dotenv_path)
   print('DB_HOST is {}'.format(os.environ.get('DB_HOST')))
else:
   raise RuntimeError('Not found application configuration')

def get_db_connection():
    conn = psycopg2.connect(host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'])
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('CREATE TABLE if not exists students (id SERIAL PRIMARY KEY,'
                'firstname VARCHAR(100),'
                'lastname VARCHAR(100),'
                'email VARCHAR(100),'
                'birth_date DATE);'
                )
    cur.execute('CREATE TABLE if not exists lessons (id SERIAL PRIMARY KEY,'
                 'title VARCHAR(100),'
                 'teacher VARCHAR(100));'
                 )
    cur.execute('CREATE TABLE if not exists grades (student_id INT NOT NULL,'
                'lesson_id INT NOT NULL,'
                'grade FLOAT NOT NULL,'
                'PRIMARY KEY (student_id, lesson_id),'
                'CONSTRAINT fk_student FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,'
                'CONSTRAINT fk_lesson FOREIGN KEY (lesson_id) REFERENCES lessons (id) ON DELETE CASCADE);'
                 )
    conn.commit()
    cur.close()
    conn.close()



#ΕΜΦΑΝΙΣΗ ΟΛΩΝ ΤΩΝ ΜΑΘΗΤΩΝ
def get_students():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM students;')
    rows = cur.fetchall()
    students = [DBStudent(id=row[0], firstname=row[1], lastname=row[2], email=row[3], birth_date=row[4]) for row in rows]
    cur.close()
    conn.close()
    return students

#ΕΜΦΑΝΙΣΗ ΟΛΩΝ ΤΩΝ ΜΑΘΗΜΑΤΩΝ
def get_lessons():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM lessons;')
    rows = cur.fetchall()
    lessons = [DBLesson(id=row[0], title=row[1], teacher=row[2]) for row in rows]
    cur.close()
    conn.close()
    return lessons


#ΕΜΦΑΝΙΣΗ ΟΛΩΝ ΤΩΝ ΒΑΘΜΩΝ
def get_grades():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM grades;')
    rows = cur.fetchall()
    grades = [Grade(student_id=row[0], lesson_id=row[1], grade=row[2]) for row in rows]
    cur.close()
    conn.close()
    return grades

#ΕΜΦΑΝΙΣΗ ΣΥΓΚΕΚΡΙΜΕΝΟΥ ΜΑΘΗΤΗ
def get_individual_student(studentid: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select * from students where id = %s;', (studentid, ))
    row = cur.fetchone()
    print(row)
    if row is None:
        return None
    birth_date = datetime.strptime(row[4], '%Y-%m-%d')
    student=DBStudent(id=row[0], firstname=row[1], lastname=row[2],email=row[3], birth_date=birth_date)
    cur.close()
    conn.close()
    return student

#ΕΜΦΑΝΙΣΗ ΣΥΓΚΕΚΡΙΜΕΝΟΥ ΜΑΘΗΜΑΤΟΣ
def get_individual_lesson(lessonid: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select * from lessons where id = %s;', (lessonid, ))
    row = cur.fetchone()
    print(row)
    if row is None:
        return None
    lesson=DBLesson(id=row[0], title=row[1], teacher=row[2])
    cur.close()
    conn.close()
    return lesson


#ΕΜΦΑΝΙΣΗ ΒΑΘΜΩΝ ΣΥΓΚΕΡΙΜΕΝΟΥ ΦΟΙΤΗΤΗ
def get_individual_student_grades(student_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select * from grades where student_id = %s;', (student_id, ))
    rows = cur.fetchall()
    grades = [Grade(student_id=row[0], lesson_id=row[1], grade=row[2]) for row in rows]
    cur.close()
    conn.close()
    return grades

#ΕΜΦΑΝΙΣΗ ΒΑΘΜΩΝ ΣΥΓΚΕΡΚΙΜΕΝΟΥ ΜΑΘΗΜΑΤΟΣ
def get_individual_lesson_grades(lesson_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select * from grades where lesson_id = %s;', (lesson_id, ))
    rows = cur.fetchall()
    grades = [Grade(student_id=row[0], lesson_id=row[1], grade=row[2]) for row in rows]
    cur.close()
    conn.close()
    return grades

#ΕΜΦΑΝΙΣΗ ΒΑΘΜΟΥ ΜΑΘΗΤΗ ΣΕ ΣΥΓΚΕΚΡΙΜΕΝΟ ΜΑΘΗΜΑ
def get_individual_grade(student_id: int, lesson_id : int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select * from grades where student_id = %s and lesson_id = %s ;', (student_id,lesson_id))
    row = cur.fetchone()
    print(row)
    if row is None:
        return None
    grade=Grade(student_id=row[0], lesson_id=row[1], grade=row[2])
    cur.close()
    conn.close()
    return grade


#ΑΠΟΘΗΚΕΥΣΗ ΜΑΘΗΤΗ
def save_student(student):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = 'INSERT INTO students (firstname, lastname, email, birth_date) VALUES (%s, %s, %s, %s);'
    values = (student.firstname, student.lastname, student.email, student.birth_date)
    cur.execute(sql,values)
    conn.commit()
    cur.close()
    conn.close()

#ΑΠΟΘΗΚΕΥΣΗ ΜΑΘΗΜΑΤΟΣ
def save_lesson(lesson):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = 'INSERT INTO lessons (title, teacher) VALUES (%s, %s);'
    values = (lesson.title, lesson.teacher)
    cur.execute(sql,values)
    conn.commit()
    cur.close()
    conn.close()

#ΑΠΟΘΗΚΕΥΣΗ ΒΑΘΜΟΥ 
def save_grade(studentGrade):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = 'INSERT INTO grades (student_id, lesson_id, grade) VALUES (%s, %s, %s);'
    values = (studentGrade.student_id, studentGrade.lesson_id, studentGrade.grade)   
    cur.execute(sql,values)
    conn.commit()
    cur.close()
    conn.close()

#ΕΠΕΞΕΡΓΑΣΙΑ ΜΑΘΗΤΗ
def edit_student(student,id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'UPDATE students SET firstname = %s, lastname = %s, email = %s, birth_date = %s WHERE id = %s;',
        (student.firstname, student.lastname, student.email, student.birth_date, id)
    )
    print('query')
    conn.commit()
    cur.close()
    conn.close()

#ΕΠΕΞΕΡΓΑΣΙΑ ΜΑΘΗΜΑΤΟΣ
def edit_lesson(lesson,id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'UPDATE lessons SET title = %s, teacher = %s WHERE id = %s;',
        (lesson.title, lesson.teacher, id)
    )
    print('query')
    conn.commit()
    cur.close()
    conn.close()

#ΕΠΕΞΕΡΓΑΣΙΑ ΒΑΘΜΟΥ
def edit_grade(studentGrade,student_id,lesson_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'UPDATE grades SET student_id=%s, lesson_id=%s, grade = %s WHERE student_id=%s AND lesson_id=%s;',
        (student_id,lesson_id,studentGrade.grade,student_id,lesson_id)
    )
    print('query')
    conn.commit()
    cur.close()
    conn.close()

#ΔΙΑΓΡΑΦΗ ΜΑΘΗΤΗ
def delete_student(studentid: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM students WHERE id = %s;', (studentid, ))
    row = cur.fetchone()
    print(row)
    if row is None:
        cur.close()
        conn.close()
        return False
    cur.execute('DELETE FROM students WHERE id = %s;', (studentid, ))
    conn.commit()
    cur.close()
    conn.close()
    return True


#ΔΙΑΓΡΑΦΗ ΜΑΘΗΜΑΤΟΣ
def delete_lesson(lessonid: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM lessons WHERE id = %s;', (lessonid, ))
    row = cur.fetchone()
    print(row)
    if row is None:
        cur.close()
        conn.close()
        return False
    cur.execute('DELETE FROM lessons WHERE id = %s;', (lessonid, ))
    conn.commit()
    cur.close()
    conn.close()
    return True

#ΔΙΑΓΡΑΦΗ ΒΑΘΜΟΥ
def delete_grade(student_id: int, lesson_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM grades WHERE student_id = %s AND lesson_id = %s;', (student_id,lesson_id))
    row = cur.fetchone()
    print(row)
    if row is None:
        cur.close()
        conn.close()
        return False
    cur.execute('DELETE FROM grades WHERE student_id = %s AND lesson_id = %s;', (student_id,lesson_id))
    conn.commit()
    cur.close()
    conn.close()
    return True

#ΜΕΤΡΗΣΗ ΜΕΣΟΥ ΟΡΟΥ ΚΑΘΕ ΜΑΘΗΤΗ
def get_all_student_avg():
    #ΔΗΜΙΟΥΡΓΙΑ ΕΝΟΣ ΚΕΝΟΥ DICTIONARY ΠΟΥ ΘΑ ΑΠΟΘΗΚΕΥΤΟΥΝ ΤΟ STUDENT ID ΚΑΙ Ο ΜΕΣΟΣ ΟΡΟΣ ΤΟΥ
    student_avgs={}
    conn = get_db_connection()
    cur = conn.cursor()
    #ΛΗΨΗ ΑΠΟ ΤΗΝ ΒΑΣΗ ΤΟ ΜΕΣΟ ΟΡΟ ΚΑΘΕ ΜΑΘΗΤΗ ΞΕΧΩΡΙΣΤΑ
    cur.execute('SELECT student_id, AVG(grade) FROM grades GROUP BY student_id;')
    rows=cur.fetchall()
    for row in rows:
        #ΠΡΟΣΘΗΚΗ ΣΤΟ DICTIONARY ΤΟΥ ΜΕΣΟΥ ΟΡΟΥ ΕΝΟΣ ΜΑΘΗΜΑΤΟΣ, ΕΞΑΓΩΓΗ ΤΟΥ ΑΡΙΘΜΟΥ ΑΠΟ ΤΟ TUPLE ΚΑΙ ΣΤΡΟΓΓΥΛΟΠΟΙΗΣΗ
        #ΣΤΟ 1 ΔΕΚΑΔΙΚΟ
        student_avgs[row[0]]=round(float(row[1]),1)
    conn.commit()
    cur.close()
    conn.close()
    return student_avgs

#ΜΕΤΡΗΣΗ ΜΕΣΟΥ ΟΡΟΥ ΤΑΞΗΣ ΚΑΙ ΜΑΘΗΜΑΤΩΝ
def get_class_avg():
    #ΔΗΜΙΟΥΡΓΙΑ ΕΝΟΣ ΚΕΝΟΥ DICTIONARY ΠΟΥ ΘΑ ΑΠΟΘΗΚΕΥΤΟΥΝ ΤΑ LESSON ID ΚΑΙ Ο ΜΕΣΟΣ ΟΡΟΣ ΤΟΥ
    lesson_avgs={}
    conn = get_db_connection()
    cur = conn.cursor()
    #ΛΗΨΗ ΑΠΟ ΤΗΝ ΒΑΣΗ ΤΟΥ ΣΥΝΟΛΙΚΟΥ ΜΕΣΟΥ ΟΡΟΥ ΤΗΣ ΤΑΞΗΣ
    cur.execute('SELECT AVG(grade) FROM grades')
    #ΣΤΡΟΓΓΥΛΟΠΟΙΗΣΗ ΤΟΥ ΑΡΙΘΜΟΥ ΣΤΟ 1 ΔΕΚΑΔΙΚΟ
    avg=cur.fetchone()
    classAvg=round(float(avg[0]),1)
    #ΛΗΨΗ ΑΠΟ ΤΗΝ ΒΑΣΗ ΤΟΥ ΜΕΣΟ ΟΡΟ ΚΑΘΕ ΜΑΘΗΜΑΤΟΣ ΞΕΧΩΡΙΣΤΑ
    cur.execute('SELECT lesson_id, AVG(grade) FROM grades GROUP BY lesson_id;')
    rows=cur.fetchall()
    for row in rows:
        #ΠΡΟΣΘΗΚΗ ΣΤΟ DICTIONARY ΤΟΥ ΜΕΣΟΥ ΟΡΟΥ ΕΝΟΣ ΜΑΘΗΜΑΤΟΣ, ΕΞΑΓΩΓΗ ΤΟΥ ΑΡΙΘΜΟΥ ΑΠΟ ΤΟ TUPLE ΚΑΙ ΣΤΡΟΓΓΥΛΟΠΟΙΗΣΗ
        #ΣΤΟ 1 ΔΕΚΑΔΙΚΟ
        lesson_avgs[row[0]]=round(float(row[1]),1)
    conn.commit()
    cur.close()
    conn.close()
    return classAvg, lesson_avgs
        
    

#ΔΙΑΓΡΑΦΗ ΠΙΝΑΚΑ
def delete_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM grades')
    cur.execute('DELETE FROM lessons')
    cur.execute('DELETE FROM students')
    conn.commit()
    cur.close()
    conn.close()