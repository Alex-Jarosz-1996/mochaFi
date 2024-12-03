import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Brush, Bar } from 'recharts';
import ReactECharts from 'echarts-for-react';
import { DesktopWrapper, Form, Input, Select, Button, Title, ButtonGroup, DeleteButton } from '../styles';
import { format } from 'date-fns';

const Chart = () => {
  const [ticker, setTicker] = useState('');
  const [timePeriod, setTimePeriod] = useState('');
  const [timeInterval, setTimeInterval] = useState('');
  const [country, setCountry] = useState('');
  const [stockData, setStockData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [chartType, setChartType] = useState('line');

  const fetchStockData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`/api/stock_price/${ticker}`);
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
      const response = await fetch('/api/stock_price', {
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
      await fetchStockData();
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
      const response = await fetch('/api/stock_price', {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Failed to delete stocks');
      }
      setStockData(null);
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

  const formatXAxisDate = (tickItem) => format(new Date(tickItem), 'MMM yy');

  const formatCandlestickData = () => {
    if (!stockData) return { dates: [], prices: [] };
    return {
      dates: stockData.prices.map((item) => item.date),
      prices: stockData.prices.map((item) => [item.open, item.close, item.low, item.high]),
    };
  };

  const renderCandlestickChart = () => {
    const formattedData = formatCandlestickData();
    const volumeData = stockData.prices.map((item) => ({
      value: item.volume,
      itemStyle: {
        color: item.close > item.open ? '#00da3c' : '#ec0000', // Green if close > open, Red if close < open
      },
    }));
  
    const option = {
      grid: [
        { // Grid for the candlestick chart
          left: '10%',
          right: '8%',
          height: '60%',
        },
        { // Grid for the volume chart
          left: '10%',
          right: '8%',
          top: '75%',
          height: '15%',
        },
      ],
      xAxis: [
        {
          type: 'category',
          data: formattedData.dates,
          gridIndex: 0, // candlestick chart
        },
        {
          type: 'category',
          data: formattedData.dates,
          gridIndex: 1, // volume chart
          axisLabel: { show: false }, // hide axis labels for volume chart
        },
      ],
      yAxis: [
        {
          scale: true,
          gridIndex: 0, // candlestick chart
        },
        {
          scale: true,
          gridIndex: 1, // volume chart
          axisLabel: { show: false }, // hide axis labels for volume chart
        },
      ],
      series: [
        {
          type: 'candlestick',
          data: formattedData.prices,
          itemStyle: {
            color: '#00da3c', // green -> bullish candle color
            color0: '#ec0000', // red -> bearish candle color
            borderColor: '#008F28',
            borderColor0: '#8A0000',
          },
        },
        {
          name: 'Volume',
          type: 'bar',
          xAxisIndex: 1,
          yAxisIndex: 1,
          data: volumeData,
        },
      ],
      tooltip: {
        trigger: 'axis', // show tooltip when hovering over axis points
        axisPointer: {
          type: 'shadow', // make the tooltip follow the bar
        },
        formatter: (params) => {
          const candlestick = params.find((p) => p.seriesType === 'candlestick');
          const volume = params.find((p) => p.seriesName === 'Volume');
  
          // Safely access both candlestick and volume data
          let tooltipText = '';
          if (candlestick) {
            tooltipText += `
              Date: ${candlestick.name}<br/>
              Open: ${candlestick.data[1]}<br/>
              Close: ${candlestick.data[0]}<br/>
              High: ${candlestick.data[3]}<br/>
              Low: ${candlestick.data[2]}<br/>
            `;
          }
          if (volume) {
            tooltipText += `Volume: ${volume.data.value.toLocaleString()}<br/>`;
          }
          return tooltipText;
        },
      },
      dataZoom: [
        {
          type: 'slider', // slider for zooming both charts
          xAxisIndex: [0, 1],
          start: 0,
          end: 100,
        },
        {
          type: 'inside', // allows zooming by dragging
          xAxisIndex: [0, 1],
          start: 0,
          end: 100,
        },
      ],
    };
  
    return <ReactECharts option={option} style={{ height: 400, width: '100%' }} />;
  };
  
  
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
          <option value="">Select country</option>
          <option value="US">United States</option>
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

        <ButtonGroup>
          <Button type="submit">Fetch Stock Data</Button>
          <DeleteButton type="button" onClick={deleteAllStocks}>
            Delete All Stocks
          </DeleteButton>
        </ButtonGroup>

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
                <Line type="monotone" dataKey="close" name="Close Price" stroke="#8884d8" dot={false} />
                <Bar dataKey="volume" fill="#82ca9d" />
                <Brush dataKey="date" height={30} stroke="#8884d8" />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            renderCandlestickChart()
          )}
        </div>
      )}
    </DesktopWrapper>
  );
};

export default Chart;
