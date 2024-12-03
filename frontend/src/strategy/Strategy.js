import React, { useState } from 'react';
import { Button, Form, Input, Select, DeleteButton, ButtonGroup } from '../styles';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Brush, Bar, ReferenceDot } from 'recharts';
import { format } from 'date-fns';

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
      const response = await fetch("/api/strategy", {
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
      const response = await fetch(`/api/strategy/trades/${ticker}`);

      if (!response.ok) {
        setError('Trade data not found');
        throw new Error('Trade data not found');
      }

      const data = await response.json();
      console.log("Fetching Trades Data");
      console.log(data);
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
      const response = await fetch(`/api/strategy/results/${ticker}`);

      if (!response.ok) {
        setError('Results data not found');
        throw new Error('Results data not found');
      }

      const data = await response.json();
      console.log("Fetching Results Data");
      console.log(data);
      setResultsData(data);

    } catch (err) {
      setError(err.message);
    
    } finally {
      setLoading(false);
    
    }
  };

  const deleteStrategy = async (stock) => {
    setError(null);
    try {
      const response = await fetch(`/api/strategy/${stock}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to remove strategy');
      }

    } catch (err) {
      console.log(err.message);
      setError(err.message);

    } finally {
      setTradesData(null);
      setResultsData(null);
    }
  };
  
  // Consolidate and align dates
  const consolidateDates = () => {
    const tradesDates = tradesData?.results?.map((trade) => trade.date) || [];
    const buySellDates = resultsData?.buy_sell_pairs_timestamp?.flatMap((pair) => [pair[0], pair[2]]) || [];
    const profitLossDates = resultsData?.profit_loss_shares?.map((entry) => entry[0]) || [];

    // Combine, deduplicate, and sort all dates
    const allDates = [...new Set([...tradesDates, ...buySellDates, ...profitLossDates])];
    allDates.sort((a, b) => new Date(a) - new Date(b));

    return allDates;
  };

  // Align data using the consolidated dates
  const alignDataWithDates = (allDates) => {
    let cumulativeInvestment = resultsData?.initial_investment || 0;
    let alignedGrowthData = [];
    
    allDates.forEach((date) => {
      const profitLoss = resultsData?.profit_loss_shares?.find(([d]) => d === date);
      if (profitLoss) {
        cumulativeInvestment += profitLoss[1];
      }
      alignedGrowthData.push({ date, value: cumulativeInvestment });
    });

    return alignedGrowthData;
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    addStrategyData();
  };

  const formatXAxisDate = (tickItem) => format(new Date(tickItem), 'MMM dd, yyyy');

  const renderLineChart = () => (
    <ResponsiveContainer width="100%" height={400}>
      <h4>{`Buy / Sell Chart for ${ticker}.`}</h4>
      <LineChart data={tradesData?.results || []}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" tickFormatter={formatXAxisDate} />
        <YAxis label={{ value: '$', position: 'insideLeft' }} />
        <Tooltip formatter={(value) => `$${value}`} labelFormatter={(label) => formatXAxisDate(label)} />
        <Legend />
        <Line type="monotone" dataKey="close_price" name="Close Price" stroke="#8884d8" dot={false} />
        <Bar dataKey="volume" fill="#82ca9d" />
        <Brush dataKey="date" height={30} stroke="#8884d8" />

        {resultsData?.buy_sell_pairs_timestamp?.map((trade, index) => {
          const [buyDate, buyPrice, sellDate, sellPrice] = trade;
          const isProfitable = sellPrice > buyPrice;
          const arrowColour = isProfitable ? '#00b300' : '#ff4d4f';

          return (
            <React.Fragment key={index}>
              <ReferenceDot
                x={buyDate}
                y={buyPrice}
                r={8}
                fill={arrowColour}
                stroke={arrowColour}
                label={{
                  value: '↑',
                  position: 'top',
                  fill: arrowColour,
                  fontSize: 16,
                  fontWeight: 'bold',
                }}
              />
              <ReferenceDot
                x={sellDate}
                y={sellPrice}
                r={8}
                fill={arrowColour}
                stroke={arrowColour}
                label={{
                  value: '↓',
                  position: 'bottom',
                  fill: arrowColour,
                  fontSize: 16,
                  fontWeight: 'bold',
                }}
              />
            </React.Fragment>
          );
        })}
      </LineChart>
    </ResponsiveContainer>
  );
  
  const allDates = consolidateDates();
  const alignedGrowthData = alignDataWithDates(allDates);
  
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

        <ButtonGroup>
          <Button type="submit" disabled={loading}>Submit Strategy</Button>
          <Button
            type="button"
            onClick={() => deleteStrategy(ticker)}
            style={{
              backgroundColor: '#ff4d4f',
              color: 'white',
              padding: '',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
              marginLeft: '5px'
            }}
          >
            Delete Strategy
          </Button>
        </ButtonGroup>

      </Form>

      {error && <div style={{ color: 'red' }}>{error}</div>}

      {tradesData && resultsData && (
        <div>
          {renderLineChart()}
        </div>
      )}

      {resultsData && alignedGrowthData.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <h4>{`Capital growth for ${ticker} using strategy ${strategyName} with an initial investment of $${resultsData.initial_investment}.`}</h4>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={alignedGrowthData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" tickFormatter={formatXAxisDate} />
              <YAxis label={{ value: 'Investment Value ($)', angle: -90, position: 'insideLeft' }} />
              <Tooltip formatter={(value) => `$${value.toFixed(2)}`} labelFormatter={formatXAxisDate} />
              <Line type="linear" dataKey="value" stroke="#8884d8" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {tradesData && resultsData && (
        <div
          style={{
            border: '1px solid #ddd',
            borderRadius: '8px',
            padding: '20px',
            backgroundColor: '#ffffff',
            marginTop: '20px',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
          }}
        >
          <h4
            style={{
              marginBottom: '20px',
              fontSize: '1.5rem',
              color: '#333',
              borderBottom: '1px solid #ddd',
              paddingBottom: '10px',
            }}
          >
            Results Data
          </h4>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '16px',
              rowGap: '20px',
              paddingBottom: '10px',
            }}
          >
            <div>
              <strong>Country Code:</strong> {resultsData.code.toUpperCase()}
            </div>
            <div>
              <strong>Country:</strong> {resultsData.country.toUpperCase()}
            </div>
            <div>
              <strong>Total Profit:</strong>{' '}
              <span style={{ color: resultsData.total_profit >= 0 ? '#00b300' : '#ff4d4f' }}>
                ${resultsData.total_profit}
              </span>
            </div>
            <div>
              <strong>Total Trades:</strong> {resultsData.total_number_of_trades}
            </div>
            <div>
              <strong>Profit Trades:</strong> {resultsData.number_profit_trades}
            </div>
            <div>
              <strong>Loss Trades:</strong> {resultsData.number_loss_trades}
            </div>
            <div>
              <strong>Win Percentage:</strong>{' '}
              <span style={{ color: '#00b300' }}>
                {resultsData.pct_win}%
              </span>
            </div>
            <div>
              <strong>Loss Percentage:</strong>{' '}
              <span style={{ color: '#ff4d4f' }}>
                {resultsData.pct_loss}%
              </span>
            </div>
            <div>
              <strong>Greatest Profit:</strong>{' '}
              <span style={{ color: '#00b300' }}>
                ${resultsData.greatest_profit}
              </span>
            </div>
            <div>
              <strong>Greatest Loss:</strong>{' '}
              <span style={{ color: '#ff4d4f' }}>
                ${resultsData.greatest_loss}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Strategy;
