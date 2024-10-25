import React, { useState } from 'react';
import { Button, Form, Input, Select } from '../styles';

const HOST_URL = "http://localhost:5000";

const Strategy = () => {
  const [ticker, setTicker] = useState('');
  const [country, setCountry] = useState('');
  const [strategyName, setStrategyName] = useState('');
  const [timePeriod, setTimePeriod] = useState('');
  const [timeInterval, setTimeInterval] = useState('');
  const [windowSlow, setWindowSlow] = useState('');
  const [windowFast, setWindowFast] = useState('');
  const [tradesData, setTradesData] = useState(null);
  const [resultsData, setResultsData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const addStrategyData = async () => {
    setLoading(true);
    setError(null);

    const url = `${HOST_URL}/strategy`;
    const payload = {
      code: ticker,
      country: country,
      strategy: strategyName,
      time_period: timePeriod,
      time_interval: timeInterval,
      window_slow: windowSlow,
      window_fast: windowFast
    };
  
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        setTradesData(null);
        setResultsData(null);
        setError(errorData.error || 'Unknown error occurred');
        return;
      }
      
      await response.json();
      fetchTradesData();
      fetchResultsData();
      
    } catch (err) {
      setTradesData(null);
      setResultsData(null);
      setError('Network error: ' + err.message);
    
    } finally {
      setLoading(false);
    
    }
  };
  
  const fetchTradesData = async () => {
    setLoading(true);
    setError(null);

    try {
      const url = `${HOST_URL}/trades/${ticker}`;
      const response = await fetch(url);

      if (!response.ok) {
        setError('Trade data not found');
        throw new Error('Trade data not found');
      }

      const data = await response.json();
      setTradesData(data);

    } catch (err) {
      setError(err.message);
    
    } finally {
      setLoading(false);
    
    }
  };
  
  const fetchResultsData = async () => {
    setLoading(true);
    setError(null);

    try {
      const url = `${HOST_URL}/results/${ticker}`;
      const response = await fetch(url);

      if (!response.ok) {
        setError('Results data not found');
        throw new Error('Results data not found');
      }

      const data = await response.json();
      setResultsData(data);

    } catch (err) {
      setError(err.message);
    
    } finally {
      setLoading(false);
    
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    addStrategyData();
  };
  
  return (
    <div>
      <h3>Strategy Tab</h3>
      
      <Form onSubmit={handleSubmit}>
        <Input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          placeholder="Ticker"
          required
        />

        <Select value={country} onChange={(e) => setCountry(e.target.value)}>
          <option value="">Select country</option>
          <option value="US">United States</option>
        </Select>

        <Select value={strategyName} onChange={(e) => setStrategyName(e.target.value)}>
          <option value="">Select strategy</option>
          <option value="MA">Moving Average</option>
          <option value="MACD">MACD</option>
          <option value="RSI">RSI</option>
          <option value="VW_MACD">Volume Weighted MACD</option>
        </Select>

        <Select value={timePeriod} onChange={(e) => setTimePeriod(e.target.value)}>
          <option value="">Select time period</option>
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
        </Select>

        <Select value={timeInterval} onChange={(e) => setTimeInterval(e.target.value)}>
          <option value="">Select time interval</option>
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
        </Select>

        <Input
          type="number"
          value={windowSlow}
          onChange={(e) => setWindowSlow(e.target.value)}
          placeholder="Set Slow Window"
          required
        />

        <Input
          type="number"
          value={windowFast}
          onChange={(e) => setWindowFast(e.target.value)}
          placeholder="Set Fast Window"
          required
        />

        <Button type="submit" disabled={loading}>Submit Strategy</Button>

      </Form>

      {error && <div style={{ color: 'red' }}>{error}</div>}

      {tradesData && (
        <div>
          <h4>Trades Data:</h4>
          {tradesData.results.map((trade, index) => (
            <div key={index}>
              <p>Date: {trade.date}</p>
              <p>Country: {trade.country}</p>
              <p>Close Price: {trade.close_price}</p>
              <p>Buy Signal: {trade.buy_signal}</p>
              <p>Buy Price: {trade.buy_price}</p>
              <p>Sell Signal: {trade.sell_signal}</p>
              <p>Sell Price: {trade.sell_price}</p>
            </div>
          ))}
        </div>
      )}

      {resultsData && (
        <div>
          <h4>Results Data:</h4>
          <p>Country: {resultsData.country}</p>
          <p>Total Profit: {resultsData.total_profit}</p>
          <p>Total Number of Trades: {resultsData.total_number_of_trades}</p>
          <p>Number of Profit Trades: {resultsData.number_profit_trades}</p>
          <p>Number of Loss Trades: {resultsData.number_loss_trades}</p>
          <p>Win Percentage: {resultsData.pct_win}</p>
          <p>Loss Percentage: {resultsData.pct_loss}</p>
          <p>Greatest Profit: {resultsData.greatest_profit}</p>
          <p>Greatest Loss: {resultsData.greatest_loss}</p>
        </div>
      )}
    </div>
  );
};

export default Strategy;
