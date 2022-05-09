from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, FileField
from wtforms.validators import DataRequired


class Persform(FlaskForm):
    name = StringField('Имя персонажа', validators=[DataRequired()])
    content = TextAreaField("Расскажите про него")
    atribut = StringField("Атрибуты персонажа")
    is_private = BooleanField("Закрытый профиль персонажа")
    submit = SubmitField('Готово')