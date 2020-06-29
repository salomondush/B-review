--This is created
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY NOT NULL,
    email TEXT NOT NULL, 
    hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY NOT NULL,
    isbn TEXT NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS reviews (
    user_id INTEGER REFERENCES users,
    rating INTEGER NOT NULL,
    review VARCHAR(100) NOT NULL,
    book_id INTEGER REFERENCES books
);

--might reference the last table book_id to books