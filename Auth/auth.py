import telebot
import token_bot


def auth(bot, message):
    bot.send_message(message.chat.id, message.from_user.id)
    if message.from_user.id == 1063715692:
        bot.send_message(message.chat.id, "Да здравствует мой господин!")
        return True
    elif message.from_user.id == 1386813746:
        bot.send_message(message.chat.id, "Макс, заебал. сделай своего бота")
        bot.send_message(message.chat.id, "Access denied!")
        return False
    elif message.from_user.id == 597741205:
        bot.send_message(message.chat.id, "Карина, ты прекрасна как всегда!")
        return True
    elif message.from_user.id == 109382558:
        bot.send_message(message.chat.id, "Карина Р. хочет есть🐹!")
        return True
    else:
        bot.send_message(message.chat.id, "Кто ты, странник??")