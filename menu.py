from likes import get_likes
from project_data import db_session
from project_data.__all_models import users, like
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup
from search_soulmate import find_soulmate


def menu(update, context):
    if not update.message.text:
        update.message.reply_text("Нажми на кнопку:)")
        return 10
    db_sess = db_session.create_session()
    user = db_sess.query(users.User).filter(users.User.id == update.message.from_user.id).first()
    if not user.to_search:
        user.change_status(db_sess)
    profile = user.get_info(db_sess)
    update.message.reply_text("Твоя анкета:")
    context.bot.send_photo(update.message.chat_id, open(profile['photo'], "rb"))
    text_reply = f"{profile['city']}, " \
                 f"{profile['name']}, {profile['age']}\n" \
                 f"{profile['about']}"

    if user.insta_link:
        update.message.reply_text(text_reply + "\n" + f"inst: {user.insta_link}",
                                  reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text(text_reply, reply_markup=ReplyKeyboardRemove())

    reply_keyboard = [["Смотреть анкеты", "Редактировать мою анкету"],
                      ["Остановить поиск", "Привязка инсты", "Оценившие"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text("Выбери действие", reply_markup=markup)
    context.user_data["summ"] = 0  # кол-во просмотренных анкет
    context.user_data["likes_saw"] = 0
    return 10


def menu_handler(update, context):
    text = update.message.text
    db_sess = db_session.create_session()
    user = db_sess.query(users.User).filter(users.User.id == update.message.from_user.id).first()
    if text == "Смотреть анкеты" or \
            update.message.text == "❤" or update.message.text == "👎":
        soulmate = (find_soulmate(user.id, user.city, user.age,
                                  user.partner, db_sess))
        if update.message.text == "❤" and soulmate:
            id = soulmate[context.user_data['summ'] % len(soulmate) - 1]["id"]
            liked_person = db_sess.query(users.User).filter(users.User.id == id).first()
            liked_person.set_like(user.id, db_sess)
        if not soulmate:
            reply_keyboard = [["⬅"]]
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
            update.message.reply_text("Для тебя никого не нашлось :C",
                                      reply_markup=markup)
            return 9
        soulmate = soulmate[context.user_data['summ'] % len(soulmate)]
        reply_keyboard = [["❤", "👎"], ["💤"]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        text_reply = f"{soulmate['city'].encode('utf-8').decode('utf-8')}," \
                     f" {soulmate['name'].encode('utf-8').decode('utf-8')}," \
                     f" {soulmate['age']}\n" \
                     f"{soulmate['about'].encode('utf-8').decode('utf-8')}"
        context.bot.send_photo(update.message.chat_id, open(soulmate['photo'], "rb"))
        if soulmate['insta_link']:
            update.message.reply_text(text_reply + "\n"
                                      + f"inst: {soulmate['insta_link']}", reply_markup=markup)
        else:
            update.message.reply_text(text_reply,
                                      reply_markup=markup
                                      )
        context.user_data["summ"] += 1
        return 10
    elif text == "💤":
        reply_keyboard = [["⬅"]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("Остановлен просмотр анкет", reply_markup=markup)
        return 9
    elif text == "Редактировать мою анкету":
        reply_keyboard = [[user.age]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("Твой возраст", reply_markup=markup)
        context.user_data['editing'] = True
        return 2
    elif text == "Привязка инсты":
        update.message.reply_text("inst:", reply_markup=ReplyKeyboardRemove())
        return 11
    elif text == "Остановить поиск":
        user.change_status(db_sess)
        reply_keyboard = [["Вернуться.."]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("Ваша анкет больше не отображается в поиске.\n"
                                  "SEE YOU SPACE COWBOY....", reply_markup=markup)
        return 9
    elif text == "Оценившие" or text == "следующая":
        profile = get_likes(user.id, db_sess)
        if not profile:
            reply_keyboard = [["⬅"]]
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
            update.message.reply_text("Пока что тебя никто не оценил :с", reply_markup=markup)
            return 9
        if profile:
            profile = profile[context.user_data["likes_saw"] % len(profile)]
            text = f"{profile['city'].encode('utf-8').decode('utf-8')}," \
                   f" {profile['name'].encode('utf-8').decode('utf-8')}," \
                   f" {profile['age']}\n @{profile['username']}\n" \
                   f"{profile['about'].encode('utf-8').decode('utf-8')}"
            if profile["insta_link"]:
                text += f"\ninst:{profile['insta_link']}"
            reply_keyboard = [["следующая", "вернуться назад"]]
            context.bot.send_photo(update.message.chat_id, open(profile['photo'], "rb"))
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

            update.message.reply_text(text, reply_markup=markup)
            context.user_data["likes_saw"] += 1
        return 10
    elif text == "вернуться назад":
        reply_keyboard = [["⬅"]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("Вернуться", reply_markup=markup)
        return 9
    else:
        update.message.reply_text("Выбери один из вариантов")
