CREATE TABLE trades (
    id INTEGER PRIMARY KEY,
    code TEXT,
    country TEXT,
    date DATE,
    close_price REAL,
    buy_signal REAL,
    buy_price REAL,
    sell_signal REAL,
    sell_price REAL,
    UNIQUE (code, date) ON CONFLICT ABORT
);
