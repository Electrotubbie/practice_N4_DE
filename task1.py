import json
import sqlite3
from general_functions import *
from pprint import pprint

VAR = 37
TASK_PATH = './task1/'
RESULTS_PATH = f'{TASK_PATH}results/'
DATASET_NAME = 'task_1_var_37_item.json'
DB_NAME = 'task1.db'

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany('''
        INSERT INTO competitions 
        (comp_id, name, city, begin, system, tours_count, min_rating, time_on_game)
        VALUES(:id, :name, :city, :begin, :system, :tours_count, :min_rating, :time_on_game)
    ''', data)
    db.commit()
    cursor = db.cursor()

def get_top_by(db, limit):
    # выполняется сортировка по полю tours_count
    cursor = db.cursor()
    result = cursor.execute('''
        SELECT * 
        FROM competitions 
        ORDER BY tours_count DESC 
        LIMIT ?
    ''', [limit])
    items = [dict(item) for item in result.fetchall()]
    cursor.close()
    return items

def get_stat_by(db):
    # выполняется анализ поля time_on_game
    cursor = db.cursor()
    res = cursor.execute('''
        SELECT
            SUM(time_on_game) as sum,
            AVG(time_on_game) as avg,
            MIN(time_on_game) as min,
            MAX(time_on_game) as max
        FROM competitions
    ''')
    stats = dict(res.fetchone())
    cursor.close()
    return stats

def get_freqs(db):
    # выполняется запрос частоты встречаемости поля city
    cursor = db.cursor()
    res = cursor.execute('''
        SELECT city, count(*) as count
        FROM competitions
        GROUP BY city
        ORDER BY count DESC
    ''')
    stats = {
        list(item)[0]:list(item)[1]
        for item in res.fetchall()
    }
    cursor.close()
    return stats

def get_top_filtered_sorted(db, min_rating, limit):
    # фильтрация по min_rating > заданного значения 
    # и сортировка по time_on_game
    cursor = db.cursor()
    result = cursor.execute('''
        SELECT * 
        FROM competitions
        WHERE min_rating > ?
        ORDER BY time_on_game DESC
        LIMIT ?
    ''',[min_rating, limit])
    items = [dict(item) for item in result.fetchall()]
    cursor.close()
    return items

def main():
    with open(f'{TASK_PATH}{DATASET_NAME}', mode='r', encoding='UTF-8') as f:
        data = list(json.load(f))
    database = connect_to_db(f'{TASK_PATH}{DB_NAME}')
    # закомментирована строка, чтоб далее не пополнить БД аналогичными строками
    # insert_data(database, data)

    top = get_top_by(database, VAR+10)
    save_as_json(top, f'{RESULTS_PATH}res1_top.json')

    stats_nums = get_stat_by(database)
    save_as_json(stats_nums, f'{RESULTS_PATH}res2_stats_nums.json')

    stats_categories = get_freqs(database)
    save_as_json(stats_categories, f'{RESULTS_PATH}res3_stats_categories.json')

    top_filtered_sorted = get_top_filtered_sorted(database, 2340, VAR+10) # 2340 подогнал так, чтоб срезало по VAR+10
    save_as_json(top_filtered_sorted, f'{RESULTS_PATH}res4_top_filtered_sorted.json')
    database.close()

if __name__ == '__main__':
    main()