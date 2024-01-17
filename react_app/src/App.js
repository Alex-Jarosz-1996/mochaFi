// src/App.js
import React, { useState } from 'react';
import {
  StyledBody,
  StyledContainer,
  StyledNavTabs,
  StyledTab,
  StyledTabPane,
} from './styles';
import Chart from './Chart/Chart';
import Strategy from './Strategy/Strategy';
import Trading from './Trading/Trading';

function App() {
  const [activeTab, setActiveTab] = useState('chart');

  const handleTabClick = (tab) => {
    setActiveTab(tab);
  };

  return (
    <StyledBody>
      <StyledContainer>
        <StyledNavTabs>
          <StyledTab active={activeTab === 'chart'} onClick={() => handleTabClick('chart')}>
            Chart
          </StyledTab>
          <StyledTab active={activeTab === 'strategy'} onClick={() => handleTabClick('strategy')}>
            Strategy
          </StyledTab>
          <StyledTab active={activeTab === 'trading'} onClick={() => handleTabClick('trading')}>
            Trading
          </StyledTab>
        </StyledNavTabs>

        <StyledTabPane>
          {activeTab === 'chart' && <Chart />}
          {activeTab === 'strategy' && <Strategy />}
          {activeTab === 'trading' && <Trading />}
        </StyledTabPane>
      </StyledContainer>
    </StyledBody>
  );
}

export default App;
