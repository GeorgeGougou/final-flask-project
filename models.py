class Student:
    def __init__(self, firstname, lastname, email, birth_date):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.birth_date = birth_date

    def  __str__(self):
        return f'{self.firstname} {self.lastname}'
    
class DBStudent(Student):
    def __init__(self, id, firstname, lastname, email, birth_date):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.birth_date = birth_date


class Lesson:
    def __init__(self, title, teacher):
        self.title=title
        self.teacher=teacher

    def __str__(self):
        return f'{self.title} {self.teacher}'    

class DBLesson(Lesson):
    def __init__(self, id, title, teacher):
        self.id = id
        self.title=title
        self.teacher=teacher