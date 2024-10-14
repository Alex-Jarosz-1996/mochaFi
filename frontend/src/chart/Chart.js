import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Chart = () => {
  const [ticker, setTicker] = useState('');
  const [timePeriod, setTimePeriod] = useState('1y');
  const [timeInterval, setTimeInterval] = useState('1d');
  const [country, setCountry] = useState('US');
  const [stockData, setStockData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchStockData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`/stock_price/${ticker}`);
      if (!response.ok) {
        throw new Error('Stock data not found');
      }
      const data = await response.json();
      setStockData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const addStockData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/stock_price', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: ticker,
          country,
          time_period: timePeriod,
          time_interval: timeInterval,
        }),
      });
      if (!response.ok) {
        throw new Error('Failed to add stock data');
      }
      await fetchStockData(); // Fetch the data after adding it
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    addStockData();
  };

  return (
    <div className="p-4">
      <form onSubmit={handleSubmit} className="mb-4">
        <div className="mb-2">
          <label className="block">Ticker:</label>
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value.toUpperCase())}
            className="border p-1"
            required
          />
        </div>
        <div className="mb-2">
          <label className="block">Country:</label>
          <select
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            className="border p-1"
          >
            <option value="US">United States</option>
          </select>
        </div>
        <div className="mb-2">
          <label className="block">Time Period:</label>
          <select
            value={timePeriod}
            onChange={(e) => setTimePeriod(e.target.value)}
            className="border p-1"
          >
            <option value="1d">1 Day</option>
            <option value="5d">5 Days</option>
            <option value="1mo">1 Month</option>
            <option value="3mo">3 Months</option>
            <option value="6mo">6 Months</option>
            <option value="ytd">Year to Date</option>
            <option value="1y">1 Year</option>
            <option value="2y">2 Years</option>
            <option value="5y">5 Years</option>
            <option value="10y">10 Years</option>
            <option value="max">Max</option>
          </select>
        </div>
        <div className="mb-2">
          <label className="block">Time Interval:</label>
          <select
            value={timeInterval}
            onChange={(e) => setTimeInterval(e.target.value)}
            className="border p-1"
          >
            <option value="1m">1 Minute</option>
            <option value="2m">2 Minutes</option>
            <option value="5m">5 Minutes</option>
            <option value="15m">15 Minutes</option>
            <option value="30m">30 Minutes</option>
            <option value="60m">60 Minutes</option>
            <option value="90m">90 Minutes</option>
            <option value="1h">1 Hour</option>
            <option value="1d">1 Day</option>
            <option value="5d">5 Days</option>
            <option value="1wk">1 Week</option>
            <option value="1mo">1 Month</option>
            <option value="3mo">3 Months</option>
          </select>
        </div>
        <button type="submit" className="bg-blue-500 text-white p-2 rounded">
          Fetch Stock Data
        </button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {stockData && (
        <div className="mt-4">
          <h2 className="text-xl font-bold mb-2">Stock Price Chart for {stockData.code}</h2>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={stockData.prices}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="close" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default Chart;