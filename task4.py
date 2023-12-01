import pickle
import json
import sqlite3
from general_functions import *
from pprint import pprint

VAR = 37
TASK_PATH = './task4/'
RESULTS_PATH = f'{TASK_PATH}results/'
DATASET_1_NAME = 'task_4_var_37_product_data.text'
DATASET_2_NAME = 'task_4_var_37_update_data.pkl'
DB_NAME = './task4.db'

def read_text(file_name):
    to_float = ['price']
    to_int = ['quantity', 'views']
    to_bool = ['isAvailable']

    with open(f'{file_name}', mode='r', encoding='UTF-8') as f:
        lines = f.read()
        
    lines = lines.split('\n')
    data = list()
    row = {'category': 'NA'}
    for line in lines:
        if line == '=====':
            data.append(row)
            row = {'category': 'NA'}
        else:
            underlines = line.split('::')
            if underlines[0] in to_float:
                row[underlines[0]] = float(underlines[1])
            elif underlines[0] in to_int:
                row[underlines[0]] = int(underlines[1])
            elif underlines[0] in to_bool:
                row[underlines[0]] = underlines[1] == "True"
            elif underlines[0]:
                row[underlines[0]] = underlines[1]
    return data

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany('''
        INSERT INTO product
        (category, fromCity, isAvailable, name, price, quantity, views)
        VALUES
        (:category, :fromCity, :isAvailable, :name, :price, :quantity, :views)
    ''', data)
    db.commit()
    cursor = db.cursor()

def handle_method(cursor, name, method, param=None):
    if method == 'remove':
        cursor.execute('DELETE FROM product WHERE name = ?', [name])
    elif method == 'quantity_add':
        cursor.execute('UPDATE product SET quantity = quantity + ?, version = version + 1 WHERE name = ?', [abs(param), name])
    elif method == 'quantity_sub':
        cursor.execute('UPDATE product SET quantity = quantity - ?, version = version + 1 WHERE name = ? AND ((quantity - ?) > 0)', [abs(param), name, abs(param)])
    elif method == 'price_percent':
        cursor.execute('UPDATE product SET price = ROUND(price * (1 + ?), 2), version = version + 1 WHERE name = ?', [param, name])
    elif method == 'price_abs':
        cursor.execute(f"UPDATE product SET price = price + ?, version = version + 1 WHERE name = ? AND ((price + ?) > 0)", [param, name, param])
    elif method == 'available':
        cursor.execute('UPDATE product SET isAvailable = ?, version = version + 1 WHERE name == ?', [1 if param else 0, name])
    else:
        raise ValueError(f'{method} метода нет!')

def handle_updates(db, data):
    cursor = db.cursor()
    for update in data:
        handle_method(db, update['name'], update['method'], update['param'])
    db.commit()

def get_top_updated(db):
    cursor = db.cursor()
    result = cursor.execute(f"SELECT * FROM product ORDER BY version DESC LIMIT 10")
    items = [dict(item) for item in result.fetchall()]
    cursor.close()
    return items

def get_prices_by_category(db):
    cursor = db.cursor()
    result = cursor.execute(f'''SELECT category, COUNT(*) as count,
                            MAX(price) as max,
                            MIN(price) as min,
                            ROUND(SUM(price), 2) as sum, 
                            ROUND(AVG(price), 2) as avg 
                            FROM product 
                            GROUP BY category''')
    items = [dict(item) for item in result.fetchall()]
    cursor.close()
    return items

def get_quantity_by_category(db):
    cursor = db.cursor()
    result = cursor.execute(f'''SELECT category, 
                            MAX(quantity) as max, 
                            MIN(quantity) as min,
                            SUM(quantity) as sum, 
                            AVG(quantity) as avg 
                            FROM product 
                            GROUP BY category''')
    items = [dict(item) for item in result.fetchall()]
    cursor.close()
    return items

def get_data_from_category(db):
    cursor = db.cursor()
    result = cursor.execute(f'''SELECT category, 
                                MAX(price) as max, 
                                MIN(price) as min 
                                FROM product
                                WHERE category = "tools" 
                                ''')
    items = [dict(item) for item in result.fetchall()]
    cursor.close()
    return items

def main():
    data = read_text(f'{TASK_PATH}{DATASET_1_NAME}')
    with open(f'{TASK_PATH}{DATASET_2_NAME}', mode='rb') as f:
        updates = pickle.load(f)
    # print(*list(set([meth['method'] for meth in updates])), sep=', ')
    # quantity_add, price_percent, available, quantity_sub, price_abs, remove
    database = connect_to_db(f'{TASK_PATH}{DB_NAME}')
    # закомментирована строка, чтоб далее не пополнить БД аналогичными строками
    insert_data(database, data)
    handle_updates(database, updates)

    top = get_top_updated(database)
    save_as_json(top, f'{RESULTS_PATH}res1_top.json')

    stats_nums_prices_by_cat = get_prices_by_category(database)
    save_as_json(stats_nums_prices_by_cat, f'{RESULTS_PATH}res2_prices_by_cat.json')

    stats_quantity_by_category = get_quantity_by_category(database)
    save_as_json(stats_quantity_by_category, f'{RESULTS_PATH}res3_quant_by_cat.json')

    stats_data_from_category = get_data_from_category(database)
    save_as_json(stats_data_from_category, f'{RESULTS_PATH}res4_data_from_tools.json')

    database.close()


if __name__ == '__main__':
    main()