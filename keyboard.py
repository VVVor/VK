import json

def get_button(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


keyboard = {
    "one_time": False,
    "buttons": [
        [get_button('Начать поиск', 'primary')],
        [get_button('Вперёд', 'secondary')]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

request_token_keyboard = {
    "one_time": False,
    "buttons": [
        [get_button('Разрешить', 'primary')],
    ]
}

request_token_keyboard = json.dumps(request_token_keyboard, ensure_ascii=False).encode('utf-8')
request_token_keyboard = str(request_token_keyboard.decode('utf-8'))

sql_keyboard = {
    "one_time": True,
    "buttons": [
        [get_button('Создать базу', 'primary')],
    ]
}

sql_keyboard = json.dumps(sql_keyboard, ensure_ascii=False).encode('utf-8')
empty = str(sql_keyboard.decode('utf-8'))

next_keyboard = {
    "one_time": True,
    "buttons": [
        [get_button('Дальше', 'primary')],
    ]
}

next_keyboard = json.dumps(next_keyboard, ensure_ascii=False).encode('utf-8')
next_keyboard = str(next_keyboard.decode('utf-8'))