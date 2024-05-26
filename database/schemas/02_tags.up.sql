CREATE TABLE IF NOT EXISTS tags (
    tag VARCHAR(32) PRIMARY KEY,
    picture_id VARCHAR(36),
    confidence FLOAT,
    date TEXT,
    CONSTRAINT FK_TagPicture FOREIGN KEY (picture_id) REFERENCES pictures(id)
);
