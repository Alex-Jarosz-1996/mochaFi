import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { StyledContainer } from '../styles';

const metricCategories = {
  "Basic Info": ["code", "country", "price", "marketCap", "numSharesAvail"],
  "Price Metrics": ["yearlyLowPrice", "yearlyHighPrice", "fiftyDayMA", "twoHundredDayMA"],
  "Valuation Ratios": ["acquirersMultiple", "currentRatio", "enterpriseValue", "eps", "evToEBITDA", "evToRev", "peRatioTrail", "peRatioForward", "priceToSales", "priceToBook"],
  "Dividend Info": ["dividendYield", "dividendRate", "exDivDate", "payoutRatio"],
  "Financial Metrics": ["bookValPerShare", "cash", "cashPerShare", "cashToMarketCap", "cashToDebt", "debt", "debtToMarketCap", "debtToEquityRatio", "returnOnAssets", "returnOnEquity"],
  "Income Statement": ["ebitda", "ebitdaPerShare", "earningsGrowth", "grossProfit", "grossProfitPerShare", "netIncome", "netIncomePerShare", "operatingMargin", "profitMargin", "revenue", "revenueGrowth", "revenuePerShare"],
  "Cash Flow": ["fcf", "fcfToMarketCap", "fcfPerShare", "fcfToEV", "ocf", "ocfToRevenueRatio", "ocfToMarketCap", "ocfPerShare", "ocfToEV"]
};

const Stats = () => {
  const [stock, setStock] = useState('');
  const [country, setCountry] = useState('');
  const [countries] = useState(['AUS', 'US']);
  const [stocks, setStocks] = useState([]);
  const [visibleMetrics, setVisibleMetrics] = useState(() => {
    const allMetrics = Object.values(metricCategories).flat();
    return allMetrics.reduce((acc, metric) => ({
      ...acc,
      [metric]: ['code', 'country', 'price'].includes(metric)
    }), {});
  });

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

  const toggleMetric = (metric) => {
    setVisibleMetrics(prev => ({...prev, [metric]: !prev[metric]}));
  };

  const toggleCategory = (category) => {
    const categoryMetrics = metricCategories[category];
    const areAllVisible = categoryMetrics.every(metric => visibleMetrics[metric]);
    setVisibleMetrics(prev => {
      const newState = {...prev};
      categoryMetrics.forEach(metric => {
        newState[metric] = !areAllVisible;
      });
      return newState;
    });
  };

  const formatNumber = (num) => {
    if (num === null || num === undefined) return 'N/A';
    return num.toLocaleString(undefined, { maximumFractionDigits: 2 });
  };

  const formatPercentage = (num) => {
    if (num === null || num === undefined) return 'N/A';
    return `${(num * 100).toFixed(2)}%`;
  };

  return (
    <StyledContainer>
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

      <div style={{ marginBottom: '20px' }}>
        <h4>Toggle Metrics:</h4>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
          {Object.entries(metricCategories).map(([category, metrics]) => (
            <div key={category} style={{ border: '1px solid #ddd', padding: '10px', borderRadius: '5px', minWidth: '200px', flex: '1' }}>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                <input
                  type="checkbox"
                  id={`category-${category}`}
                  checked={metrics.every(metric => visibleMetrics[metric])}
                  onChange={() => toggleCategory(category)}
                  style={{ marginRight: '5px' }}
                />
                <label htmlFor={`category-${category}`} style={{ fontSize: '1em', fontWeight: 'bold', cursor: 'pointer' }}>
                  {category}
                </label>
              </div>
              <div style={{ maxHeight: '150px', overflowY: 'auto' }}>
                {metrics.map(metric => (
                  <div key={metric} style={{ display: 'flex', alignItems: 'center', marginBottom: '5px' }}>
                    <input
                      type="checkbox"
                      id={metric}
                      checked={visibleMetrics[metric]}
                      onChange={() => toggleMetric(metric)}
                      style={{ marginRight: '5px' }}
                    />
                    <label htmlFor={metric} style={{ fontSize: '0.9em', cursor: 'pointer' }}>
                      {metric.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                    </label>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <h3>Saved Stocks</h3>

      <div style={{overflowX: 'auto'}}>
        <table>
          <thead>
            <tr>
              {Object.entries(visibleMetrics).map(([metric, isVisible]) => (
                isVisible && <th key={metric}>{metric.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</th>
              ))}
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {stocks.map((stock) => (
              <tr key={stock.id}>
                {Object.entries(visibleMetrics).map(([metric, isVisible]) => (
                  isVisible && (
                  <td key={metric}>
                    {metric === 'exDivDate' ? (stock[metric] || 'N/A') :
                    ['dividendYield', 'payoutRatio', 'cashToMarketCap', 'debtToMarketCap', 
                      'debtToEquityRatio', 'returnOnAssets', 'returnOnEquity', 'earningsGrowth', 
                      'operatingMargin', 'profitMargin', 'revenueGrowth', 'ocfToRevenueRatio'].includes(metric) 
                      ? formatPercentage(stock[metric]) :
                    ['price', 'marketCap', 'yearlyLowPrice', 'yearlyHighPrice', 'fiftyDayMA', 
                      'twoHundredDayMA', 'enterpriseValue', 'eps', 'dividendRate', 'bookValPerShare', 
                      'cash', 'cashPerShare', 'debt', 'ebitda', 'ebitdaPerShare', 'grossProfit', 
                      'grossProfitPerShare', 'netIncome', 'netIncomePerShare', 'revenue', 'revenuePerShare', 
                      'fcf', 'fcfToMarketCap', 'fcfPerShare', 'ocf', 'ocfToMarketCap', 'ocfPerShare'].includes(metric) 
                      ? (stock[metric] !== null && stock[metric] !== undefined ? `$${formatNumber(stock[metric])}` : 'N/A') :
                    formatNumber(stock[metric])}
                  </td>
                  )
                ))}
                <td>
                  <button onClick={() => handleDelete(stock.id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
    </StyledContainer>
    
  );
};

export default Stats;