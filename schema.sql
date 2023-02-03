CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name TEXT,
    time TEXT
);

CREATE TABLE participants (
    user_id INTEGER,
    course_id INTEGER
);
