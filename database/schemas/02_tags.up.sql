CREATE TABLE IF NOT EXISTS tags (
    tag VARCHAR(32),
    picture_id VARCHAR(36),
    confidence FLOAT,
    date TEXT,
    CONSTRAINT pk_tags PRIMARY KEY (tag, picture_id),
    CONSTRAINT fk_tags_pictures FOREIGN KEY (picture_id) REFERENCES pictures(id)
);
