-- Это я сгенерировал нейросетью 😉


\c authors_database

INSERT INTO users (email, login) VALUES
    ('alice@dev.com', 'alice'),
    ('bob@writer.com', 'bob'),
    ('carol@tech.com', 'carol'),
    ('dan@coder.com', 'dan');

INSERT INTO blog (owner_id, name, description) VALUES
    (1, 'Alice Tech', 'coding tips'),
    (2, 'Bob Writes', 'daily thoughts'),
    (3, 'Carol Codes', 'dev journey'),
    (1, 'Alice Life', 'personal blog');

INSERT INTO post (header, text, author_id, blog_id) VALUES
    ('Learning SQL', 'im feeling good today', 1, 1),
    ('Python Tips', 'love coding daily', 1, 1),
    ('Morning Coffee', 'amazing start today', 2, 2),
    ('Weekend Vibes', 'relaxing mode on', 2, 2),
    ('New Framework', 'excited to learn', 3, 3),
    ('Debugging Life', 'bugs everywhere', 3, 3),
    ('Sunday Mood', 'lazy day today', 1, 4);

INSERT INTO comment (commentator_id, post_id, text) VALUES
    (2, 1, 'great post'),
    (3, 1, 'very helpful'),
    (4, 1, 'thanks'),
    (1, 3, 'nice'),
    (1, 3, 'cool'),
    (3, 3, 'love it'),
    (4, 3, 'same here'),
    (1, 5, 'cool'),
    (1, 5, 'same'),
    (2, 5, 'interesting'),
    (4, 5, 'wow'),
    (1, 6, 'relatable'),
    (2, 6, 'haha'),
    (2, 6, 'literally me'),
    (3, 7, 'enjoy'),
    (4, 2, 'awesome'),
    (2, 4, 'great post'),
    (2, 4, 'mood'),
    (1, 4, 'yes');