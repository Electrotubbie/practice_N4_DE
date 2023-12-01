'''
1_DATA
{
    'acousticness': '0.0811', +
    'artist': 'Sean Paul', +
    'duration_ms': '232506', +
    'energy': '0.78',
    'genre': 'hip hop, pop', +
    'popularity': '61', 
    'song': 'Like Glue', +
    'tempo': '97.917', +
    'year': '2002' +
}
2_DATA
{
    'acousticness': '0.0191',
    'artist': 'Cobra Starship',
    'duration_ms': '215693',
    'genre': 'pop, Dance/Electronic',
    'instrumentalness': '0.748',
    'mode': '0',
    'song': 'You Make Me Feel... (feat. Sabi)',
    'speechiness': '0.0535',
    'tempo': '131.959',
    'year': '2011'
}
В итоге:
acousticness, artist, duration_ms, genre, song, tempo, year

CREATE TABLE music (
    id           INTEGER    PRIMARY KEY AUTOINCREMENT,
    acousticness REAL,
    artist       TEXT (256),
    duration_ms  INTEGER,
    genre        TEXT (256),
    song         TEXT (256),
    tempo        REAL,
    year         INTEGER
);

'''