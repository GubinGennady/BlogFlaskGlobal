from flask import Flask, render_template, request, flash
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import hash
from forms import LoginForm

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User, Post


@app.route('/')
def container():
    return render_template('index.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        login = request.form.get('login')
        password = hash.hash_password(request.form.get('password'))
        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()
    return render_template('registretion.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    form = LoginForm()
    error = ''
    print(form.data)
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
        else:
            error += 'Login error'
    return render_template('auth.html', form=form, error=error)

    # flash("Invalid username/password", 'error')
    # return redirect(url_for('login'))
    # return render_template('auth.html', form=form)


    # message = ''
    # if request.method == 'POST':
    #     print(request.form)
    #     login = request.form.get('login')
    #     password = request.form.get('password')
    #
    #     if login == 'root' and password == 'pass':
    #         message = "Правильное имя пользователя и пароль"
    #     else:
    #         message = "Неверное имя пользователя или пароль"
    # return render_template('auth.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
