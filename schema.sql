CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE admins (
    username TEXT,
    user_id INTEGER
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    time TEXT
);

CREATE TABLE participants (
    user_id INTEGER,
    course_id INTEGER
);

CREATE TABLE issues (
    username TEXT,
    topic TEXT,
    issue TEXT
);

