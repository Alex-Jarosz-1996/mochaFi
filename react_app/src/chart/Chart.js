import React, { useState } from 'react';

const Chart = () => {
  const [ticker, setTicker] = useState('');
  const [timePeriod, setTimePeriod] = useState('1y');
  const [timeInterval, setTimeInterval] = useState('1d');
  const [chartData, setChartData] = useState(null);

  const backend_url = `http://localhost:5000/chart?ticker=${ticker}&time_period=${timePeriod}&time_interval=${timeInterval}`;

  const fetchData = async () => {
    try {
      const response = await fetch(backend_url);
      if (response.ok) {
        const data = await response.json();
        setChartData(data); // Assuming the response is JSON data
      } else {
        console.error('Failed to fetch data.');
      }
    } catch (error) {
      console.error('Error while fetching data:', error);
    }
  };
  
  const handleEnter = (e) => {
    fetchData();
  };
  
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
                handleEnter();
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
        <button onClick={handleEnter}>Enter</button>
      </div>
      <div>
        {chartData && (
          <div>
            <h2>Fetched Data</h2>
            <pre>{JSON.stringify(chartData, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default Chart;
