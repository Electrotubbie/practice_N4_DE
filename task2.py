import msgpack
import sqlite3
from general_functions import *
from pprint import pprint

VAR = 37
TASK_PATH = './task2/'
RESULTS_PATH = f'{TASK_PATH}results/'
DATASET_NAME = 'task_2_var_37_subitem.msgpack'
DB_NAME = './task1/task1.db'

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany('''
        INSERT INTO info_prises
        (comp_id, name, place, prise)
        VALUES(
        (SELECT comp_id FROM competitions WHERE name = :name),
        :name, :place, :prise)
    ''', data)
    db.commit()
    cursor = db.cursor()

def first_query(db, comp_name):
    # выбор соревнования c именем name из таблицы info_prises через таблицу competitions
    # и сортировка по полю place в порядке возрастания
    cursor = db.cursor()
    result = cursor.execute('''
        SELECT *
        FROM info_prises
        WHERE comp_id = (SELECT comp_id FROM competitions WHERE name = ?)
        ORDER BY place ASC
    ''',[comp_name])
    items = [dict(item) for item in result.fetchall()]
    cursor.close()
    return items

def second_query(db, **kwargs):
    # выбор всех соревнований с prise > :prise И system = :system 
    # из таблицы competitions через таблицу info_prises
    # и сортировка по полю min_rating в порядке убывания
    cursor = db.cursor()
    result = cursor.execute('''
        SELECT *
        FROM competitions
        WHERE 
        comp_id IN (SELECT comp_id FROM info_prises WHERE prise > :prise) 
        AND system = :system
        ORDER BY min_rating DESC
    ''',kwargs)
    items = [dict(item) for item in result.fetchall()]
    cursor.close()
    return items

def third_query(db, *cities_name):
    # расчёт суммы призового фонда из любых 3-х городов
    # а также сортировка по убыванию относительно нового поля prize_fund
    cursor = db.cursor()
    result = cursor.execute('''
        SELECT comp_id, name, SUM(prise) as prize_fund
        FROM info_prises
        WHERE comp_id IN 
            (SELECT comp_id 
            FROM competitions 
            WHERE city IN (?, ?, ?))
        GROUP BY comp_id
        ORDER BY prize_fund DESC
    ''',cities_name)
    items = [dict(item) for item in result.fetchall()]
    cursor.close()
    return items

def main():
    with open(f'{TASK_PATH}{DATASET_NAME}', mode='rb') as f:
        data = list(msgpack.load(f))
    # pprint(data) # визуальный анализ полученного датасета .msgpack
    database = connect_to_db(f'{DB_NAME}')
    # закомментирована строка, чтоб далее не пополнить БД аналогичными строками
    # insert_data(database, data)

    firts_result = first_query(database, 'Хогевен 1974')
    save_as_json(firts_result, f'{RESULTS_PATH}1_result.json')
    # pprint(firts_result)

    second_result = second_query(database, prise = 10_000_000, system = 'Swiss')
    save_as_json(second_result, f'{RESULTS_PATH}2_result.json')
    # pprint(second_result)

    third_result = third_query(database, "Тбилиси", "Алма-Ата", "Баку")
    save_as_json(third_result, f'{RESULTS_PATH}3_result.json')
    # pprint(third_result)
    database.close()


if __name__ == '__main__':
    main()