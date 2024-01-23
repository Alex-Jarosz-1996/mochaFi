import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { StyledBody, StyledContainer } from './styles';
import VerticalTabs from './VerticalTabs';

function App() {
  return (
    <Router>
      <StyledBody>
        <StyledContainer>
          <VerticalTabs />
        </StyledContainer>
      </StyledBody>
    </Router>
  );
}

export default App;
