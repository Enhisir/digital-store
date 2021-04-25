from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed


class AddProductForm(FlaskForm):
    picture = FileField(label="Логотип товара (PNG)",
                        validators=[FileRequired(), FileAllowed(['png', "jpg", "webp"], 'Images only!')])
    product_name = StringField("Название товара", validators=[DataRequired()])
    price = IntegerField("Цена (в рублях)", validators=[DataRequired()])
    product_desc = TextAreaField("Описание товара")
    alert = TextAreaField("Инструкция", validators=[DataRequired()])
    submit = SubmitField('Создать')


class EditProductForm(FlaskForm):
    picture = FileField(label="Логотип товара (PNG)",
                        validators=[FileAllowed(['png', "jpg", "webp"], 'Images only!')])
    price = IntegerField("Цена (в рублях)", validators=[DataRequired()])
    product_desc = TextAreaField("Описание товара")
    alert = TextAreaField("Инструкция", validators=[DataRequired()])
    submit = SubmitField('Редактировать')
