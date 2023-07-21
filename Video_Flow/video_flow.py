import os

from pytube import YouTube
from moviepy.editor import VideoFileClip


def video_flow(bot, message):
    if message.text.startswith('https://www.youtube.com/watch'):
        download_and_convert_mp3(bot, message)
    elif message.text.startswith('https://youtu.be'):
        download_and_convert_mp3(bot, message)
    elif message.text.startswith('http'):
        bot.send_message(message.chat.id, "Скачать трек могу только по ссылке, которая начинается с "
                                          "https\\:\\/\\/www\\.\\[ "
                                          "youtube\\]\\.com\\/watch?v\\=", parse_mode='MarkdownV2')


def download_and_convert_mp3(bot, message):
    video_url = message.text
    yt = YouTube(video_url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    video_title = video.title + ".mp4"

    try:
        # Скачиваем видео
        current_file_path = os.path.abspath(__file__)
        project_directory = os.path.dirname(current_file_path)
        video_path_dir = os.path.join(project_directory, 'video_to_mp3_bot_tmp')
        video_path = f'{video_path_dir}/{video_title}'
        video.download(output_path=video_path_dir, filename=video_title)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при скачивании видео")

    audio_path = f'{video_path_dir}/{video_title}.mp3'
    video_clip = VideoFileClip(video_path)
    video_clip.audio.write_audiofile(audio_path, codec='mp3')

    audio_file = open(audio_path, 'rb')
    bot.send_audio(chat_id=message.chat.id, audio=audio_file)

    # Удаляем скачанное видео и аудио
    video_clip.close()
    os.remove(video_path)
    os.remove(audio_path)
