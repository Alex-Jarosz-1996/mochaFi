import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Stats = () => {
  const [stock, setStock] = useState('');
  const [country, setCountry] = useState('');
  const [countries] = useState(['AUS', 'US']);
  const [stocks, setStocks] = useState([]);

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

  return (
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
      <h3>Saved Stocks</h3>
      <ul>
        {stocks.map((stock) => (
          <li key={stock.id}>
            {stock.code}: ({stock.country})
            <button onClick={() => handleDelete(stock.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Stats;