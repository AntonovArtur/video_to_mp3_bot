from flask import Flask, jsonify, request
from database import execute_query, create_users_table

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:example@db:5103/postgres'


# Маршрут для корневого URL (метод GET)
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the API!'})


# Маршрут для создания нового пользователя (метод POST)
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data['name']
    team_name = data['team_name']
    isActive = data['isActive']
    telegram_id = data['telegram_id']
    balance = data['balance']

    # Проверяем наличие пользователя с заданным telegram_id
    query = 'SELECT * FROM users WHERE telegram_id = %s;'
    params = (telegram_id,)
    result = execute_query(query, params)
    if len(result) > 0:
        return jsonify({'message': 'User with this telegram_id already exists'}), 400

    query = '''
    INSERT INTO users (name, team_name, isActive, telegram_id, balance)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
    '''
    params = (name, team_name, isActive, telegram_id, balance)
    result = execute_query(query, params)
    new_user_id = result[0][0]

    response = {
        'id': new_user_id,
        'name': name,
        'team_name': team_name,
        'isActive': isActive,
        'telegram_id': telegram_id,
        'balance': balance
    }
    return jsonify(response), 201


# Маршрут для получения списка пользователей (метод GET)
@app.route('/users', methods=['GET'])
def get_users():
    query = 'SELECT * FROM users;'
    result = execute_query(query)
    users = []
    for row in result:
        user = {
            'id': row[0],
            'name': row[1],
            'team_name': row[2],
            'telegram_id': row[3],
            'balance': float(row[4]),
            'isActive': row[5]
        }
        users.append(user)
    return jsonify(users)


# Маршрут для получения пользователя по telegram_id (метод GET)
@app.route('/users/<int:telegram_id>', methods=['GET'])
def get_user_by_telegram_id(telegram_id):
    query = 'SELECT * FROM users WHERE telegram_id = %s;'
    params = (telegram_id,)
    result = execute_query(query, params)

    if len(result) == 0:
        return jsonify({'message': 'User not found'}), 404

    user = {
        'id': result[0][0],
        'name': result[0][1],
        'team_name': result[0][2],
        'telegram_id': result[0][3],
        'balance': float(result[0][4]),
        'isActive': result[0][5]
    }
    return jsonify(user)


# Маршрут для обновления информации о пользователе (метод PUT)
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data['name']
    team_name = data['team_name']
    isActive = data['isActive']
    telegram_id = data['telegram_id']
    balance = data['balance']

    query = '''
        UPDATE users
        SET name = %s, team_name = %s, isActive = %s, telegram_id = %s, balance = %s
        WHERE telegram_id = %s
        RETURNING id; -- Возвращаем обновленное значение поля id
        '''
    params = (name, team_name, isActive, telegram_id, balance, user_id)
    result = execute_query(query, params)

    response = {
        'id': result[0][0],  # Возвращаем обновленное значение id
        'name': name,
        'team_name': team_name,
        'isActive': isActive,
        'telegram_id': telegram_id,
        'balance': balance
    }
    return jsonify(response)


# Маршрут для удаления пользователя (метод DELETE)
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    query = 'DELETE FROM users WHERE telegram_id = %s;'
    params = (user_id,)
    execute_query(query, params)

    return jsonify({'message': 'User deleted'})


# Маршрут для изменения баланса пользователя по telegram_id (метод PUT)
@app.route('/users/<int:telegram_id>/balance', methods=['PUT'])
def set_balance(telegram_id):
    data = request.get_json()
    balance = data['balance']

    query = 'UPDATE users SET balance = %s WHERE telegram_id = %s;'
    params = (balance, telegram_id)
    execute_query(query, params)

    return jsonify({'message': 'Balance updated successfully'})


@app.route('/users/<int:telegram_id>/is_active', methods=['PUT'])
def user_activation(telegram_id):
    data = request.get_json()
    balance = data['isActive']

    query = 'UPDATE users SET isActive = %s WHERE telegram_id = %s;'
    params = (balance, telegram_id)
    execute_query(query, params)

    return jsonify({'message': 'Activation is updated successfully'})


# Маршрут для добавления нового поля в указанную таблицу (метод PUT)
@app.route('/add_field', methods=['PUT'])
def add_field():
    data = request.get_json()
    table_name = data['table_name']
    field_name = data['field_name']
    field_type = data['field_type']
    default_value = data.get('default_value', None)

    # Формируем SQL-запрос для добавления поля с заданными параметрами
    if default_value is not None:
        query = f'ALTER TABLE {table_name} ADD COLUMN {field_name} {field_type} DEFAULT {default_value};'
    else:
        query = f'ALTER TABLE {table_name} ADD COLUMN {field_name} {field_type};'

    if execute_query(query):
        return jsonify({'message': f'Field {field_name} added successfully to table {table_name}'})
    else:
        return jsonify({'message': 'Failed to add the field'})


if __name__ == '__main__':
    create_users_table()  # Создаем таблицу users при запуске приложения
    app.run(debug=True, host='0.0.0.0', port=8009)
