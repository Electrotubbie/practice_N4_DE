import json
import sqlite3
from pprint import pprint

VAR = 37
TASK_PATH = './task1/'
RESULTS_PATH = f'{TASK_PATH}results/'
DATASET_NAME = 'task_1_var_37_item.json'
DB_NAME = 'task1.db'

def connect_to_db(db_name):
    connection = sqlite3.connect(db_name)
    connection.row_factory = sqlite3.Row
    return connection

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany('''
        INSERT INTO competitions 
        (id, name, city, begin, system, tours_count, min_rating, time_on_game)
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
    # выполняется анализ колонки time_on_game
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
    # выполняется запрос частоты встречаемости колонки city
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

def save_as_json(data, file_name):
    with open(f'{RESULTS_PATH}{file_name}', mode='w', encoding='UTF-8') as f:
        json.dump(data, f, ensure_ascii=False)

def main():
    with open(f'{TASK_PATH}{DATASET_NAME}', mode='r', encoding='UTF-8') as f:
        data = list(json.load(f))
    database = connect_to_db(f'{TASK_PATH}{DB_NAME}')
    # insert_data(database, data)

    top = get_top_by(database, VAR+10)
    save_as_json(top, 'res1_top.json')

    stats_nums = get_stat_by(database)
    save_as_json(stats_nums, 'res2_stats_nums.json')

    stats_categories = get_freqs(database)
    save_as_json(stats_categories, 'res3_stats_categories.json')

    top_filtered_sorted = get_top_filtered_sorted(database, 2340, VAR+10) # 2340 подогнал так, чтоб срезало по VAR+10
    save_as_json(top_filtered_sorted, 'res4_top_filtered_sorted.json')

if __name__ == '__main__':
    main()