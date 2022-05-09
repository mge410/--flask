import datetime
import os
import shutil
import random

from flask import Flask, render_template, request, session, make_response, jsonify
from werkzeug.exceptions import abort
from werkzeug.utils import redirect, secure_filename

from data import db_session
from data.users import User
from data.personage import Person
from data.attribute import Attribute
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.addperson import Persform
from forms.atributa import Addatribyte
from forms.pers_atribut import Persformatrib
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import api

# Запускаем приложение
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# Лайкаем раз в неделю =)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=7
)
login_manager = LoginManager()
login_manager.init_app(app)

# Пути к картинкам
UPLOAD_FOLDER = 'static/img_pers/'
UPLOAD_FOLDER_ATRIBYTE = 'static/img_atrib/'


with open('anekdoty.txt', 'r', encoding='utf-8') as f:
    text = f.read().split("* * *")


# Обработка 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# Main
def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(api.blueprint)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


# Функция для Логирования
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Главная страница
@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        form = db_sess.query(Person).filter(
            (Person.user == current_user) | (Person.is_private != True)).order_by(Person.like.desc()).all()
    else:
        form = db_sess.query(Person).filter(Person.is_private != True).order_by(Person.like.desc()).all()
    return render_template("index.html", form=form)


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


# Логируемся
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# Выходим
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# Добавляем персонажа
@app.route('/addperson',  methods=['GET', 'POST'])
@login_required
def add_pers():
    form = Persform()
    if form.validate_on_submit():
        f = request.files['file']
        if f:
            if os.path.exists(f"{UPLOAD_FOLDER}{f.filename}"):
                os.remove(f"{UPLOAD_FOLDER}{f.filename}")
        f.save(secure_filename(f.filename))
        shutil.move(f.filename, UPLOAD_FOLDER)
        person = Person()
        person.name = form.name.data
        person.content = form.content.data
        person.is_private = form.is_private.data
        person.img = f"{UPLOAD_FOLDER}{f.filename}"
        current_user.persone.append(person)
        db_sess = db_session.create_session()
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('addperson.html',
                           form=form, get="Добавление персонажа")


# Удаляем персонажа
@app.route('/pers_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def pers_delete(id):
    db_sess = db_session.create_session()
    pers = db_sess.query(Person).filter(Person.id == id,
                                      Person.user == current_user
                                      ).first()
    if pers:
        db_sess.delete(pers)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


# Лайкаем раз в неделю =)
@app.route("/like/<int:id>")
def session_like(id):
    visits_count = session.get('visits_count', 0)
    db_sess = db_session.create_session()
    pers = db_sess.query(Person).filter(Person.id == id).first()
    if visits_count == 0:
        pers.like = pers.like + 1
        db_sess.commit()
        session['visits_count'] = visits_count + 1
        return redirect('/')
    else:
        return redirect('/')


# Меняем персонажа
@app.route('/pers_rec/<int:id>', methods=['GET', 'POST'])
@login_required
def pers_rec(id):
    form = Persform()
    if request.method == "GET":
        db_sess = db_session.create_session()
        pers = db_sess.query(Person).filter(Person.id == id, Person.user == current_user).first()
        if pers:
            form.name.data = pers.name
            form.content.data = pers.content
            form.is_private.data = pers.is_private
        else:
            abort(404)
        print(pers.img)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        pers = db_sess.query(Person).filter(Person.id == id,
                                          Person.user == current_user
                                          ).first()
        if pers:
            f = request.files['file']
            if f:
                if os.path.exists(f"{UPLOAD_FOLDER}{f.filename}"):
                    os.remove(f"{UPLOAD_FOLDER}{f.filename}")
                    if os.path.exists(pers.img):
                        os.remove(pers.img)
                f.save(secure_filename(f.filename))
                shutil.move(f.filename, UPLOAD_FOLDER)
            pers.name = form.name.data
            pers.content = form.content.data
            pers.is_private = form.is_private.data
            pers.img = f"{UPLOAD_FOLDER}{f.filename}"
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addperson.html',
                           title='Редактирование персонажа',
                           form=form, get="Изменение персонажа")


# Рандомный анекдот
@app.route("/randon")
def anecdot():
    return text[random.randint(0, len(text) - 1)]


# Главная страница артибутов
@app.route("/atribyte")
def index_atribyt():
    db_sess = db_session.create_session()
    form = db_sess.query(Attribute).all()
    return render_template("index_atribyte.html", form=form)


# Добавляем артибуты
@app.route('/addatribyte',  methods=['GET', 'POST'])
@login_required
def add_atribute():
    form = Addatribyte()
    if form.validate_on_submit():
        f = request.files['file']
        f.save(secure_filename(f.filename))
        shutil.move(f.filename, UPLOAD_FOLDER_ATRIBYTE)
        atribute = Attribute()
        atribute.name = form.name.data
        atribute.description = form.description.data
        atribute.img = f"{UPLOAD_FOLDER_ATRIBYTE}{f.filename}"
        db_sess = db_session.create_session()
        db_sess.add(atribute)
        db_sess.commit()
        return redirect('/atribyte')
    return render_template('add_atribut.html',
                           form=form, get="Добавление атрибута")


# Выбераем артибуты персонажам
@app.route("/choice_of_attribute/<int:id>", methods=['GET', 'POST'])
@login_required
def choice_of_attribute(id):
    form = Persformatrib()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        pers = db_sess.query(Person).filter(Person.name == form.name.data).first()
        atrib = db_sess.query(Attribute).filter(Attribute.id == id).first()
        atrib.persone.append(pers)
        db_sess.commit()
    return render_template('add_pers_atrib.html',
                           form=form, get="Добавление атрибута")


# Пуск =)
if __name__ == '__main__':
    main()