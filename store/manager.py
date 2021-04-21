from flask import render_template, Blueprint, make_response, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.utils import redirect

from base.db_session import create_session
from base.users import User
from store.forms.users import RegisterForm, LoginForm

store_blueprint = Blueprint('store', __name__, template_folder='templates')


@store_blueprint.errorhandler(403)
def not_allowed():
    return make_response(jsonify({'error': 'Not Allowed'}), 403)


@store_blueprint.errorhandler(404)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


@store_blueprint.route('/')
def index():
    data = {
        "title": "Главная",
        "current_user": current_user
    }
    return render_template("store/index.html", **data)


@store_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    local_db_session = create_session()
    form = RegisterForm()

    data = {
        "title": "Регистрация",
        "current_user": current_user,
        "form": form
    }

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            data["message"] = "Пароли не совпадают"
        elif local_db_session.query(User).filter(User.login == form.login.data).first():
            data["message"] = "Пользователь с таким именем уже есть"
        elif local_db_session.query(User).filter(User.login == form.email.data).first():
            data["message"] = "Пользователь с таким e-mail уже есть"
        else:
            user = User(login=form.login.data, email=form.email.data)
            user.set_password(form.password.data)
            local_db_session.add(user)
            local_db_session.commit()
            user = local_db_session.query(User).filter_by(login=user.login).first()
            login_user(user, remember=False)
            return redirect('/')
    return render_template("store/register.html", **data)


@store_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    local_db_session = create_session()
    form = LoginForm()

    params = {
        "title": "Авторизация",
        "current_user": current_user,
        "form": form
    }

    if form.validate_on_submit():
        user = local_db_session.query(User).filter_by(login=form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        params["message"] = "Неправильный логин или пароль",
    return render_template('store/login.html', **params)


@store_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def admin_required(func):
    def function_decorator(*args, **kwargs):
        if current_user.is_admin:
            return func(*args, **kwargs)
        else:
            return not_allowed()
    return function_decorator


@store_blueprint.route("/admin/products/add", methods=['GET', 'POST'])
@admin_required
@login_required
def add_product():
    return jsonify({"nice": True})
