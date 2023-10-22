import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from .like import Like


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    sex = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    partner = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    to_search = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    insta_link = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String)
    sent_like = orm.relation("Like", primaryjoin='User.id==Like.liker_id')
    received_like = orm.relation("Like", primaryjoin='User.id==Like.partner_id')

    def to_bd(self, dict_inf, db_sess):
        user = db_sess.query(User).filter(User.id == self.id).first()
        user.name = dict_inf['name']
        user.age = dict_inf['age']
        user.sex = dict_inf['sex']
        user.about = dict_inf['about']
        user.partner = dict_inf['partner']
        user.city = dict_inf['city']
        user.photo = dict_inf['photo']
        db_sess.commit()

    def for_search(self):
        return {"age": 0, "city": 0, "sex": 0}

    def get_info(self, db_sess):
        user = db_sess.query(User).filter(User.id == self.id).first()
        return {"age": user.age, "name": user.name, "about": user.about, "partner": user.partner,
                "city": user.city, "insta_link": user.insta_link, "id": user.id,
                "photo": user.photo, "username": user.username}

    def set_like(self, liker_id, db_sess):
        user = db_sess.query(User).filter(User.id == self.id).first()
        like = Like()
        if like.is_like(liker_id, user.id, db_sess):
            like.add_like(liker_id, user.id, db_sess)

    def set_insta(self, db_sess, link):
        user = db_sess.query(User).filter(User.id == self.id).first()
        user.insta_link = link
        db_sess.commit()

    def change_status(self, db_sess):
        user = db_sess.query(User).filter(User.id == self.id).first()
        if user.to_search:
            user.to_search = False
        else:
            user.to_search = True
        db_sess.commit()
