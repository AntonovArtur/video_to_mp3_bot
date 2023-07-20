import os

from pytube import YouTube
from moviepy.editor import VideoFileClip
import telebot
import token_bot

bot = telebot.TeleBot(token_bot.bot_token)
chat_id = '-1001989493249'


def download_and_convert_mp3(video):
    print("download_and_convert_mp3")
    video_title = video.title + ".mp4"

    try:
        # Скачиваем видео
        video_path_dir = '/Users/a1/Desktop/video_to_mp3_bot_tmp/'
        video_path = f'{video_path_dir}{video_title}'
        video.download(output_path=video_path_dir, filename=video_title)
    except Exception as e:
        bot.send_message(chat_id, f"Произошла ошибка при скачивании видео")

    # Задаем путь для сохранения аудио файла с тем же названием
    audio_path = f'{video_path_dir}{video_title}.mp3'

    # Конвертируем видео в аудио формат
    video_clip = VideoFileClip(video_path)
    video_clip.audio.write_audiofile(audio_path, codec='mp3')

    # Отправляем аудио-файл через Telegram бота

    audio_file = open(audio_path, 'rb')
    bot.send_audio(chat_id=chat_id, audio=audio_file)

    # Удаляем скачанное видео и аудио
    video_clip.close()
    os.remove(video_path)
    os.remove(audio_path)


def handle_message(message):
    bot.send_message(chat_id, message.from_user.id)
    if message.from_user.id == 1063715692:
        bot.send_message(chat_id, "Да здравствует мой господин!")
    elif message.from_user.id == 1386813746:
        bot.send_message(chat_id, "Макс, заебал. сделай своего бота")
    elif message.from_user.id == 597741205:
        bot.send_message(chat_id, "Карина, ты прекрасна как всегда!")

    else:
        bot.send_message(chat_id, "Кто ты, странник??")

    if message.text.startswith('https://www.youtube.com/watch'):
        video_url = message.text
        yt = YouTube(video_url)
        # Выбираем видео в формате mp4 с наилучшим качеством
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        download_and_convert_mp3(video)

    elif message.text.startswith('https://youtu.be'):
        print(message)
        video_url = message.text
        yt = YouTube(video_url)
        # выбираем видео в формате mp4 с наилучшим качеством
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        download_and_convert_mp3(video)
    elif message.text.startswith('http'):
        bot.send_message(chat_id, "Скачать трек могу только по ссылке, которая начинается с https\\:\\/\\/www\\.\\["
                                  "youtube\\]\\.com\\/watch?v\\=", parse_mode='MarkdownV2')


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
