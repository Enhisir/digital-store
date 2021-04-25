from sqlalchemy_serializer import SerializerMixin

from base.db_session import SqlAlchemyBase
from sqlalchemy import orm, Column, Integer, String, ForeignKey


class Item(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    value = Column(String, nullable=False)
    binary_value = Column(String, nullable=True)
    product = orm.relation("Product")
