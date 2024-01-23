import React from 'react';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import Home from './home/Home';
import Chart from './chart/Chart';
import Strategy from './strategy/Strategy';
import Trading from './trading/Trading';

function TabPanel(props) {
  const { children, value, index } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`vertical-tabpanel-${index}`}
      aria-labelledby={`vertical-tab-${index}`}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const VerticalTabs = () => {
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Router>
      <Box
        sx={{
          flexGrow: 1,
          bgcolor: 'background.paper',
          display: 'flex',
          height: 224,
        }}
      >
        <Tabs
          orientation="vertical"
          variant="scrollable"
          value={value}
          onChange={handleChange}
          aria-label="Vertical tabs example"
          sx={{ borderRight: 1, borderColor: 'divider' }}
        >
          <Tab value={0} label="Home" />
          <Tab value={1} label="Chart" />
          <Tab value={2} label="Strategy" />
          <Tab value={3} label="Trading" />
        </Tabs>

        <Routes>
          <Route path="/" element={<Navigate to="/home" />} />
          <Route path="/home" element={<TabPanel value={value} index={0}><Home /></TabPanel>} />
          <Route path="/chart" element={<TabPanel value={value} index={1}><Chart /></TabPanel>} />
          <Route path="/strategy" element={<TabPanel value={value} index={2}><Strategy /></TabPanel>} />
          <Route path="/trading" element={<TabPanel value={value} index={3}><Trading /></TabPanel>} />
        </Routes>
      </Box>
    </Router>
  );
};

export default VerticalTabs;
