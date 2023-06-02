import os

from pytube import YouTube
from moviepy.editor import VideoFileClip
import telebot
import token

bot = telebot.TeleBot(token.bot_token)
chat_id = '-1001989493249'


def handle_message(message):
    if message.text.startswith('https://www.youtube.com'):
        print(message)
        video_url = message.text
        # Создаем объект YouTube
        yt = YouTube(video_url)

        # Выбираем видео в формате mp4 с наилучшим качеством
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video_title = video.title + ".mp4"

        # Скачиваем видео
        video_path_dir = '/Users/a1/Desktop/video_to_mp3_bot_tmp/'
        video_path = f'{video_path_dir}{video_title}'
        video.download(output_path=video_path_dir, filename=video_title)

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


def start():
    while True:
        try:
            # Получаем обновления о новых сообщениях
            updates = bot.get_updates()

            # Перебираем полученные обновления
            for update in updates:
                if update.message is not None:
                    handle_message(update.message)
        except Exception as e:
            print(e)
            # При возникновении ошибки продолжаем выполнение цикла
            continue


start()
