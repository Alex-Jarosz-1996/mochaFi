from yf_service.stats.aus.aus_stock_methods import (
    get50_DayMovingAverage,
    get52_WkHighPrice,
    get52_WkLowPrice,
    get200_DayMovingAverage,
    getAcquirersMultiple,
    getBookValuePerShare,
    getCash,
    getCashPerShare,
    getCashToDebt,
    getCashToMarketCap,
    getCurrentRatio,
    getDebt,
    getDebtEquityRatio,
    getDebtToMarketCap,
    getEarningsGrowth,
    getEBITDA,
    getEBITDA_perShare,
    getEnterpriseValue,
    getEPS,
    getEV_ToEBITDA,
    getEV_ToRevenue,
    getExDividendDate,
    getFreeCashFlowToEnterpriseValue,
    getGrossProfit,
    getGrossProfitPerShare,
    getLeveredFreeCashFlow,
    getLeveredFreeCashFlowPerShare,
    getLeveredFreeCashFlowToMarketCap,
    getMarketCap,
    getNetIncome,
    getNetIncomePerShare,
    getNumberOfSharesOutstanding,
    getOCF_toRevenueRatio,
    getOperatingCashFlow,
    getOperatingCashFlowPerShare,
    getOperatingCashFlowToEnterpriseValue,
    getOperatingCashFlowToMarketCap,
    getOperatingMargin,
    getPayoutRatio,
    getPE_ratioForward,
    getPE_ratioTrailing,
    getPrice,
    getPriceToBook,
    getPriceToSales,
    getProfitMargin,
    getReturnOnAssets,
    getReturnOnEquity,
    getRevenue,
    getRevenueGrowth,
    getRevenuePerShare,
    getTrailingDividendRate,
    getTrailingDividendYield,
)
from yf_service.stats.aus.websites import yahooFinancePriceData, yahooFinanceData


class StockPriceMetrics:
    def __init__(self, yf_data_price, yf_data):
        self.price = getPrice(yf_data_price)
        self.marketCap = getMarketCap(yf_data)
        self.numSharesAvail = getNumberOfSharesOutstanding(yf_data)
        self.yearlyLowPrice = get52_WkLowPrice(yf_data)
        self.yearlyHighPrice = get52_WkHighPrice(yf_data)
        self.fiftyDayMA = get50_DayMovingAverage(yf_data)
        self.twoHundredDayMA = get200_DayMovingAverage(yf_data)


class ValueMetrics:
    def __init__(self, yf_data):
        self.acquirersMultiple = getAcquirersMultiple(yf_data)
        self.currentRatio = getCurrentRatio(yf_data)
        self.enterpriseValue = getEnterpriseValue(yf_data)
        self.eps = getEPS(yf_data)
        self.evToEBITDA = getEV_ToEBITDA(yf_data)
        self.evToRev = getEV_ToRevenue(yf_data)
        self.peRatioTrail = getPE_ratioTrailing(yf_data)
        self.peRatioForward = getPE_ratioForward(yf_data)
        self.priceToSales = getPriceToSales(yf_data)
        self.priceToBook = getPriceToBook(yf_data)


class DividendMetrics:
    def __init__(self, yf_data):
        self.dividendYield = getTrailingDividendYield(yf_data)
        self.dividendRate = getTrailingDividendRate(yf_data)
        self.exDivDate = getExDividendDate(yf_data)
        self.payoutRatio = getPayoutRatio(yf_data)


class BalanceSheetMetrics:
    def __init__(self, yf_data):
        self.bookValPerShare = getBookValuePerShare(yf_data)
        self.cash = getCash(yf_data)
        self.cashPerShare = getCashPerShare(yf_data)
        self.cashToMarketCap = getCashToMarketCap(yf_data)
        self.cashToDebt = getCashToDebt(yf_data)
        self.debt = getDebt(yf_data)
        self.debtToMarketCap = getDebtToMarketCap(yf_data)
        self.debtToEquityRatio = getDebtEquityRatio(yf_data)
        self.returnOnAssets = getReturnOnAssets(yf_data)
        self.returnOnEquity = getReturnOnEquity(yf_data)


class IncomeRelatedMetrics:
    def __init__(self, yf_data):
        self.ebitda = getEBITDA(yf_data)
        self.ebitdaPerShare = getEBITDA_perShare(yf_data)
        self.earningsGrowth = getEarningsGrowth(yf_data)
        self.grossProfit = getGrossProfit(yf_data)
        self.grossProfitPerShare = getGrossProfitPerShare(yf_data)
        self.netIncome = getNetIncome(yf_data)
        self.netIncomePerShare = getNetIncomePerShare(yf_data)
        self.operatingMargin = getOperatingMargin(yf_data)
        self.profitMargin = getProfitMargin(yf_data)
        self.revenue = getRevenue(yf_data)
        self.revenueGrowth = getRevenueGrowth(yf_data)
        self.revenuePerShare = getRevenuePerShare(yf_data)


class CashFlowMetrics:
    def __init__(self, yf_data):
        self.fcf = getLeveredFreeCashFlow(yf_data)
        self.fcfToMarketCap = getLeveredFreeCashFlowToMarketCap(yf_data)
        self.fcfPerShare = getLeveredFreeCashFlowPerShare(yf_data)
        self.fcfToEV = getFreeCashFlowToEnterpriseValue(yf_data)
        self.ocf = getOperatingCashFlow(yf_data)
        self.ocfToRevenueRatio = getOCF_toRevenueRatio(yf_data)
        self.ocfToMarketCap = getOperatingCashFlowToMarketCap(yf_data)
        self.ocfPerShare = getOperatingCashFlowPerShare(yf_data)
        self.ocfToEV = getOperatingCashFlowToEnterpriseValue(yf_data)


class AusStockClass:
    """
    Class for Australian only stocks
    """

    def __init__(self, ticker: str):
        self.country = "aus"
        self.ticker = ticker
        self.yf_data_price = yahooFinancePriceData(self.ticker)
        self.yf_data = yahooFinanceData(self.ticker)

        # Initialize metric classes
        self.stockPriceMetrics = StockPriceMetrics(self.yf_data_price, self.yf_data)
        self.valueMetrics = ValueMetrics(self.yf_data)
        self.dividendMetrics = DividendMetrics(self.yf_data)
        self.balanceSheetMetrics = BalanceSheetMetrics(self.yf_data)
        self.incomeRelatedMetrics = IncomeRelatedMetrics(self.yf_data)
        self.cashFlowMetrics = CashFlowMetrics(self.yf_data)

    def display_all_metrics(self):
        """
        Display all the metrics of the stock in a readable format.
        """
        attributes = vars(self)

        # Iterate over the attributes and display them
        for attr_name, attr_value in attributes.items():
            if isinstance(
                attr_value,
                (
                    StockPriceMetrics,
                    ValueMetrics,
                    DividendMetrics,
                    BalanceSheetMetrics,
                    IncomeRelatedMetrics,
                    CashFlowMetrics,
                ),
            ):
                print(f"\n{attr_name}:")
                for metric_name, metric_value in vars(attr_value).items():
                    print(f"  {metric_name}: {metric_value}")
            else:
                print(f"{attr_name}: {attr_value}")
