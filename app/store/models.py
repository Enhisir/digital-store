from sqlalchemy_serializer import SerializerMixin

from app.store.db_session import SqlAlchemyBase
from sqlalchemy import orm, Column, Integer, String, ForeignKey


class Product(SqlAlchemyBase, SerializerMixin):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    product_desc = Column(String, nullable=True)
    alert = Column(String, nullable=True)
    amount = Column(String, nullable=True)
    purchases = Column(Integer, default=0)


class ProductKey(Product):
    __tablename__ = "product_keys"

    keys = orm.relation("Key", back_populates="product_keys")


class Item(SqlAlchemyBase, SerializerMixin):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))


class Key(Item):
    __tablename__ = "keys"

    value = Column(String, nullable=False)
    product = orm.relation("Product", back_populates="keys")


# class Account(SqlAlchemyBase, SerializerMixin):
#     __tablename__ = "accounts"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     product_id = Column(Integer,
#                                    ForeignKey("products.id"))
#     login = Column(String, nullable=False)
#     password = Column(String, nullable=False)
#     additional = Column(String, nullable=True)
