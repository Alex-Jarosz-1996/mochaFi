import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Brush } from 'recharts';
import ReactECharts from 'echarts-for-react';
import { DesktopWrapper, Form, Input, Select, Button, Title, ButtonGroup, DeleteButton } from '../styles';
import { format } from 'date-fns';

const Chart = () => {
  const [ticker, setTicker] = useState('');
  const [timePeriod, setTimePeriod] = useState('1y');
  const [timeInterval, setTimeInterval] = useState('1d');
  const [country, setCountry] = useState('US');
  const [stockData, setStockData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [chartType, setChartType] = useState('line'); // State for toggling between chart types

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
      console.log(err.message);
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
        setStockData(null);
        throw new Error('Failed to add stock data');
      }
      await fetchStockData(); // Fetch the data after adding it
    } catch (err) {
      console.log(err.message);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const deleteAllStocks = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/stock_price_delete', {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Failed to delete stocks');
      }
      setStockData(null); // Clear the stock data after deletion
    } catch (err) {
      console.log(err.message);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    addStockData();
  };

  // Function to format the date as 'MMM yy', e.g., Jan 24, Feb 24
  const formatXAxisDate = (tickItem) => {
    return format(new Date(tickItem), 'MMM yy');
  };

  // Format stockData for ECharts candlestick chart
  const formatCandlestickData = () => {
    if (!stockData) return { dates: [], prices: [] };
    const formattedData = {
      dates: stockData.prices.map((item) => item.date),
      prices: stockData.prices.map((item) => [item.open, item.close, item.low, item.high]), // Candlestick format: [open, close, low, high]
    };
    return formattedData;
  };

  // Render the ECharts candlestick chart
  const renderCandlestickChart = () => {
    const formattedData = formatCandlestickData();
    const option = {
      title: {
        text: `Candlestick Chart for ${ticker}`,
      },
      xAxis: {
        type: 'category',
        data: formattedData.dates,
      },
      yAxis: {
        scale: true,
      },
      series: [
        {
          type: 'candlestick',
          data: formattedData.prices,
          itemStyle: {
            color: '#00da3c', // Bullish candle color
            color0: '#ec0000', // Bearish candle color
            borderColor: '#008F28',
            borderColor0: '#8A0000',
          },
        },
      ],
      dataZoom: [
        {
          type: 'slider', // Slider for zooming
          xAxisIndex: 0,  // Horizontal zooming
          start: 0,       // Default starting range
          end: 100,       // Default ending range
        },
        {
          type: 'inside', // Allows zooming by dragging
          xAxisIndex: 0,  // Horizontal zooming
          start: 0,
          end: 100,
        },
      ],
    };
  
    return <ReactECharts option={option} style={{ height: 400, width: '100%' }} />;
  };

  // Custom Tooltip to display close, high, low, and volume
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="custom-tooltip" style={{ backgroundColor: '#fff', padding: '10px', border: '1px solid #ccc' }}>
          <p className="label">{`Date: ${format(new Date(label), 'MMM dd, yyyy')}`}</p>
          <p>{`Close: $${data.close}`}</p>
          <p>{`High: $${data.high}`}</p>
          <p>{`Low: $${data.low}`}</p>
          <p>{`Volume: ${data.volume.toLocaleString()}`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <DesktopWrapper>
      <Title>Stock Price Chart</Title>
      <Form onSubmit={handleSubmit}>
        <Input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value.toUpperCase())}
          placeholder="Ticker"
          required
        />
        <Select value={country} onChange={(e) => setCountry(e.target.value)}>
          <option value="US">United States</option>
        </Select>
        <Select value={timePeriod} onChange={(e) => setTimePeriod(e.target.value)}>
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

        <ButtonGroup>
          <Button type="submit">Fetch Stock Data</Button>
          <DeleteButton type="button" onClick={deleteAllStocks}>
            Delete All Stocks
          </DeleteButton>
        </ButtonGroup>

        {/* Dropdown for selecting chart type */}
        <Select value={chartType} onChange={(e) => setChartType(e.target.value)}>
          <option value="line">Line Chart</option>
          <option value="candlestick">Candlestick Chart</option>
        </Select>
      </Form>

      {loading && <p>Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      {stockData && (
        <div className="mt-4">
          <h2 className="text-xl font-bold mb-2">Stock Price Chart for {stockData.code}</h2>
          {chartType === 'line' ? (
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={stockData.prices}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" tickFormatter={formatXAxisDate} />
                <YAxis label={{ value: '$', position: 'insideLeft' }} />
                <Tooltip content={<CustomTooltip />} />
                <Legend formatter={() => ''} />
                <Line type="monotone" dataKey="close" stroke="#8884d8" dot={false} />
                <Brush dataKey="date" height={30} stroke="#8884d8" />
              </LineChart>
            </ResponsiveContainer>
                      ) : (
            renderCandlestickChart() // Render candlestick chart if selected
          )}
        </div>
      )}
    </DesktopWrapper>
  );
};

export default Chart;
