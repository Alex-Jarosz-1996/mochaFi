import styled from 'styled-components';

export const DesktopWrapper = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
`;

export const Form = styled.form`
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 20px;
`;

export const Input = styled.input`
  width: 150px;
  padding: 10px;
`;

export const Select = styled.select`
  width: 150px;
  padding: 10px;
`;

export const Button = styled.button`
  padding: 5px 10px;
  cursor: pointer;
  height: 40px;
`;

export const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
`;

export const Th = styled.th`
  position: sticky;
  top: 0;
  background-color: #f8f8f8;
  cursor: pointer;
  user-select: none;
  padding: 12px;
  text-align: left;
  border-bottom: 2px solid #ddd;

  &:hover {
    background-color: #f0f0f0;
  }
`;

export const Td = styled.td`
  padding: 12px;
  border-bottom: 1px solid #ddd;
`;

export const CategoryContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
`;

export const CategoryBox = styled.div`
  flex: 1;
  min-width: 200px;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 4px;
`;

export const CategoryTitle = styled.div`
  font-weight: bold;
  margin-bottom: 10px;
`;

export const MetricLabel = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 5px;
`;

export const Title = styled.h2`
  margin-bottom: 20px;
`;

export const ToggleSection = styled.div`
  margin-bottom: 20px;
`;

export const ToggleTitle = styled.h3`
  margin-bottom: 10px;
`;

export const DeleteButton = styled(Button)`
  background-color: #ff4d4d;
  color: white;
  border: none;
  margin-left: 10px;
  &:hover {
    background-color: #ff3333;
  }
`;

export const DeleteAllButton = styled(DeleteButton)`
  margin-bottom: 20px;
`;

export const ButtonGroup = styled.div`
  display: flex;
  justify-content: center;
`;