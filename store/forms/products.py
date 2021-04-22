from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed


class ProductForm(FlaskForm):
    picture = FileField(label="Логотип товара (PNG)", validators=[DataRequired()])
    product_name = StringField("Название товара", validators=[FileRequired(), FileAllowed(['png'], 'Images only!')])
    price = IntegerField("Цена (в рублях)", validators=[DataRequired()])
    product_desc = TextAreaField("Описание товара")
    alert = TextAreaField("Инструкция", validators=[DataRequired()])
    submit = SubmitField('Создать')
