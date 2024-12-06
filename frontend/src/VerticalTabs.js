import React, { useEffect } from 'react';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import { Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';

import Chart from './chart/Chart';
import Strategy from './strategy/Strategy';
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
      case '/stats': setValue(0); break;
      case '/chart': setValue(1); break;
      case '/strategy': setValue(2); break;
      default: setValue(0); break;
    }
  }, [location]);

  const handleChange = (event, newValue) => {
    setValue(newValue);

    // Navigate based on tab selection
    switch(newValue) {
      case 0: navigate('/stats'); break;
      case 1: navigate('/chart'); break;
      case 2: navigate('/strategy'); break;
      default: break;
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        minHeight: '100vh',
      }}
    >
      <Tabs
        orientation="vertical"
        variant="scrollable"
        value={value}
        onChange={handleChange}
        aria-label="Vertical tabs example"
        sx={{ 
          borderRight: 1, 
          borderColor: 'divider',
          minWidth: '120px',
          position: 'sticky',
          top: 0,
          height: '100vh',
          '& .MuiTab-root': {
            alignItems: 'flex-start',
            textAlign: 'left',
          }
        }}
      >
        <Tab label="Stats" />
        <Tab label="Chart" />
        <Tab label="Strategy" />
      </Tabs>

      <Box sx={{ flexGrow: 1 }}>
        <Routes>
          <Route path="/" element={<Navigate to="/stats" />} />
          <Route path="/stats" element={<TabPanel value={value} index={0}><Stats /></TabPanel>} />
          <Route path="/chart" element={<TabPanel value={value} index={1}><Chart /></TabPanel>} />
          <Route path="/strategy" element={<TabPanel value={value} index={2}><Strategy /></TabPanel>} />
        </Routes>
      </Box>
    </Box>
  );
};

export default VerticalTabs;