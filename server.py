#!/usr/bin/env python
from flask import Flask
from flask_login import LoginManager

from base.users import User
from store.manager import store_blueprint
from base.db_session import global_init as db_global_init, create_session

app = Flask(__name__)
app.config.from_object("config.ProductionConfig")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_session = create_session()
    return db_session.query(User).get(user_id)


if __name__ == '__main__':
    db_global_init("db/vault.db")
    admin = User(login="admin", email="enhisir@yandex.ru")
    admin.set_password("<j;t_[hfyb_vjq_cfqn!")
    admin.is_admin = True
    db_session = create_session()
    print(db_session.query(User).filter_by(login="admin").first())
    if db_session.query(User).filter_by(login="admin").first() is None:
        db_session.add(admin)
        db_session.commit()
    app.register_blueprint(store_blueprint)
    app.run(debug=True)
