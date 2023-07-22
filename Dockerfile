FROM python:3.9-slim

# Установка supervisord
RUN pip install supervisor

# Копируем файл конфигурации supervisord в контейнер
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Создаем директорию для приложения
WORKDIR /video_to_mp3_bot

# Копируем requirements.txt внутрь контейнера
COPY requirements.txt .

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы из текущей директории (папка Dockerfile) внутрь контейнера
COPY . .

# Запускаем supervisord, который запустит оба приложения (app.py и main.py)
# CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

CMD ["python", "app.py"]
#CMD ["python", "main.py"]
# Запуск сервера Flask при запуске контейнера
# CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
