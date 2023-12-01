'''
competitions
{
    "id": 202353,
    "name": "Гран-при ФИДЕ 1998",
    "city": "Тбилиси",
    "begin": "09.04",
    "system": "Olympic",
    "tours_count": 13,
    "min_rating": 2539,
    "time_on_game": 17
}

info_place
{
    'name': 'Кубок мира 1974', 
    'place': 0, 
    'prise': 21000000
}

Создание таблиц в БД
CREATE TABLE competitions (
    id           INTEGER    PRIMARY KEY AUTOINCREMENT,
    comp_id      INTEGER,
    name         TEXT (256),
    city         TEXT (256),
    begin        TEXT (256),
    system       TEXT (256),
    tours_count  INTEGER,
    min_rating   INTEGER,
    time_on_game INTEGER
);
CREATE TABLE info_prises (
    id      INTEGER    PRIMARY KEY AUTOINCREMENT,
    comp_id INTEGER    REFERENCES competitions (comp_id),
    name    TEXT (256),
    place   INTEGER,
    prise   INTEGER
);
'''