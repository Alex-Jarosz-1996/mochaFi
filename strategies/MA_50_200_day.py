from core.algo_core import AlgorithmDefinition


class Strategy(AlgorithmDefinition):
    def __init__(self, algorithmName, algo: AlgorithmDefinition):
        self.algorithmName = algorithmName
        
        super().__init__(algo.data)
        
        # Strategy: Calculate moving averages
        self.data['MA50'] = round(algo.data['Close'].rolling(50).mean(), 2)
        self.data['MA200'] = round(algo.data['Close'].rolling(200).mean(), 2)

        # Algo: Generate trading signals
        self.data['BuyCondition'] = (self.data['MA50'] > self.data['MA200'])
        self.data['SellCondition'] = (self.data['MA200'] > self.data['MA50'])
