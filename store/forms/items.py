from flask_wtf import FlaskForm
from wtforms import SubmitField,  TextAreaField, FileField
from wtforms.validators import DataRequired


class ItemForm(FlaskForm):
    value = TextAreaField("Содержание товара", validators=[DataRequired()])
    file = FileField("Содержание товара: файл (опционально)")
    submit = SubmitField()

    def __init__(self, *args, mode: str = "a", **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.submit.label.text = "Создать" if mode == "a" else "Изменить"
