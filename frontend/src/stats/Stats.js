import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Button,
  ButtonGroup, 
  CategoryBox,
  CategoryContainer,
  CategoryTitle,
  DeleteAllButton,
  DeleteButton,
  Form, 
  Input,
  MetricLabel, 
  Select, 
  Table,
  Td,
  Th,
  Title,
  ToggleTitle,
  ToggleSection,
  DesktopWrapper
} from '../styles';

const HOST_URL = "http://localhost:5000";

const metricCategories = {
  "Basic Info": ["code", "country", "price", "marketCap", "numSharesAvail"],
  "Price Metrics": ["yearlyLowPrice", "yearlyHighPrice", "fiftyDayMA", "twoHundredDayMA"],
  "Valuation Ratios": ["acquirersMultiple", "currentRatio", "enterpriseValue", "eps", "evToEBITDA", "evToRev", "peRatioTrail", "peRatioForward", "priceToSales", "priceToBook"],
  "Dividend Info": ["dividendYield", "dividendRate", "exDivDate", "payoutRatio"],
  "Financial Metrics": ["bookValPerShare", "cash", "cashPerShare", "cashToMarketCap", "cashToDebt", "debt", "debtToMarketCap", "debtToEquityRatio", "returnOnAssets", "returnOnEquity"],
  "Income Statement": ["ebitda", "ebitdaPerShare", "earningsGrowth", "grossProfit", "grossProfitPerShare", "netIncome", "netIncomePerShare", "operatingMargin", "profitMargin", "revenue", "revenueGrowth", "revenuePerShare"],
  "Cash Flow": ["fcf", "fcfToMarketCap", "fcfPerShare", "fcfToEV", "ocf", "ocfToRevenueRatio", "ocfToMarketCap", "ocfPerShare", "ocfToEV"]
};

const metricDisplayNames = {
  acquirersMultiple: "Acquirers Multiple",
  bookValPerShare: "Book Value per Share",
  cash: "Cash",
  cashPerShare: "Cash per Share",
  cashToDebt: "Cash to Debt",
  cashToMarketCap: "Cash to Market Cap",
  code: "Code",
  country: "Country",
  currentRatio: "Current Ratio",
  debt: "Debt",
  debtToEquityRatio: "Debt to Equity",
  debtToMarketCap: "Debt to Market Cap",
  dividendRate: "Dividend Rate",
  dividendYield: "Dividend Yield",
  earningsGrowth: "Earnings Growth",
  ebitda: "EBITDA",
  ebitdaPerShare: "EBITDA per Share",
  enterpriseValue: "Enterprise Value",
  eps: "EPS",
  evToEBITDA: "EV/EBITDA",
  evToRev: "EV/Revenue",
  exDivDate: "Ex-Dividend Date",
  fcf: "Free Cash Flow",
  fcfPerShare: "FCF per Share",
  fcfToEV: "FCF to EV",
  fcfToMarketCap: "FCF to Market Cap",
  fiftyDayMA: "50 Day MA",
  grossProfit: "Gross Profit",
  grossProfitPerShare: "Gross Profit per Share",
  marketCap: "Market Cap",
  netIncome: "Net Income",
  netIncomePerShare: "Net Income per Share",
  numSharesAvail: "Shares Available",
  ocf: "Operating Cash Flow",
  ocfPerShare: "OCF per Share",
  ocfToEV: "OCF to EV",
  ocfToMarketCap: "OCF to Market Cap",
  ocfToRevenueRatio: "OCF to Revenue",
  operatingMargin: "Operating Margin",
  payoutRatio: "Payout Ratio",
  peRatioForward: "P/E (Forward)",
  peRatioTrail: "P/E (Trailing)",
  price: "Price",
  priceToBook: "Price to Book",
  priceToSales: "Price to Sales",
  profitMargin: "Profit Margin",
  returnOnAssets: "Return on Assets",
  returnOnEquity: "Return on Equity",
  revenue: "Revenue",
  revenueGrowth: "Revenue Growth",
  revenuePerShare: "Revenue per Share",
  twoHundredDayMA: "200 Day MA",
  yearlyHighPrice: "Yearly High",
  yearlyLowPrice: "Yearly Low",
};

const Stats = () => {
  const [stock, setStock] = useState('');
  const [country, setCountry] = useState('');
  const [countries] = useState(['US']); // NOTE: add 'AUS' when have access to more secure data
  const [stocks, setStocks] = useState([]);
  const [sortColumn, setSortColumn] = useState('');
  const [sortDirection, setSortDirection] = useState('asc');
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
      const response = await axios.get(`${HOST_URL}/stocks`);
      setStocks(response.data);
    } catch (error) {
      console.error('Error fetching stocks:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${HOST_URL}/stock`, { stock, country });
      setStock('');
      setCountry('');
      fetchStocks();
    } catch (error) {
      console.error('Error adding stock:', error);
    }
  };

  const handleDelete = async (stockId) => {
    try {
      await axios.delete(`${HOST_URL}/stock/${stockId}`);
      fetchStocks();
    } catch (error) {
      console.error('Error deleting stock:', error);
    }
  };

  const handleDeleteAll = async () => {
    try {
      await axios.delete(`${HOST_URL}/stocks`);
      fetchStocks();
    } catch (error) {
      console.error('Error deleting all stocks:', error);
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

  const formatValue_gt_6 = (value) => {
    const absValue = Math.abs(value);
    const numDigits = Math.floor(Math.log10(absValue)) + 1;

    if (numDigits > 6) {
      return `$${(value * 1e-6).toFixed(2)}T`;
    } else if (numDigits > 3) {
      return `$${(value * 1e-3).toFixed(2)}B`;
    } else {
      return `$${(value).toFixed(2)}M`; 
    }
  };

  const formatValue_gt_3 = (value) => {
    const absValue = Math.abs(value);
    const numDigits = Math.floor(Math.log10(absValue)) + 1;

    if (numDigits > 3) {
      return `${(value * 1e-3).toFixed(2)}B`;
    } else if (numDigits > 0) {
      return `${(value).toFixed(2)}M`;
    } else {
      return `${(value * 1e3).toFixed(2)}k`;
    }
  };

  const return_value = (value) => {
    return `${value.toFixed(2)}`;
  };

  const convert_to_pct = (value)=> {
    return `${(value * 100).toFixed(2)}`;
  };

  const formatValue_dp = (value) => {
    if (value < 1) {
      return `$${value.toFixed(3)}`;
    } else {
      return `$${value.toFixed(2)}`;
    }
  };

  const formatValue_or_na = (value) => {
    return value || 'N/A';
  }

  const formatValue = (metric, value) => {
    if (value === null || value === undefined) return 'N/A';
  
    switch(metric) {
      case 'acquirersMultiple':
        return `$${return_value(value)}`;
      case 'bookValPerShare':
        return `$${return_value(value)}`;
      case 'cash':
        return formatValue_gt_3(value);
      case 'cashPerShare':
        return `$${return_value(value)}`;
      case 'cashToDebt':
        return `${return_value(value)}`;
      case 'cashToMarketCap':
        return `${convert_to_pct(value)}%`;
      case 'code':
        return value.toUpperCase();
      case 'country':
        return value.toLowerCase() === 'aus' ? 'Australia' :
               value.toLowerCase() === 'us' ? 'United States' :
               value;
      case 'currentRatio':
        return `${return_value(value)}`;
      case 'debt':
        return formatValue_gt_3(value);
      case 'debtToEquityRatio':
        return `${return_value(value)}`;
      case 'debtToMarketCap':
        return `${convert_to_pct(value)}%`;
      case 'dividendRate':
        return `$${return_value(value)}`;
      case 'dividendYield':
        return `${return_value(value)}%`;
      case 'earningsGrowth':
        return `${return_value(value)}%`;
      case 'ebitda':
        return `$${formatValue_gt_3(value)}`;
      case 'ebitdaPerShare':
        return `$${return_value(value)}`;
      case 'enterpriseValue':
        return formatValue_gt_6(value);
      case 'eps':
        return `$${return_value(value)}`;
      case 'evToEBITDA':
        return `${return_value(value)}`;
      case 'evToRev':
        return `${return_value(value)}`;
      case 'exDivDate':
        return formatValue_or_na(value);
      case 'fcf':
        return `$${formatValue_gt_3(value)}`;
      case 'fcfPerShare':
        return `$${return_value(value)}`;
      case 'fcfToEV':
        return `${return_value(value)}`;
      case 'fcfToMarketCap':
        return `${return_value(value)}`;
      case 'fiftyDayMA':
        return formatValue_dp(value);
      case 'grossProfit':
        return `$${formatValue_gt_3(value)}`;
      case 'grossProfitPerShare':
        return `$${return_value(value)}`;
      case 'marketCap':
        return formatValue_gt_6(value);
      case 'netIncome':
        return `$${formatValue_gt_3(value)}`;
      case 'netIncomePerShare':
        return `$${return_value(value)}`;
      case 'numSharesAvail':
        return formatValue_gt_3(value);
      case 'ocf':
        return `$${formatValue_gt_3(value)}`;
      case 'ocfPerShare':
        return `$${return_value(value)}`;
      case 'ocfToEV':
        return `${return_value(value)}`;
      case 'ocfToMarketCap':
        return `${return_value(value)}`;
      case 'ocfToRevenueRatio':
        return `${convert_to_pct(value)}%`;
      case 'operatingMargin':
        return `${return_value(value)}%`;
      case 'payoutRatio':
        return `${return_value(value)}%`;
      case 'peRatioForward':
        return `${return_value(value)}`;
      case 'peRatioTrail':
        return `${return_value(value)}`;
      case 'price':
        return formatValue_dp(value);
      case 'priceToBook':
        return `${return_value(value)}`;
      case 'priceToSales':
        return `${return_value(value)}`;
      case 'profitMargin':
        return `${return_value(value)}%`;
      case 'returnOnAssets':
        return `${return_value(value)}%`;
      case 'returnOnEquity':
        return `${return_value(value)}%`;
      case 'revenue':
        return `$${formatValue_gt_3(value)}`;
      case 'revenueGrowth':
        return `${return_value(value)}%`;
      case 'revenuePerShare':
        return `$${return_value(value)}`;
      case 'twoHundredDayMA':
        return formatValue_dp(value);
      case 'yearlyHighPrice':
        return formatValue_dp(value);
      case 'yearlyLowPrice':
        return formatValue_dp(value);
    }
  };

  const handleSort = (column) => {
    if (column === sortColumn) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortColumn(column);
      setSortDirection('asc');
    }
  };

  const sortedStocks = [...stocks].sort((a, b) => {
    if (sortColumn) {
      if (a[sortColumn] < b[sortColumn]) return sortDirection === 'asc' ? -1 : 1;
      if (a[sortColumn] > b[sortColumn]) return sortDirection === 'asc' ? 1 : -1;
    }
    return 0;
  });

  return (
    <DesktopWrapper>
      <Title>Stock Statistics Dashboard</Title>
      <Form onSubmit={handleSubmit}>
        <Input
          type="text"
          value={stock}
          onChange={(e) => setStock(e.target.value)}
          placeholder="Enter stock symbol"
          required
        />
        <Select
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          required
        >
          <option value="">Select country</option>
          {countries.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </Select>
        <Button type="submit">Add Stock</Button>
      </Form>

      <ToggleSection>
        <ToggleTitle>Toggle Metrics:</ToggleTitle>
        <CategoryContainer>
          {Object.entries(metricCategories).map(([category, metrics]) => (
            <CategoryBox key={category}>
              <CategoryTitle>
                <input
                  type="checkbox"
                  id={`category-${category}`}
                  checked={metrics.every(metric => visibleMetrics[metric])}
                  onChange={() => toggleCategory(category)}
                />
                <label htmlFor={`category-${category}`}>{category}</label>
              </CategoryTitle>
              <div>
                {metrics.map(metric => (
                  <MetricLabel key={metric}>
                    <input
                      type="checkbox"
                      id={metric}
                      checked={visibleMetrics[metric]}
                      onChange={() => toggleMetric(metric)}
                    />
                    <label htmlFor={metric}>{metricDisplayNames[metric]}</label>
                  </MetricLabel>
                ))}
              </div>
            </CategoryBox>
          ))}
        </CategoryContainer>
      </ToggleSection>

      <ButtonGroup>
        <DeleteAllButton onClick={handleDeleteAll}>Delete All Stocks</DeleteAllButton>
      </ButtonGroup>

      <Title>Saved Stocks</Title>

      <div style={{overflowX: 'auto', maxHeight: '600px'}}>
        <Table>
          <thead>
            <tr>
              {Object.entries(visibleMetrics).map(([metric, isVisible]) => (
                isVisible && (
                  <Th key={metric} onClick={() => handleSort(metric)}>
                    {metricDisplayNames[metric]}
                    {sortColumn === metric && (
                      <span>{sortDirection === 'asc' ? ' ▲' : ' ▼'}</span>
                    )}
                  </Th>
                )
              ))}
              <Th>Action</Th>
            </tr>
          </thead>
          <tbody>
            {sortedStocks.map((stock) => (
              <tr key={stock.id}>
                {Object.entries(visibleMetrics).map(([metric, isVisible]) => (
                  isVisible && (
                    <Td key={metric}>
                      {formatValue(metric, stock[metric])}
                    </Td>
                  )
                ))}
                <Td>
                  <DeleteButton onClick={() => handleDelete(stock.id)}>Delete</DeleteButton>
                </Td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
    </DesktopWrapper>
  );
};

export default Stats;