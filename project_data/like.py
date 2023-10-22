import datetime
import sqlalchemy
from sqlalchemy import orm

from . import db_session
from .db_session import SqlAlchemyBase


class Like(SqlAlchemyBase):
    __tablename__ = 'likes'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    liker_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("users.id"))

    partner_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    def add_like(self, liker_id, partner_id, db_sess):
        like = Like()
        like.liker_id = liker_id
        like.partner_id = partner_id
        db_sess.add(like)
        db_sess.commit()

    def is_like(self, liker_id, partner_id, db_sess):
        for like in db_sess.query(Like).all():
            if like.liker_id and like.liker_id == liker_id and like.partner_id == partner_id:
                return False
        return True
