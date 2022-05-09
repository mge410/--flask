from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, FileField
from wtforms.validators import DataRequired


class Persformatrib(FlaskForm):
    name = StringField('Имя персонажа', validators=[DataRequired()])
    submit = SubmitField('Выбрать')