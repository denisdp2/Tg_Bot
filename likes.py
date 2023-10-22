from project_data import users
from project_data.like import Like


def get_likes(id_partner, db_sess):
    list_likes = []
    for like in db_sess.query(Like).filter(Like.partner_id == id_partner).all():
        user = db_sess.query(users.User).filter(users.User.id == like.liker_id).first()
        list_likes.append(user.get_info(db_sess))
    return list_likes
