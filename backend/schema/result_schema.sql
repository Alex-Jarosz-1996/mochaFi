CREATE TABLE results (
    id INTEGER PRIMARY KEY,
    code TEXT,
    country TEXT,
    initial_investment REAL,
    buy_sell_pairs_timestamp JSON,
    profit_loss_shares JSON,
    strategy_roi REAL,
    total_profit REAL,
    total_profit_per_trade JSON,
    total_number_of_trades INTEGER,
    number_profit_trades INTEGER,
    number_loss_trades INTEGER,
    pct_win REAL,
    pct_loss REAL,
    greatest_profit REAL,
    greatest_loss REAL,
    UNIQUE (code) ON CONFLICT ABORT
);
