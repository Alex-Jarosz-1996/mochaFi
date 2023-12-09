from algo_core import AlgorithmDefinition

class Strategy(AlgorithmDefinition):
    def __init__(self, algo: AlgorithmDefinition):
        super().__init__(algo.algorithmName, algo.data)
        
        # Strategy: Calculate moving averages
        self.data['MA50'] = round(algo.data['Close'].rolling(50).mean(), 2)
        self.data['MA200'] = round(algo.data['Close'].rolling(200).mean(), 2)

        # Algo: Generate trading signals
        self.data['BuyCondition'] = (self.data['MA50'] > self.data['MA200'])
        self.data['SellCondition'] = (self.data['MA200'] > self.data['MA50'])
