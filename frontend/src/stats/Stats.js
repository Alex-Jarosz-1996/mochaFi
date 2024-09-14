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
  StyledContainer 
} from '../styles';

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
  code: "Code",
  country: "Country",
  price: "Price",
  marketCap: "Market Cap",
  numSharesAvail: "Shares Available",
  yearlyLowPrice: "Yearly Low",
  yearlyHighPrice: "Yearly High",
  fiftyDayMA: "50 Day MA",
  twoHundredDayMA: "200 Day MA",
  acquirersMultiple: "Acquirers Multiple",
  currentRatio: "Current Ratio",
  enterpriseValue: "Enterprise Value",
  eps: "EPS",
  evToEBITDA: "EV/EBITDA",
  evToRev: "EV/Revenue",
  peRatioTrail: "P/E (Trailing)",
  peRatioForward: "P/E (Forward)",
  priceToSales: "Price to Sales",
  priceToBook: "Price to Book",
  dividendYield: "Dividend Yield",
  dividendRate: "Dividend Rate",
  exDivDate: "Ex-Dividend Date",
  payoutRatio: "Payout Ratio",
  bookValPerShare: "Book Value per Share",
  cash: "Cash",
  cashPerShare: "Cash per Share",
  cashToMarketCap: "Cash to Market Cap",
  cashToDebt: "Cash to Debt",
  debt: "Debt",
  debtToMarketCap: "Debt to Market Cap",
  debtToEquityRatio: "Debt to Equity",
  returnOnAssets: "Return on Assets",
  returnOnEquity: "Return on Equity",
  ebitda: "EBITDA",
  ebitdaPerShare: "EBITDA per Share",
  earningsGrowth: "Earnings Growth",
  grossProfit: "Gross Profit",
  grossProfitPerShare: "Gross Profit per Share",
  netIncome: "Net Income",
  netIncomePerShare: "Net Income per Share",
  operatingMargin: "Operating Margin",
  profitMargin: "Profit Margin",
  revenue: "Revenue",
  revenueGrowth: "Revenue Growth",
  revenuePerShare: "Revenue per Share",
  fcf: "Free Cash Flow",
  fcfToMarketCap: "FCF to Market Cap",
  fcfPerShare: "FCF per Share",
  fcfToEV: "FCF to EV",
  ocf: "Operating Cash Flow",
  ocfToRevenueRatio: "OCF to Revenue",
  ocfToMarketCap: "OCF to Market Cap",
  ocfPerShare: "OCF per Share",
  ocfToEV: "OCF to EV",
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

  const handleDeleteAll = async () => {
    try {
      await axios.delete('http://localhost:5000/stocks');
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

  const formatValue = (metric, value) => {
    if (value === null || value === undefined) return 'N/A';

    switch(metric) {
      case 'code':
      case 'country':
        return value.toLowerCase() === 'aus' ? 'Australia' :
               value.toLowerCase() === 'us' ? 'United States' :
               value;
      case 'exDivDate':
        return value || 'N/A';
      case 'price':
      case 'yearlyLowPrice':
      case 'yearlyHighPrice':
      case 'fiftyDayMA':
      case 'twoHundredDayMA':
      case 'eps':
      case 'dividendRate':
      case 'bookValPerShare':
      case 'cashPerShare':
      case 'ebitdaPerShare':
      case 'grossProfitPerShare':
      case 'netIncomePerShare':
      case 'revenuePerShare':
      case 'fcfPerShare':
      case 'ocfPerShare':
        return `$${value.toFixed(2)}`;
      case 'marketCap':
      case 'enterpriseValue':
      case 'cash':
      case 'debt':
      case 'ebitda':
      case 'grossProfit':
      case 'netIncome':
      case 'revenue':
      case 'fcf':
      case 'ocf':
        return `$${(value / 1e9).toFixed(2)}B`;
      case 'numSharesAvail':
        return `${(value / 1e6).toFixed(2)}M`;
      case 'dividendYield':
      case 'payoutRatio':
      case 'cashToMarketCap':
      case 'debtToMarketCap':
      case 'returnOnAssets':
      case 'returnOnEquity':
      case 'earningsGrowth':
      case 'operatingMargin':
      case 'profitMargin':
      case 'revenueGrowth':
      case 'ocfToRevenueRatio':
        return `${(value * 100).toFixed(2)}%`;
      default:
        return value.toFixed(2);
    }
  };

  return (
    <StyledContainer>
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
            <option value="">Select a country</option>
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
                    style={{ marginRight: '5px' }}
                  />
                  <label htmlFor={`category-${category}`} style={{ fontSize: '1em', fontWeight: 'bold', cursor: 'pointer' }}>
                    {category}
                  </label>
                </CategoryTitle>
                <div style={{ maxHeight: '150px', overflowY: 'auto' }}>
                  {metrics.map(metric => (
                    <MetricLabel key={metric}>
                      <input
                        type="checkbox"
                        id={metric}
                        checked={visibleMetrics[metric]}
                        onChange={() => toggleMetric(metric)}
                        style={{ marginRight: '5px' }}
                      />
                      <label htmlFor={metric} style={{ fontSize: '0.9em', cursor: 'pointer' }}>
                        {metricDisplayNames[metric]}
                      </label>
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

        <div style={{overflowX: 'auto'}}>
          <Table>
            <thead>
              <tr>
                {Object.entries(visibleMetrics).map(([metric, isVisible]) => (
                  isVisible && (
                    <Th key={metric}>{metricDisplayNames[metric]}</Th>
                  )
                ))}
                <Th>Action</Th>
              </tr>
            </thead>
            <tbody>
              {stocks.map((stock) => (
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
    </StyledContainer>
  );
};

export default Stats;