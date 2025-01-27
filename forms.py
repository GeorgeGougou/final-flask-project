from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email

class StudentForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    birth_date = DateField('Birth Date', format = "%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField('Submit')

class LessonForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    teacher = SelectField('Teacher', choices=['Smith', 'Brown', 'Miller', 'Wilson', 'Jonhson'])
    submit = SubmitField('Submit')

