import telebot
import token_bot
from API.user import get_user_by_telegram_id, create_user


def auth(bot, message):
    bot.send_message(message.chat.id, "Начался процесс авторизации(убрать текст)")
    return bool(check_user_exist(bot, message)['isActive'])
    # if message.from_user.id == 1063715692:
    #     bot.send_message(message.chat.id, "Да здравствует мой господин!!")
    #     return True
    # elif message.from_user.id == 1386813746:
    #     bot.send_message(message.chat.id, "Макс, заебал. сделай своего бота")
    #     bot.send_message(message.chat.id, "Access denied!")
    #     return False
    # elif message.from_user.id == 597741205:
    #     bot.send_message(message.chat.id, "Карина, ты прекрасна как всегда!")
    #     return True
    # elif message.from_user.id == 109382558:
    #     bot.send_message(message.chat.id, "Карина Р. хочет есть🐹!")
    #     return True
    # else:
    #     bot.send_message(message.chat.id, "Кто ты, странник??")


def check_user_exist(bot, message):
    response = get_user_by_telegram_id(message.from_user.id)
    if 'message' in response and response['message'] == 'User not found':
        bot.send_message(message.chat.id, "User not found! Регистрирую нового пользователя")
        return create_new_user(message)
    else:
        user = response['name']
        bot.send_message(message.chat.id, f"Пользователь {user} найден")
        return response


def create_new_user(message):
    name = message.from_user.first_name
    last_name = message.from_user.last_name
    return create_user(
        f"{name} {last_name}",
        message.from_user.username,
        message.from_user.id,
        0,
        False)
