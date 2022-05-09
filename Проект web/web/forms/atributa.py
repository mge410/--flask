from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, FileField
from wtforms.validators import DataRequired


class Addatribyte(FlaskForm):
    name = StringField('Имя атрибута', validators=[DataRequired()])
    description = TextAreaField("Расскажите про него")
    submit = SubmitField('Готово')