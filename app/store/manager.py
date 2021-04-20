import flask

from app.store import db_session
from app.store.models import *

store_blueprint = flask.Blueprint(
    'store',
    __name__,
    template_folder='templates'
)


@store_blueprint.route('/')
def index():
    data = {
        "title": "Главная"
    }
    return flask.render_template("store/index.html", **data)
