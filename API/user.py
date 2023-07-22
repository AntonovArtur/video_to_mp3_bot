import requests

# base_url = 'http://localhost:8009'  # Укажите URL вашего API
base_url = 'http://194.87.145.137:8009'  # Укажите URL вашего API


def create_user(name, team_name, telegram_id, balance, is_active):
    url = f'{base_url}/users'
    data = {
        'name': name,
        'team_name': team_name,
        'telegram_id': telegram_id,
        'balance': balance,
        'isActive': is_active
    }
    response = requests.post(url, json=data)
    return response.json()


def get_all_users():
    url = f'{base_url}/users'
    response = requests.get(url)
    return response.json()

# TODO дописать обработку ошибок


def get_user_by_telegram_id(telegram_id):
    url = f'{base_url}/users/{telegram_id}'
    response = requests.get(url)
    return response.json()


def update_user(user_id, name, team_name, telegram_id, balance, is_active):
    url = f'{base_url}/users/{user_id}'
    data = {
        'name': name,
        'team_name': team_name,
        'telegram_id': telegram_id,
        'balance': balance,
        'isActive': is_active
    }
    response = requests.put(url, json=data)
    return response.json()


def delete_user(user_id):
    url = f'{base_url}/users/{user_id}'
    response = requests.delete(url)
    return response.json()


def update_balance(telegram_id, balance):
    url = f'{base_url}/users/{telegram_id}/balance'
    data = {
        'balance': balance
    }
    response = requests.put(url, json=data)
    return response.json()


def update_user_activation(telegram_id, is_active):
    url = f'{base_url}/users/{telegram_id}/is_active'
    data = {
        'isActive': is_active
    }
    response = requests.put(url, json=data)
    return response.json()
