import React from 'react';

const Statistics = () => {
  return (
    <div>
    
    <label for="Country_selector">Select Country from dropdown: </label>
    <select id="Country_selector" name="Select_countries">
        <option value="Blank">-</option>
        <option value="Aus">Australia</option>
        <option value="US">US</option>
    </select>
    <div id="message"></div>

    <label for="Stock_selector">Select Stock from all: </label>
    
    </div>
  );
};

export default Statistics;
