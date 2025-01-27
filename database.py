import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
from models import Student, DBStudent, Lesson, DBLesson

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
    conn.commit()
    cur.close()
    conn.close()

def get_students():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM students;')
    rows = cur.fetchall()
    students = [DBStudent(id=row[0], firstname=row[1], lastname=row[2], email=row[3], birth_date=row[4]) for row in rows]
    cur.close()
    conn.close()
    return students

def get_lessons():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM lessons;')
    rows = cur.fetchall()
    lessons = [DBLesson(id=row[0], title=row[1], teacher=row[2]) for row in rows]
    cur.close()
    conn.close()
    return lessons

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


def save_student(student):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = 'INSERT INTO students (firstname, lastname, email, birth_date) VALUES (%s, %s, %s, %s);'
    values = (student.firstname, student.lastname, student.email, student.birth_date)
    cur.execute(sql,values)
    conn.commit()
    cur.close()
    conn.close()

def save_lesson(lesson):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = 'INSERT INTO lessons (title, teacher) VALUES (%s, %s);'
    values = (lesson.title, lesson.teacher)
    cur.execute(sql,values)
    conn.commit()
    cur.close()
    conn.close()

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

def delete_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DROP TABLE STUDENTS')
    conn.commit()
    cur.close()
    conn.close()