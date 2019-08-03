DROP TABLE IF EXISTS Actors;
DROP TABLE IF EXISTS Movies;
DROP TABLE IF EXISTS Movie_Cast;

CREATE TABLE Actors (
    nconst TEXT PRIMARY KEY,
    name TEXT,
    updated TEXT
);

CREATE TABLE Movies (
    tconst TEXT PRIMARY KEY,
    title TEXT,
    year INTEGER,
    updated TEXT
);

CREATE TABLE Movie_Cast (
    nconst REFERENCES Actors (nconst),
    tconst REFERENCES Movies (tconst),
    PRIMARY KEY (nconst, tconst)
);