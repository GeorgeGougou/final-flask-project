from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, NumberRange, ReadOnly

#ΔΗΜΙΟΥΡΓΙΑ ΦΟΡΜΑΣ ΓΙΑ ΑΠΟΘΗΚΕΥΣΗ ΤΩΝ ΣΤΟΙΧΕΙΩΝ ΕΝΟΣ ΜΑΘΗΤΗ ΑΠΟ ΤΟΝ ΧΡΗΣΤΗ
class StudentForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    birth_date = DateField('Birth Date', format = "%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField('Submit')

#ΔΗΜΙΟΥΡΓΙΑ ΤΗΣ ΦΟΡΜΑΣ ΓΙΑ ΑΠΟΘΗΚΕΥΣΗ ΤΩΝ ΣΤΟΙΧΕΙΩΝ ΕΝΟΣ ΜΑΘΗΜΑΤΟΣ
class LessonForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    teacher = SelectField('Teacher', choices=['Mr.Smith', 'Mrs.Brown', 'Mr.Miller', 'Mr.Wilson', 'Mrs.Jonhson'])
    submit = SubmitField('Submit')

#ΔΗΜΙΟΥΡΓΙΑ ΤΗΣ ΦΟΡΜΑΣ ΓΙΑ ΑΠΟΘΗΚΕΥΣΗ ΤΩΝ ΣΤΟΙΧΕΙΩΝ ΕΝΟΣ ΒΑΘΜΟΥ
class GradeForm(FlaskForm):
    student_id = SelectField('Student ID',choices=[],coerce=int,validators=[DataRequired()])
    lesson_id = SelectField('Lesson Id',choices=[],coerce=int,validators=[DataRequired()])
    grade = DecimalField('Grade', validators=[DataRequired(), NumberRange(min=0, max=10)])
    submit = SubmitField('Submit')

#ΔΗΜΙΟΥΡΓΙΑ ΤΗΣ ΦΟΡΜΑΣ ΓΙΑ ΤΗΝ ΕΠΕΞΕΡΓΑΣΙΑ ΕΝΟΣ ΒΑΘΜΟΥ, ΧΩΡΙΣ ΝΑ ΕΠΗΡΕΑΖΕΤΑΙ ΤΟ Student Id ΚΑΙ ΤΟ Lesson Id
class EditGradeFrom(FlaskForm):
    student_id = IntegerField('Student ID',validators=[DataRequired(),ReadOnly()])
    lesson_id = IntegerField('Lesson Id',validators=[DataRequired(),ReadOnly()])
    grade = DecimalField('Grade', validators=[DataRequired(), NumberRange(min=0, max=10)])
    submit = SubmitField('Submit')