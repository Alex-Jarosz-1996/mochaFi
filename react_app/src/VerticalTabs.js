import * as React from 'react';
import PropTypes from 'prop-types';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";

import Chart from './Chart/Chart';
import Home from './Home/Home';
import Strategy from './Strategy/Strategy';
import Trading from './Trading/Trading';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`vertical-tabpanel-${index}`}
      aria-labelledby={`vertical-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.number.isRequired,
  value: PropTypes.number.isRequired,
};

function a11yProps(index) {
  return {
    id: `vertical-tab-${index}`,
    'aria-controls': `vertical-tabpanel-${index}`,
  };
}

export default function VerticalTabs() {
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
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
        <Tab label="Home" {...a11yProps(0)} />  
        <Tab label="Chart" {...a11yProps(1)} />
        <Tab label="Strategy" {...a11yProps(2)} />
        <Tab label="Trading" {...a11yProps(3)} />
      </Tabs>
      
      <TabPanel value={value} index={0}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />  
          </Routes>
        </BrowserRouter>  
      </TabPanel>
      
      <TabPanel value={value} index={1}>
        <BrowserRouter>
          <Routes>
            <Route path="/chart" element={<Chart />} />  
          </Routes>
        </BrowserRouter>  
      </TabPanel>
      
      <TabPanel value={value} index={2}>
        <BrowserRouter>
          <Routes>
            <Route path="/strategy" element={<Strategy />} />  
          </Routes>
        </BrowserRouter>  
      </TabPanel>
      
      <TabPanel value={value} index={3}>
        <BrowserRouter>
          <Routes>
            <Route path="/trading" element={<Trading />} />  
          </Routes>
        </BrowserRouter>
      </TabPanel>
    
    </Box>
  );
}
