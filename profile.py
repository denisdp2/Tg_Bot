import sqlalchemy.exc
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from project_data import users, db_session


def greeting(update, context):
    if not update.message.text:
        update.message.reply_text("Нажмите на кнопку:)")
        return 1
    context.user_data['editing'] = False  # для проверки редактирует ли человек анкету
    try:
        user = users.User()
        user.id = update.message.from_user.id
        user.username = update.message.from_user.username
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        update.message.reply_text("Давай создадим тебе анкету\n"
                                  "Твой возраст", reply_markup=ReplyKeyboardRemove())
        return 2
    except sqlalchemy.exc.IntegrityError:
        reply_keyboard = [["начать"]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("Тебя мы уже здесь видели!",
                                  reply_markup=markup)
        return 9


def age_add(update, context):
    if not update.message.text:
        update.message.reply_text("Введите корректный возраст(только цифры)")
        return 2
    if update.message.text.isnumeric():
        context.user_data["age"] = int(update.message.text)
        if context.user_data['editing']:
            db_sess = db_session.create_session()
            user = db_sess.query(users.User).filter(users.User.id == update.message.from_user.id).first()
            reply_keyboard = [[user.city]]
            markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
            update.message.reply_text("Твой город", reply_markup=markup)
            return 3
        update.message.reply_text("Твой город", reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text("Введите корректный возраст(только цифры)",
                                  reply_markup=ReplyKeyboardRemove())
        return 2
    return 3


def city_add(update, context):
    if not update.message.text:
        update.message.reply_text("Введите город корректно")
        return 3
    if context.user_data['editing']:
        context.user_data['city'] = update.message.text
        reply_keyboard = [['Твоё прошлое фото']]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("Твоё фото", reply_markup=markup)
        return 4
    if update.message.text.isnumeric():
        update.message.reply_text("Введите корректный город(только буквы)",
                                  reply_markup=ReplyKeyboardRemove())
        return 3
    else:
        context.user_data["city"] = update.message.text.lower().capitalize()
        update.message.reply_text("Твоё фото(не файлом)")
        return 4


def photo_add(update, context):
    if not update.message.photo and update.message.text != 'Твоё прошлое фото':
        update.message.reply_text('Отправьте фото(не файлом)')
        return 4
    if context.user_data['editing']:
        db_sess = db_session.create_session()
        user = db_sess.query(users.User).filter(users.User.id == update.message.from_user.id).first()
        if update.message.text == 'Твоё прошлое фото':
            context.user_data["photo"] = user.photo
        else:
            try:
                context.user_data["photo"] = update.message.photo[2].get_file().download(
                    custom_path=f'images/{update.message.from_user.id}.jpg')
            except IndexError:
                try:
                    context.user_data["photo"] = update.message.photo[1].get_file().download(
                        custom_path=f'images/{update.message.from_user.id}.jpg')
                except IndexError:
                    context.user_data["photo"] = update.message.photo[0].get_file().download(
                        custom_path=f'images/{update.message.from_user.id}.jpg')

        reply_keyboard = [[user.name]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("Твоё имя", reply_markup=markup)
        return 5
    elif update.message.photo:
        try:
            context.user_data["photo"] = update.message.photo[2].get_file().download(
                custom_path=f'images/{update.message.from_user.id}.jpg')
        except IndexError:
            try:
                context.user_data["photo"] = update.message.photo[1].get_file().download(
                    custom_path=f'images/{update.message.from_user.id}.jpg')
            except IndexError:
                context.user_data["photo"] = update.message.photo[0].get_file().download(
                    custom_path=f'images/{update.message.from_user.id}.jpg')
        update.message.reply_text("Твоё имя")
        return 5
    else:
        update.message.reply_text('Отправьте фото(не файлом)')
        return 4


def name_add(update, context):
    if not update.message.text:
        update.message.reply_text("Введите имя корректно")
        return 5
    reply_keyboard = [["Я парень", "Я девушка"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True,
                                 resize_keyboard=True)
    update.message.reply_text("Твой пол.\n"
                              "Выбери вариант ответа.", reply_markup=markup)
    context.user_data["name"] = update.message.text
    return 6


def sex_add(update, context):
    if not update.message.text:
        update.message.reply_text("Выбери один из вариантов")
        return 6
    if update.message.text == "Я парень":
        context.user_data["sex"] = "М"
    elif update.message.text == "Я девушка":
        context.user_data["sex"] = "Ж"
    else:
        update.message.reply_text("Выбери один из вариантов")
        return 6
    if context.user_data['editing']:
        reply_keyboard = [["Оставить прошлое описание"]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        update.message.reply_text("Расскажи о себе", reply_markup=markup)
        return 7
    update.message.reply_text("Расскажи о себе",
                              reply_markup=ReplyKeyboardRemove())
    return 7


def about_add(update, context):
    if not update.message.text:
        update.message.reply_text("Расскажи о себе что-нибудь интересное")
        return 7
    if context.user_data['editing'] and update.message.text == "Оставить прошлое описание":
        db_sess = db_session.create_session()
        user = db_sess.query(users.User).filter(users.User.id == update.message.from_user.id).first()
        context.user_data['about'] = user.about
    else:
        context.user_data["about"] = update.message.text
    reply_keyboard = [["Парни", "Девушки", "Все"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text("Кто тебе интересен?", reply_markup=markup)
    return 8


def type_partner_add(update, context):
    if not update.message.text:
        update.message.reply_text("Выбери один из вариантов")
        return 8
    if update.message.text == "Парни":
        context.user_data["partner"] = "М"
    elif update.message.text == "Девушки":
        context.user_data["partner"] = "Ж"
    elif update.message.text == "Все":
        context.user_data["partner"] = "Н"
    else:
        update.message.reply_text("Выбери один из вариантов")
        return 8
    profile = context.user_data
    db_sess = db_session.create_session()
    user = db_sess.query(users.User).filter(users.User.id == update.message.from_user.id).first()
    db_sess = db_session.create_session()
    user.to_bd(profile, db_sess)
    db_sess.commit()
    reply_keyboard = [["продолжить"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text("Анкета создана.", reply_markup=markup)
    return 9


def inst_add(update, context):
    if not update.message.text:
        update.message.reply_text("Введи свой инстаграмм корректно")
        return 11
    db_sess = db_session.create_session()
    user = db_sess.query(users.User).filter(users.User.id == update.message.from_user.id).first()
    user.set_insta(db_sess, update.message.text)
    reply_keyboard = [["⬅"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text("Инстаграмм привязан", reply_markup=markup)
    return 9
