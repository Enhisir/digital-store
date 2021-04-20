from sqlalchemy_serializer import SerializerMixin

from base.db_session import SqlAlchemyBase
from sqlalchemy import orm, Column, Integer, String, ForeignKey


class Key(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("product_keys.id"))
    value = Column(String, nullable=False)
    product = orm.relation("ProductKey")


# class Account(SqlAlchemyBase, SerializerMixin):
#     __tablename__ = "accounts"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     product_id = Column(Integer,
#                                    ForeignKey("products.id"))
#     login = Column(String, nullable=False)
#     password = Column(String, nullable=False)
#     additional = Column(String, nullable=True)
