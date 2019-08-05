DROP TABLE IF EXISTS Actors;
DROP TABLE IF EXISTS Movies;
DROP TABLE IF EXISTS Movie_Cast;

CREATE TABLE Actors (
    nconst TEXT PRIMARY KEY,
    primaryName TEXT,
    birthYear TEXT,
    deathYear TEXT,
    primaryProfession TEXT,
    knownForTitles TEXT,
    updated TEXT
);

CREATE TABLE Movies (
    tconst TEXT PRIMARY KEY,
    titleType TEXT,
    primaryTitle TEXT,
    originalTitle TEXT,
    isAdult INTEGER,
    startYear TEXT,
    endYear TEXT,
    runtimeMinutes Text,
    genres TEXT,
    updated TEXT
);

CREATE TABLE Movie_Cast (
    nconst REFERENCES Actors (nconst),
    tconst REFERENCES Movies (tconst),
    PRIMARY KEY (nconst, tconst)
);

