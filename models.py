
#ΔΗΜΙΟΥΡΓΙΑ ΚΛΑΣΗΣ STUDENT 
class Student:
    def __init__(self, firstname, lastname, email, birth_date):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.birth_date = birth_date

    def  __str__(self):
        return f'{self.firstname} {self.lastname}'

#ΔΗΜΙΟΥΡΓΙΑ ΚΛΑΣΗΣ DBStudent ΠΟΥ ΚΛΗΡΟΝΟΜΕΙ ΤΗΝ ΚΛΑΣΗ Student, ΠΡΟΣΘΕΤΕΙ ΤΟ ID
class DBStudent(Student):
    def __init__(self, id, firstname, lastname, email, birth_date):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.birth_date = birth_date

#ΔΗΜΙΟΥΡΓΙΑ ΤΗΣ ΚΛΑΣΗΣ Lesson
class Lesson:
    def __init__(self, title, teacher):
        self.title=title
        self.teacher=teacher

    def __str__(self):
        return f'{self.title} {self.teacher}'    

#ΔΗΜΙΟΥΡΓΙΑ ΚΛΑΣΗΣ DBLesson ΠΟΥ ΚΛΗΡΟΝΟΜΕΙ ΤΗΝ ΚΛΑΣΗ Lesson, ΠΡΟΣΘΕΤΕΙ ΤΟ ID
class DBLesson(Lesson):
    def __init__(self, id, title, teacher):
        self.id=id
        self.title=title
        self.teacher=teacher

#ΔΗΜΙΟΥΡΓΙΑ ΤΗΣ ΚΛΑΣΗΣ Grade 
class Grade:
    def __init__(self, student_id, lesson_id, grade):
        self.student_id=student_id
        self.lesson_id=lesson_id
        self.grade=grade

#ΔΗΜΙΟΥΡΓΙΑ ΚΛΑΣΗΣ DBGrade ΠΟΥ ΚΛΗΡΟΝΟΜΕΙ ΤΗΝ ΚΛΑΣΗ Grade, ΠΡΟΣΘΕΤΕΙ FIRST NAME, LAST NAME ΤΟΥ ΠΙΝΑΚΑ
# STUDENTS ΚΑΙ LESSON_TITLE ΤΟΥ ΠΙΝΑΚΑ LESSONS ΓΙΑ ΕΜΦΑΝΙΣΗ ΤΟΥΣ ΣΤΗ ΣΕΛΙΔΑ showGrades
     
class DBGrade(Grade):
    def __init__(self, student_id, lesson_id, firstname, lastname, lesson_title, grade):
        self.student_id=student_id
        self.lesson_id=lesson_id
        self.firstname=firstname
        self.lastname=lastname
        self.lesson_title=lesson_title
        self.grade=grade