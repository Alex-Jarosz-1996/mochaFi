import styled from 'styled-components';

export const StyledBody = styled.body`
  background-color: #f8f9fa;
  margin: 0;
  padding: 0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
`;

export const StyledContainer = styled.div`
  background-color: #ffffff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
  margin: 0;
  min-height: 100vh;
  overflow-x: auto;
`;

export const StyledTable = styled.table`
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;

  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }

  th {
    background-color: #f2f2f2;
    position: sticky;
    top: 0;
    z-index: 10;
  }

  tbody tr:nth-child(even) {
    background-color: #f8f9fa;
  }
`;

export const StyledForm = styled.form`
  display: flex;
  gap: 10px;
  margin-bottom: 20px;

  input, select {
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  button {
    padding: 8px 16px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;

    &:hover {
      background-color: #0056b3;
    }
  }
`;