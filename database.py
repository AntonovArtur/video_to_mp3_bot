import psycopg2


# Функция для подключения к базе данных
def connect():
    connection = psycopg2.connect(
        user='postgres',
        password='password',
        host='db',
        port='5432',
        database='postgres'
    )
    return connection


# Функция для выполнения запросов к базе данных
def execute_query(query, params=None):
    connection = None
    cursor = None
    try:
        connection = connect()
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'Error executing query: {error}')
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Функция для создания таблицы users
def create_users_table():
    connection = None
    cursor = None
    try:
        print('СОЗДАЕМ ТАБЛИЦУ')
        connection = connect()
        cursor = connection.cursor()
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            team_name VARCHAR(255),
            telegram_id INTEGER,
            balance DECIMAL(10, 2),
            isActive BOOLEAN
        );
        '''
        cursor.execute(query)
        connection.commit()
        print("Table 'users' created successfully!")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'Error creating table: {error}')
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
