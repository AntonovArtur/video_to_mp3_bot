import os
import uuid
from pydub import AudioSegment

import speech_recognition as sr


def speech_to_text_from_file(bot, message):
    bot.send_message(message.chat.id, "test1")
    # Генерируем уникальное имя для аудиофайла
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    # Получаем абсолютный путь к текущей директории
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Создаем путь к директории "audio_files" в текущей директории
    audio_files_directory = os.path.join(current_directory, "audio_files")

    # Путь к аудиофайлу с уникальным именем
    audio_file_name = os.path.join(audio_files_directory, f"{str(uuid.uuid4())}.ogg")

    downloaded_file = bot.download_file(file_path)
    with open(audio_file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    # Путь к сконвертированному аудиофайлу в формате WAV
    wav_file_name = os.path.splitext(audio_file_name)[0] + ".wav"
    try:
        convert_ogg_to_wav(audio_file_name, wav_file_name)
    except Exception as error:
        exception_value = f'Error converting OGG to WAV: {error}'
        bot.send_message(message.chat.id, exception_value)
    # finally:

    bot.send_message(message.chat.id, "test3")
    recognizer = sr.Recognizer()
    print("recognizer = sr.Recognizer()")

    with sr.AudioFile(wav_file_name) as source:
        audio_data = recognizer.record(source)

    try:
        recognized_text = recognizer.recognize_google(audio_data, language="ru-RU")
        return recognized_text
    except sr.UnknownValueError:
        return "Речь не распознана"
    except sr.RequestError as e:
        return f"Ошибка запроса к сервису распознавания речи; {e}"


def convert_ogg_to_wav(ogg_file_path, wav_file_path):
    audio = AudioSegment.from_file(ogg_file_path, format="ogg")
    audio.export(wav_file_path, format="wav")

