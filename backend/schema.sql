CREATE TABLE IF NOT EXISTS Platform (
    PlatformID TEXT,
    PRIMARY KEY (PlatformID)
);

INSERT INTO Platform (PlatformID)
VALUES
    ('YOUTUBE'),
    ('SOUNDCLOUD'),
    ('SPOTIFY')
;

CREATE TABLE IF NOT EXISTS Playlist (
    PlaylistID TEXT,
    Platform TEXT,
    Title TEXT,
    Owner TEXT,
    Description TEXT,
    Thumbnail TEXT,  -- thumbnail endpoint with max res
    Length INTEGER,
    Etag TEXT,
    PRIMARY KEY (PlaylistID, Platform),
    FOREIGN KEY (Platform) REFERENCES Platform(PlatformID)
);

CREATE TABLE IF NOT EXISTS Track (
    TrackID TEXT,
    Platform TEXT,
    Title TEXT,
    Owner TEXT,
    Thumbnail TEXT,  -- thumbnail endpoint with medium res
    DurationSeconds INTEGER,
    PRIMARY KEY (TrackID, Platform),
    FOREIGN KEY (Platform) REFERENCES Platform(PlatformID)
);

CREATE TABLE IF NOT EXISTS PlaylistTracks (
    PlaylistID TEXT,
    TrackID TEXT,
    Platform TEXT,
    Position INTEGER,
    PRIMARY KEY (PlaylistID, TrackID, Platform, Position),
    FOREIGN KEY (PlaylistID, Platform) REFERENCES Playlist(PlaylistID, Platform),
    FOREIGN KEY (TrackID, Platform) REFERENCES Track(TrackID, Platform)
);