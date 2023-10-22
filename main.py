from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CommandHandler
from profile import greeting, age_add, about_add, city_add, inst_add, photo_add, \
    sex_add, type_partner_add, name_add
from project_data import db_session
from menu import menu_handler, menu
from start import start
import os

PORT = int(os.environ.get('PORT', 5000))


def stop(update, context):
    pass


def main():
    updater = Updater("1630023550:AAEjhu8caj8GfiHPcP32cMTG7zmtWz9GnVQ")
    db_session.global_init("db/users.db")
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.all, greeting)],
            2: [MessageHandler(Filters.all, age_add)],
            3: [MessageHandler(Filters.all, city_add)],
            4: [MessageHandler(Filters.all, photo_add)],
            5: [MessageHandler(Filters.all, name_add)],
            6: [MessageHandler(Filters.all, sex_add)],
            7: [MessageHandler(Filters.all, about_add)],
            8: [MessageHandler(Filters.all, type_partner_add)],
            9: [MessageHandler(Filters.all, menu)],
            10: [MessageHandler(Filters.text, menu_handler)],
            11: [MessageHandler(Filters.all, inst_add)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)

    print("Bot started")

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path="1630023550:AAEjhu8caj8GfiHPcP32cMTG7zmtWz9GnVQ",
                          webhook_url='https://find-soulmate-bot.herokuapp.com/'
                                      + "1630023550:AAEjhu8caj8GfiHPcP32cMTG7zmtWz9GnVQ")

    updater.idle()


if __name__ == '__main__':
    main()
