import datetime
from sqlalchemy_serializer import SerializerMixin
from base.db_session import SqlAlchemyBase
from sqlalchemy import orm, Column, Integer, String, DateTime


class Product(SqlAlchemyBase, SerializerMixin):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    product_desc = Column(String, nullable=True)
    alert = Column(String, nullable=True)
    amount = Column(String, nullable=True)
    purchases = Column(Integer, default=0)
    creation_date = Column(DateTime, default=datetime.datetime.now)


class ProductKey(Product):
    __tablename__ = "product_keys"

    keys = orm.relation("Key", back_populates="product")