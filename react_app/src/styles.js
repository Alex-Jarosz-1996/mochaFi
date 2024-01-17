import styled from 'styled-components';

export const StyledBody = styled.body`
  background-color: #f8f9fa;
`;

export const StyledContainer = styled.div`
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-top: 50px;
`;

export const StyledNavTabs = styled.ul`
  display: flex;
  list-style-type: none;
  margin-bottom: 20px;
`;

export const StyledTab = styled.li`
  flex: 1;
  text-align: center;
  padding: 10px;
  cursor: pointer;
  background-color: ${(props) => (props.active ? '#007bff' : 'inherit')};
  color: ${(props) => (props.active ? '#ffffff' : 'inherit')};
  border-radius: 5px;
`;

export const StyledTabPane = styled.div`
  padding: 20px;
`;
