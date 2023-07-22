import os
import uuid

import telebot
import token_bot
from API.user import get_all_users
from Auth.auth import auth
from Features.speach_to_text import speech_to_text_from_file
from Video_Flow.video_flow import video_flow

bot = telebot.TeleBot(token_bot.bot_token)


# chat_id = '-1001989493249'
def search_voice_cmd(bot, message, recognized_text):
    if recognized_text == "список участников":
        response = get_all_users()
        bot.reply_to(message, str(response))


@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    if auth(bot, message):
        bot.reply_to(message, "voice message")
        recognized_text = speech_to_text_from_file(bot, message)
        bot.reply_to(message, f"Распознанный текст: {recognized_text}")
        search_voice_cmd(bot, message, recognized_text)
    else:
        bot.send_message(message.chat.id, "Чтобы пользоваься услугой перевода текста в текст нужно активаровать "
                                          "аккаунт. Обратитесь в поддержку")


def handle_message(message):
    # bot.send_message(message.chat.id, message)
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
                if update.message is not None and "voice" in update.message.content_type:
                    handle_voice_message(update.message)
                    continue
                elif update.message is not None:
                    handle_message(update.message)
                    # Обновляем значение последнего обновления

        except Exception as e:
            print(e)
            last_update_id = update.update_id
            # При возникновении ошибки продолжаем выполнение цикла
            continue


# bot.polling()
start()
