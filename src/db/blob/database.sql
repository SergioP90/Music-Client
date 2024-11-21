-- Artist Table: Stores the artists detected in the audio files
CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Albums Table: Stores the albums detected in the audio files
CREATE TABLE IF NOT EXISTS albums (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for the album
    name TEXT NOT NULL,  -- Name to identify the album
    artist TEXT NOT NULL,  -- Name of the artist who created the album
    FOREIGN KEY (artistID) REFERENCES artists(ID)
);

-- Songs Table: Stores the songs detected in blob storage
CREATE TABLE IF NOT EXISTS songs {
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for the song
    name TEXT NOT NULL,  -- Name to identify the song
    artistID INTEGER NOT NULL,  -- ID of the artist who created the song
    albumID INTEGER NOT NULL,  -- ID of the album the song belongs to
    duration INTEGER NOT NULL,  -- Duration of the song in seconds
    creationDate DATETIME NOT NULL,  -- Date the song was created
    FOREIGN KEY (artistID) REFERENCES artists(ID),
    FOREIGN KEY (albumID) REFERENCES albums(ID)
};

-- Playlists Table: Stores the playlists created by the user
CREATE TABLE IF NOT EXISTS playlists {
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for the playlist
    name TEXT NOT NULL  -- Name to identify the playlist
};

-- PlaylistSongs Table: Stores the songs associated with each playlist
CREATE TABLE IF NOT EXISTS playlistSongs {
    playlistID INTEGER NOT NULL,  -- ID of the playlist
    songID INTEGER NOT NULL,  -- ID of the song
    PRIMARY KEY (playlistID, songID) REFERENCES playlists(ID, songID),
    FOREIGN KEY (playlistID) REFERENCES playlists(ID),
    FOREIGN KEY (songID) REFERENCES songs(ID)
};
