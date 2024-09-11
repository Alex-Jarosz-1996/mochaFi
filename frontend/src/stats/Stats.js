import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Stats = () => {
  const [stock, setStock] = useState('');
  const [country, setCountry] = useState('');
  const [countries] = useState(['AUS', 'US']);
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    fetchStocks();
  }, []);

  const fetchStocks = async () => {
    try {
      const response = await axios.get('http://localhost:5000/stocks');
      setStocks(response.data);
    } catch (error) {
      console.error('Error fetching stocks:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/stock', { stock, country });
      setStock('');
      setCountry('');
      fetchStocks();
    } catch (error) {
      console.error('Error adding stock:', error);
    }
  };

  const handleDelete = async (stockId) => {
    try {
      await axios.delete(`http://localhost:5000/stock/${stockId}`);
      fetchStocks();
    } catch (error) {
      console.error('Error deleting stock:', error);
    }
  };

  const formatNumber = (num) => {
    return num ? num.toLocaleString(undefined, { maximumFractionDigits: 2 }) : 'N/A';
  };

  const formatPercentage = (num) => {
    return num ? `${(num * 100).toFixed(2)}%` : 'N/A';
  };

  return (
    <div>
      <h2>Stock Selector</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={stock}
          onChange={(e) => setStock(e.target.value)}
          placeholder="Enter stock symbol"
          required
        />
        <select
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          required
        >
        <option value="">Select a country</option>
        {countries.map((c) => (
          <option key={c} value={c}>
            {c}
          </option>
        ))}
        </select>
        <button type="submit">Add Stock</button>
      </form>
      <h3>Saved Stocks</h3>
      <div style={{overflowX: 'auto'}}>
        <table>
          <thead>
            <tr>
              <th>Code</th>
              <th>Country</th>
              <th>Price</th>
              <th>Market Cap</th>
              <th>Shares Available</th>
              <th>Yearly Low</th>
              <th>Yearly High</th>
              <th>50 Day MA</th>
              <th>200 Day MA</th>
              <th>Acquirers Multiple</th>
              <th>Current Ratio</th>
              <th>Enterprise Value</th>
              <th>EPS</th>
              <th>EV/EBITDA</th>
              <th>EV/Rev</th>
              <th>P/E (Trail)</th>
              <th>P/E (Forward)</th>
              <th>Price to Sales</th>
              <th>Price to Book</th>
              <th>Dividend Yield</th>
              <th>Dividend Rate</th>
              <th>Ex-Dividend Date</th>
              <th>Payout Ratio</th>
              <th>Book Value per Share</th>
              <th>Cash</th>
              <th>Casper per Share</th>
              <th>Cash to Market Cap</th>
              <th>Cash to Debt</th>
              <th>Debt</th>
              <th>Debt to Market Cap</th>
              <th>Debt to Equity Ratio</th>
              <th>Return on Assets</th>
              <th>Return on Equity</th>
              <th>EBITDA</th>
              <th>EBITDA per Share</th>
              <th>Earnings Growth</th>
              <th>Gross Profit</th>
              <th>Gross Profit per Share</th>
              <th>Net Income</th>
              <th>Net Income per Share</th>
              <th>Operating Margin</th>
              <th>Profit Margin</th>
              <th>Revenue</th>
              <th>Revenue Growth</th>
              <th>Revenue per Share</th>
              <th>Free Cash Flow</th>
              <th>Free Cash Flow to Market Cap</th>
              <th>Free Cash Flow per Share</th>
              <th>Free Cash Flow to Enterprise Value</th>
              <th>Operating Cash Flow</th>
              <th>Operating Cash Flow to Revenue Ratio</th>
              <th>Operating Cash Flow to Market Cap</th>
              <th>Operating Cash Flow per Share</th>
              <th>Operating Cash Flow to Enterprise Value</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {stocks.map((stock) => (
              <tr key={stock.id}>
                <td>{stock.code}</td>
                <td>{stock.country}</td>
                <td>${formatNumber(stock.price)}</td>
                <td>${formatNumber(stock.marketCap)}</td>
                <td>{formatNumber(stock.numSharesAvail)}</td>
                <td>${formatNumber(stock.yearlyLowPrice)}</td>
                <td>${formatNumber(stock.yearlyHighPrice)}</td>
                <td>${formatNumber(stock.fiftyDayMA)}</td>
                <td>${formatNumber(stock.twoHundredDayMA)}</td>
                <td>{formatNumber(stock.acquirersMultiple)}</td>
                <td>{formatNumber(stock.currentRatio)}</td>
                <td>${formatNumber(stock.enterpriseValue)}</td>
                <td>${formatNumber(stock.eps)}</td>
                <td>{formatNumber(stock.evToEBITDA)}</td>
                <td>{formatNumber(stock.evToRev)}</td>
                <td>{formatNumber(stock.peRatioTrail)}</td>
                <td>{formatNumber(stock.peRatioForward)}</td>
                <td>{formatNumber(stock.priceToSales)}</td>
                <td>{formatNumber(stock.priceToBook)}</td>
                <td>{formatPercentage(stock.dividendYield)}</td>
                <td>${formatNumber(stock.dividendRate)}</td>
                <td>{stock.exDivDate || 'N/A'}</td>
                <td>{formatPercentage(stock.payoutRatio)}</td>
                <td>${formatNumber(stock.bookValPerShare)}</td>
                <td>${formatNumber(stock.cash)}</td>
                <td>${formatNumber(stock.cashPerShare)}</td>
                <td>{formatPercentage(stock.cashToMarketCap)}</td>
                <td>{formatNumber(stock.cashToDebt)}</td>
                <td>${formatNumber(stock.debt)}</td>
                <td>{formatPercentage(stock.debtToMarketCap)}</td>
                <td>{formatPercentage(stock.debtToEquityRatio)}</td>
                <td>{formatPercentage(stock.returnOnAssets)}</td>
                <td>{formatPercentage(stock.returnOnEquity)}</td>
                <td>{formatNumber(stock.ebitda)}</td>
                <td>{formatNumber(stock.ebitdaPerShare)}</td>
                <td>{formatPercentage(stock.earningsGrowth)}</td>
                <td>{formatNumber(stock.grossProfit)}</td>
                <td>{formatNumber(stock.grossProfitPerShare)}</td>
                <td>{formatNumber(stock.netIncome)}</td>
                <td>{formatNumber(stock.netIncomePerShare)}</td>
                <td>{formatPercentage(stock.operatingMargin)}</td>
                <td>{formatPercentage(stock.profitMargin)}</td>
                <td>{formatNumber(stock.revenue)}</td>
                <td>{formatPercentage(stock.revenueGrowth)}</td>
                <td>{formatNumber(stock.revenuePerShare)}</td>
                <td>{formatNumber(stock.fcf)}</td>
                <td>{formatNumber(stock.fcfToMarketCap)}</td>
                <td>{formatNumber(stock.fcfPerShare)}</td>
                <td>{formatNumber(stock.fcfToEV)}</td>
                <td>{formatNumber(stock.ocf)}</td>
                <td>{formatPercentage(stock.ocfToRevenueRatio)}</td>
                <td>{formatNumber(stock.ocfToMarketCap)}</td>
                <td>{formatNumber(stock.ocfPerShare)}</td>
                <td>{formatNumber(stock.ocfToEV)}</td>
                <td>
                  <button onClick={() => handleDelete(stock.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Stats;