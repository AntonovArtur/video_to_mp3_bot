import os
import uuid

import telebot
import token_bot
from Auth.auth import auth
from Features.speach_to_text import speech_to_text_from_file
from Video_Flow.video_flow import video_flow

bot = telebot.TeleBot(token_bot.bot_token)


# chat_id = '-1001989493249'
@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    bot.send_message(message.chat.id, "voice message")


    # Вызываем функцию для распознавания речи из файла
    recognized_text = speech_to_text_from_file(bot, message)

    # Отправляем пользователю распознанный текст
    bot.send_message(message.chat.id, f"Распознанный текст: {recognized_text}")


def handle_message(message):
    bot.send_message(message.chat.id, message)
    if auth(bot, message):
        video_flow(bot, message)
    else:
        bot.send_message(message.chat.id, "Ваш аккаунт не активарован. Обратитесь в поддержку")


def start():
    global update
    last_update_id = 0  # Идентификатор последнего обновления

    while True:
        try:
            # Получаем обновления о новых сообщениях, начиная с последнего обновления + 1
            updates = bot.get_updates(offset=last_update_id + 1)

            # Перебираем полученные обновления
            for update in updates:
                last_update_id = update.update_id
                if update.message is not None:
                    if "voice" in update.message.content_type:
                        handle_voice_message(update.message)

                    continue
                handle_message(update.message)
                # Обновляем значение последнего обновления

        except Exception as e:
            print(e)
            last_update_id = update.update_id
            # При возникновении ошибки продолжаем выполнение цикла
            continue


# bot.polling()
start()
