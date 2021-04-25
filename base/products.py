import datetime
from sqlalchemy_serializer import SerializerMixin
from base.db_session import SqlAlchemyBase
from sqlalchemy import orm, Column, Integer, String, DateTime, BLOB


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    picture = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    product_desc = Column(String, nullable=True)
    alert = Column(String, nullable=False)
    amount = Column(String, default=0)
    purchases = Column(Integer, default=0)
    creation_date = Column(DateTime, default=datetime.datetime.now)
    items = orm.relation("Item", back_populates="product")
