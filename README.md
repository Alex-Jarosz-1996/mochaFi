# mochaFi
**DISCLAIMER: MOCHAFI DOES NOT ASSUME THAT FINANCIAL DATA IS CURRENT AND ACCURATE. IT IS INTENDED FOR PERSONAL USE ONLY.**

mochaFi is a project which utilises the python [yfinance](https://pypi.org/project/yfinance/) codebase to extract financial data of US companies.
mochaFi performs the following functionalities:
### stats
stats displays financial information on the company.

### chart
chart plots the stock chart of the company using a ***Line Chart*** or a ***Candlestick Chart***

### strategy
strategy allows you to compare the performance of different strategies over a defined time period.
Current strategies are:
1. Moving Average
2. MACD
3. RSI
4. Volume Weighted MACD

## Usage
To use project:
1. Clone the repo
```bash
git clone <repo>
```

2. Build the project with docker
```bash
docker compose build
```

3. Run the project with docker
```bash
docker compose up
```

4. The mochaFi project should now be running on **http://localhost:3000/stats**
