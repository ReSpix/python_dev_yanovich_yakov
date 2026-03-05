\c authors_database

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR,
    login VARCHAR NOT NULL
);

CREATE TABLE blog (
    id SERIAL PRIMARY KEY,
    owner_id INT NOT NULL,
    name VARCHAR NOT NULL,
    description VARCHAR,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

CREATE TABLE post (
    id SERIAL PRIMARY KEY,
    header VARCHAR,
    text VARCHAR NOT NULL,
    author_id INT NOT NULL,
    blog_id INT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES users(id),
    FOREIGN KEY (blog_id) REFERENCES blog(id)
);

CREATE TABLE comment (
    id SERIAL PRIMARY KEY,
    commentator_id INT NOT NULL,
    post_id INT NOT NULL,
    text VARCHAR NOT NULL,
    FOREIGN KEY (commentator_id) REFERENCES users(id),
    FOREIGN KEY (post_id) REFERENCES post(id)
);
