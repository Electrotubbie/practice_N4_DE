import pickle
import msgpack
import sqlite3
from general_functions import *
from pprint import pprint

VAR = 37
TASK_PATH = './task3/'
RESULTS_PATH = f'{TASK_PATH}results/'
DATASET_1_NAME = 'task_3_var_37_part_1.pkl'
DATASET_2_NAME = 'task_3_var_37_part_2.msgpack'
DB_NAME = './task3.db'

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany('''
        INSERT INTO music
        (acousticness, artist, duration_ms, genre, song, tempo, year)
        VALUES
        (:acousticness, :artist, :duration_ms, :genre, :song, :tempo, :year)
    ''', data)
    db.commit()
    cursor = db.cursor()

def get_top_by(db, limit):
    # выполняется сортировка по полю tempo
    cursor = db.cursor()
    result = cursor.execute('''
        SELECT * 
        FROM music 
        ORDER BY tempo DESC 
        LIMIT ?
    ''', [limit])
    items = [dict(item) for item in result.fetchall()]
    cursor.close()
    return items

def get_stat_by(db):
    # выполняется анализ поля year
    cursor = db.cursor()
    res = cursor.execute('''
        SELECT
            SUM(year) as sum,
            AVG(year) as avg,
            MIN(year) as min,
            MAX(year) as max
        FROM music
    ''')
    stats = dict(res.fetchone())
    cursor.close()
    return stats

def get_freqs(db):
    # выполняется запрос частоты встречаемости поля artist
    cursor = db.cursor()
    res = cursor.execute('''
        SELECT artist, count(*) as count
        FROM music
        GROUP BY artist
        ORDER BY count DESC
    ''')
    stats = {
        list(item)[0]:list(item)[1]
        for item in res.fetchall()
    }
    cursor.close()
    return stats

def get_top_filtered_sorted(db, limit):
    # фильтрация по genre содержит metal 
    # и сортировка по year
    cursor = db.cursor()
    result = cursor.execute('''
        SELECT * 
        FROM music
        WHERE genre GLOB "*[m|M]etal*"
        ORDER BY year ASC
        LIMIT ?
    ''',[limit])
    items = [dict(item) for item in result.fetchall()]
    cursor.close()
    return items

def main():
    with open(f'{TASK_PATH}{DATASET_1_NAME}', mode='rb') as f:
        data_1 = pickle.load(f)
    with open(f'{TASK_PATH}{DATASET_2_NAME}', mode='rb') as f:
        data_2 = list(msgpack.load(f))
    data = data_1 + data_2

    database = connect_to_db(f'{TASK_PATH}{DB_NAME}')
    # закомментирована строка, чтоб далее не пополнить БД аналогичными строками
    # insert_data(database, data)

    top = get_top_by(database, VAR+10)
    save_as_json(top, f'{RESULTS_PATH}res1_top.json')

    stats_nums = get_stat_by(database)
    save_as_json(stats_nums, f'{RESULTS_PATH}res2_stats_nums.json')

    stats_categories = get_freqs(database)
    save_as_json(stats_categories, f'{RESULTS_PATH}res3_stats_categories.json')

    top_filtered_sorted = get_top_filtered_sorted(database, VAR+15)
    save_as_json(top_filtered_sorted, f'{RESULTS_PATH}res4_top_filtered_sorted.json')
    database.close()

if __name__ == '__main__':
    main()

# # получение всех ключей из двух датасетов
# data_keys_1 = []
# data_keys_2 = []
# for row in data_1:
#     data_keys_1.extend(row.keys())
# for row in data_2:
#     data_keys_2.extend(row.keys())
# data_keys_1 = set(data_keys_1)
# # pprint(data_keys_1)
# data_keys_2 = set(data_keys_2)
# # pprint(data_keys_2)
# print(*[item for item in list(data_keys_1) if item in data_keys_2], sep=', ')