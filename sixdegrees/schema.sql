CREATE TABLE Movie_Cast (
    nconst REFERENCES Actors (nconst),
    tconst REFERENCES Movies (tconst),
    PRIMARY KEY (nconst, tconst)
)