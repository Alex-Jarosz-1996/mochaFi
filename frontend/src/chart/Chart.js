import React, { useState } from 'react';

const Chart = () => {
  const [ticker, setTicker] = useState('');
  const [timePeriod, setTimePeriod] = useState('1y');
  const [timeInterval, setTimeInterval] = useState('1d');

  return (
    <div>
      <div>
        <label>Ticker:</label>
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter")
                void(0)
          }}
        />
      </div>
      <div>
        <label>Time Period:</label>
        <select
          value={timePeriod}
          onChange={(e) => setTimePeriod(e.target.value)}
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
      <div>
        <label>Time Interval:</label>
        <select
          value={timeInterval}
          onChange={(e) => setTimeInterval(e.target.value)}
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
      <div>
        <button>Enter</button>
      </div>
        {/* <div>
          {isLoading ? (
            <div>Loading...</div>
          ) : chartData ? (
            <div>
              <h2>Fetched Data</h2>
              <pre>{JSON.stringify(chartData, null, 2)}</pre>
            </div>
          ) : (
            <div>No data to display</div>
          )}
      </div> */}
    </div>
  );
};

export default Chart;
