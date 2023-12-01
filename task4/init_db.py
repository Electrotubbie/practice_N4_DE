'''
CREATE TABLE product (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT,
    price       REAL,
    quantity    INTEGER,
    category    TEXT,
    fromCity    TEXT,
    isAvailable TEXT,
    views       INTEGER,
    version     INTEGER DEFAULT (0) 
);
'''
