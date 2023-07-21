from flask import Flask, jsonify, request
from database import execute_query, create_users_table

app = Flask(__name__)


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
    mustache_count = data['mustache_count']
    telegram_id = data['telegram_id']
    balance = data['balance']

    # Проверяем наличие пользователя с заданным telegram_id
    query = 'SELECT * FROM users WHERE telegram_id = %s;'
    params = (telegram_id,)
    result = execute_query(query, params)
    if len(result) > 0:
        return jsonify({'message': 'User with this telegram_id already exists'}), 400

    query = '''
    INSERT INTO users (name, team_name, mustache_count, telegram_id, balance)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
    '''
    params = (name, team_name, mustache_count, telegram_id, balance)
    result = execute_query(query, params)
    new_user_id = result[0][0]

    response = {
        'id': new_user_id,
        'name': name,
        'team_name': team_name,
        'mustache_count': mustache_count,
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
            'mustache_count': row[3],
            'telegram_id': row[4],
            'balance': float(row[5])
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
        'mustache_count': result[0][3],
        'telegram_id': result[0][4],
        'balance': float(result[0][5])
    }
    return jsonify(user)


# Маршрут для обновления информации о пользователе (метод PUT)
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data['name']
    team_name = data['team_name']
    mustache_count = data['mustache_count']
    telegram_id = data['telegram_id']
    balance = data['balance']

    query = '''
    UPDATE users
    SET name = %s, team_name = %s, mustache_count = %s, telegram_id = %s, balance = %s
    WHERE telegram_id = %s;
    '''
    params = (name, team_name, mustache_count, telegram_id, balance, user_id)
    execute_query(query, params)

    response = {
        'id': user_id,
        'name': name,
        'team_name': team_name,
        'mustache_count': mustache_count,
        'telegram_id': telegram_id,
        'balance': balance
    }
    return jsonify(response)


# Маршрут для удаления пользователя (метод DELETE)
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    query = 'DELETE FROM users WHERE id = %s;'
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


if __name__ == '__main__':
    create_users_table()  # Создаем таблицу users при запуске приложения
    app.run(debug=True, host='0.0.0.0', port=8009)