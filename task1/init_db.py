'''
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

CREATE TABLE competitions (
    ""           INTEGER    PRIMARY KEY AUTOINCREMENT,
    id           INTEGER,
    name         TEXT (256),
    city         TEXT (256),
    begin        TEXT (256),
    system       TEXT (256),
    tours_count  INTEGER,
    min_rating   INTEGER,
    time_on_game INTEGER
);
'''