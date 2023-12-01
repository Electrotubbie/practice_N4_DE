import json
import sqlite3

def save_as_json(data, path):
    with open(f'{path}', mode='w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False)

def connect_to_db(db_name):
    connection = sqlite3.connect(db_name)
    connection.row_factory = sqlite3.Row
    return connection