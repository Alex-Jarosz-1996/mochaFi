CREATE TABLE stock_price_history (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    country TEXT,
    date DATE,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    adj_close_price REAL,
    volume INTEGER,
    UNIQUE (code, date) ON CONFLICT ABORT
);
