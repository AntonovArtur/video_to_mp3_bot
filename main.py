import telebot
import token_bot
from Auth.auth import auth
from Video_Flow.video_flow import video_flow

bot = telebot.TeleBot(token_bot.bot_token)
chat_id = '-1001989493249'


def handle_message(message):
    if auth(bot, message):
        video_flow(bot, message)
    else:
        bot.send_message(message.chat.id, "Register first")


def start():
    global update
    last_update_id = 0  # Идентификатор последнего обновления

    while True:
        try:
            # Получаем обновления о новых сообщениях, начиная с последнего обновления + 1
            updates = bot.get_updates(offset=last_update_id + 1)

            # Перебираем полученные обновления
            for update in updates:
                if update.message is not None:
                    handle_message(update.message)

                    # Обновляем значение последнего обновления
                    last_update_id = update.update_id

        except Exception as e:
            print(e)
            last_update_id = update.update_id
            # При возникновении ошибки продолжаем выполнение цикла
            continue


# bot.polling()
start()
