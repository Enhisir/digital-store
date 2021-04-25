import os

from flask import render_template, Blueprint, make_response, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.utils import redirect, secure_filename

from config import Config
from base.db_session import create_session
from base.items import Item
from base.products import Product
from base.users import User
from store.forms.items import ItemForm
from store.forms.products import EditProductForm, AddProductForm
from store.forms.users import RegisterForm, LoginForm
store_blueprint = Blueprint('store', __name__, template_folder='templates', static_folder="static")


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
        "current_user": current_user,
        "products": create_session().query(Product).all()
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
            data["message"] = {
                "type": "alert alert-danger",
                "value": "Пароли не совпадают"
            }
        elif local_db_session.query(User).filter(User.login == form.login.data).first():
            data["message"] = {
                "type": None,
                "value": "Пользователь с таким именем уже есть"
            }
        elif local_db_session.query(User).filter(User.login == form.email.data).first():
            data["message"] = {
                "type": "alert alert-danger",
                "value": "Пользователь с таким e-mail уже есть"
            }
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
        params["message"] = {
            "type": "alert alert-danger",
            "value": "Неправильный логин или пароль"
        }
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
            return redirect("/")
    return function_decorator


@store_blueprint.route("/products/add", methods=['GET', 'POST'], endpoint="add_product")
@admin_required
@login_required
def add_product():
    db_session = create_session()
    form = AddProductForm()

    data = {
        "title": "Новый товар",
        "current_user": current_user,
        "form": form
    }
    if form.validate_on_submit():
        if form.picture.data is None:
            data["message"] = {
                "type": "alert alert-danger",
                "value": "Нет картинки"
            }
        else:
            path = os.path.join(Config.PICTURE_UPLOAD_FOLDER, secure_filename(form.picture.data.filename))
            form.picture.data.save(path)
            product = Product(
                picture=form.picture.data.filename,
                product_name=form.product_name.data,
                price=form.price.data,
                product_desc=form.product_desc.data,
                alert=form.alert.data
            )
            db_session.add(product)
            db_session.commit()
            data["message"] = {
                "type": "alert alert-info",
                "value": "Новый товар успешно создан!"
            }
    return render_template("store/new_product.html", **data)

    db_session = create_session()
    form = ProductForm()

    data = {
        "title": "Новый товар",
        "current_user": current_user,
        "form": form
    }
    if form.validate_on_submit():
        if form.picture.data is None:
            data["message"] = {
                "type": "alert alert-danger",
                "value": "Нет картинки"
            }
        else:
            path = os.path.join(Config.PICTURE_UPLOAD_FOLDER, secure_filename(form.picture.data.filename))
            form.picture.data.save(path)
            product = Product(
                picture=form.picture.data.filename,
                product_name=form.product_name.data,
                price=form.price.data,
                product_desc=form.product_desc.data,
                alert=form.alert.data
            )
            db_session.add(product)
            db_session.commit()
            data["message"] = {
                 "type": "alert alert-info",
                 "value": "Новый товар создан!"
            }
            data["product"] = product
            data.pop("form")
            return render_template("store/show_product.html", **data)
    return render_template("store/new_product.html", **data)


@store_blueprint.route("/products/edit/<int:pid>", methods=['GET', 'POST'], endpoint="edit_product")
@admin_required
@login_required
def edit_product(pid: int):
    db_session = create_session()
    form = EditProductForm()
    product = db_session.query(Product).get(pid)
    if product is None:
        return not_found()
    data = {
        "title": "Изменить товар",
        "current_user": current_user,
        "form": form,
        "product": product
    }
    if form.validate_on_submit():
        if form.picture.data:
            path = os.path.join(Config.PICTURE_UPLOAD_FOLDER, secure_filename(form.picture.data.filename))
            form.picture.data.save(path)
            product.picture = form.picture.data.filename
        product.price = form.price.data
        product.product_desc = form.product_desc.data
        product.alert = form.alert.data
        db_session.commit()
        data["message"] = {
            "type": "alert alert-info",
            "value": "Товар успешно изменен!"
        }
        return render_template("store/edit_product.html", **data)
    else:
        form.price.data = product.price
        form.product_desc.data = product.product_desc
        form.alert.data = product.alert
        return render_template("store/edit_product.html", **data)


@store_blueprint.route("/products/delete/<int:pid>", endpoint="delete_product")
@admin_required
@login_required
def delete_product(pid: int):
    db_session = create_session()
    product = db_session.query(Product).get(pid)
    if product is None:
        return not_found()
    db_session.delete(product)
    db_session.commit()
    return redirect("/")


@store_blueprint.route("/products/<int:pid>", endpoint="show_product")
def show_product(pid: int):
    db_session = create_session()
    product = db_session.query(Product).get(pid)
    if product is None:
        return not_found()
    data = {
        "title": product.product_name,
        "current_user": current_user,
        "product": product
    }
    return render_template("store/show_product.html", **data)


@store_blueprint.route("/products/<int:pid>/items/add", methods=['GET', 'POST'], endpoint="add_item")
@admin_required
@login_required
def add_item(pid: int):
    db_session = create_session()
    product = db_session.query(Product).get(pid)
    if product is None:
        return not_found()
    form = ItemForm()
    data = {
        "title": "Новый экземпляр",
        "current_user": current_user,
        "form": form,
        "product": product
    }
    if form.validate_on_submit():
        item = Item(product_id=product.id,
                    value=form.value.data)
        if form.file.data:
            path = os.path.join(Config.ITEM_UPLOAD_FOLDER, secure_filename(form.file.data.filename))
            form.file.data.save(path)
            item.binary_value = form.file.data.filename
        db_session.add(item)
        item = db_session.query(Item).filter_by(value=form.value.data).first()
        item.product.amount += 1
        db_session.commit()
        data["message"] = {
            "type": "alert alert-info",
            "value": "Новый экземпляр продукта создан!"
        }
        data.pop("form")
        return render_template("store/show_product.html", **data)
    return render_template("store/new_item.html", **data)


@store_blueprint.route("/products/<int:pid>/items/<int:iid>/edit", methods=['GET', 'POST'], endpoint="edit_item")
@admin_required
@login_required
def edit_item(pid: int, iid: int):
    db_session = create_session()
    product = db_session.query(Product).get(pid)
    if product is None:
        return not_found()
    item = db_session.query(Item).get(iid)
    if item is None:
        return not_found()
    form = ItemForm(mode="e")
    data = {
        "title": "Новый экземпляр",
        "current_user": current_user,
        "form": form,
        "product": product,
        "item": item
    }
    if form.validate_on_submit():
        if form.file.data:
            path = os.path.join(Config.ITEM_UPLOAD_FOLDER, secure_filename(form.file.data.filename))
            form.file.data.save(path)
            item.binary_value = form.file.data.filename
        item.value = form.value.data
        db_session.commit()
        data["message"] = {
            "type": "alert alert-info",
            "value": "Экземпляр продукта изменен!"
        }
        data.pop("form")
        return render_template("store/show_product.html", **data)
    form.value.data = item.value
    return render_template("store/edit_item.html", **data)


@store_blueprint.route("/products/<int:pid>/items/<int:iid>/delete", endpoint="delete_item")
@admin_required
@login_required
def delete_item(pid: int, iid: int):
    db_session = create_session()
    product = db_session.query(Product).get(pid)
    if product is None:
        return not_found()
    item = db_session.query(Item).get(iid)
    if item is None:
        return not_found()
    item = db_session.query(Item).get(iid)
    db_session.delete(item)
    db_session.commit()
    return redirect(f"/products/{product.id}")
