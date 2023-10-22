from telegram import ReplyKeyboardMarkup


def start(update, context):
    reply_keyboard = [["продолжить"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    update.message.reply_text("Привет, я бот, предназначенный для поиска друга,"
                              " подруги или второй половинки", reply_markup=markup)
    return 1