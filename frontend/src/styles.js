import styled from 'styled-components';

export const Title = styled.h2`
  color: #2c3e50;
  font-size: 28px;
  margin-bottom: 20px;
  text-align: center;
`;

export const Form = styled.form`
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  justify-content: center;
`;

export const Input = styled.input`
  padding: 10px;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 16px;
`;

export const Select = styled.select`
  padding: 10px;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 16px;
`;

export const Button = styled.button`
  padding: 10px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background-color: #2980b9;
  }
`;

export const ToggleSection = styled.div`
  margin-bottom: 20px;
`;

export const ToggleTitle = styled.h4`
  color: #34495e;
  font-size: 18px;
  margin-bottom: 10px;
`;

export const CategoryContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
`;

export const CategoryBox = styled.div`
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 15px;
  min-width: 200px;
  flex: 1;
`;

export const CategoryTitle = styled.label`
  font-weight: bold;
  font-size: 16px;
  color: #2c3e50;
  display: flex;
  align-items: center;
  margin-bottom: 10px;
`;

export const MetricLabel = styled.label`
  font-size: 14px;
  color: #34495e;
  display: flex;
  align-items: center;
  margin-bottom: 5px;
`;

export const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
`;

export const Th = styled.th`
  background-color: #3498db;
  color: white;
  padding: 12px;
  text-align: left;
  font-weight: bold;
`;

export const Td = styled.td`
  
  padding: 10px;
  border-bottom: 1px solid #e0e0e0;
`;

export const DeleteButton = styled.button`
  padding: 5px 10px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background-color: #c0392b;
  }
`;

export const DeleteAllButton = styled(Button)`
  background-color: #e74c3c;
  margin-left: 10px;

  &:hover {
    background-color: #c0392b;
  }
`;

export const ButtonGroup = styled.div`
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
`;