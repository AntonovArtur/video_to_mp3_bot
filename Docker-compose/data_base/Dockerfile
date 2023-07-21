FROM postgres:latest

# Копирование SQL-скрипта внутрь контейнера
COPY init.sql /docker-entrypoint-initdb.d/

# Установка пароля для суперпользователя PostgreSQL
ENV POSTGRES_PASSWORD=password

# Запуск базы данных PostgreSQL
CMD ["postgres"]