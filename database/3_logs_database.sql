\c logs_database

CREATE TABLE space_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE event_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    space_type_id INTEGER NOT NULL,
    event_type_id INTEGER NOT NULL,
    FOREIGN KEY (space_type_id) REFERENCES space_type(id),
    FOREIGN KEY (event_type_id) REFERENCES event_type(id)
);

INSERT INTO space_type (name) VALUES 
    ('global'),
    ('blog'),
    ('post');

INSERT INTO event_type (name) VALUES 
    ('login'),
    ('comment'),
    ('create_post'),
    ('delete_post'),
    ('logout');
