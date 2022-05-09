import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Person(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'person'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    like = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    atribut_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("attribute.id"))
    atribut = orm.relation('Attribute')