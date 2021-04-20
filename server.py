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
    local_db_session = create_session()
    return local_db_session.query(User).get(user_id)


if __name__ == '__main__':
    db_global_init("db/vault.db")
    app.register_blueprint(store_blueprint)
    app.run(debug=True)
