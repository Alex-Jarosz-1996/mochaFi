import React, { useEffect } from 'react';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import { Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';

import Home from './home/Home';
import Chart from './chart/Chart';
import Strategy from './strategy/Strategy';
import Trading from './trading/Trading';
import Stats from './stats/Stats';

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
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Update tab based on current path
    switch(location.pathname) {
      case '/home': setValue(0); break;
      case '/stats': setValue(1); break;
      case '/chart': setValue(2); break;
      case '/strategy': setValue(3); break;
      case '/trading': setValue(4); break;
      default: setValue(0); break;
    }
  }, [location]);

  const handleChange = (event, newValue) => {
    setValue(newValue);

    // Navigate based on tab selection
    switch(newValue) {
      case 0: navigate('/home'); break;
      case 1: navigate('/stats'); break;
      case 2: navigate('/chart'); break;
      case 3: navigate('/strategy'); break;
      case 4: navigate('/trading'); break;
      default: break;
    }
  };

  return (
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
        <Tab label="Home" />
        <Tab label="Stats" />
        <Tab label="Chart" />
        <Tab label="Strategy" />
        <Tab label="Trading" />
      </Tabs>

      <Routes>
        <Route path="/" element={<Navigate to="/home" />} />
        <Route path="/home" element={<TabPanel value={value} index={0}><Home /></TabPanel>} />
        <Route path="/stats" element={<TabPanel value={value} index={1}><Stats /></TabPanel>} />
        <Route path="/chart" element={<TabPanel value={value} index={2}><Chart /></TabPanel>} />
        <Route path="/strategy" element={<TabPanel value={value} index={3}><Strategy /></TabPanel>} />
        <Route path="/trading" element={<TabPanel value={value} index={4}><Trading /></TabPanel>} />
      </Routes>
    </Box>
  );
};

export default VerticalTabs;
