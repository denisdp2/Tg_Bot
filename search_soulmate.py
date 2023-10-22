import json
import random
from project_data.__all_models import users


def find_soulmate(current_id, current_city, current_age, current_partner, db_sess):
    spisok_soulmates = []
    for user in db_sess.query(users.User).all():
        if not user.age or not user.to_search:
            continue
        soulmate_city = user.city
        soulmate_age = user.age
        soulmate_sex = user.sex
        soulmate_id = user.id
        if int(soulmate_age) + 2 >= int(current_age) >= int(soulmate_age) - 1 \
                and soulmate_city == current_city and \
                (soulmate_sex == current_partner or current_partner == 'Н') and \
                current_id != soulmate_id:
            spisok_soulmates.append(user.get_info(db_sess))
    if spisok_soulmates:
        return spisok_soulmates
    else:
        return []
