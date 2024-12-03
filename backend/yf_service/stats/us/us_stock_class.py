import yfinance as yf

from yf_service.stats.us.us_stock_methods import (
    getAcquirersMultiple,
    getBookValuePerShare,
    getCash,
    getCashPerShare,
    getCashToDebt,
    getCashToMarketCap,
    getCurrentRatio,
    getDebt,
    getDebtToEquity,
    getDebtToMarketCap,
    getDividendRate,
    getDividendYield,
    getEarningsGrowth,
    getEBITDA,
    getEBITDA_PerShare,
    getEnterpriseValue,
    getEPS,
    getEV_ToEBITDA,
    getEV_ToRevenue,
    getExDivdate,
    getFCF,
    getFCF_PerShare,
    getFCF_ToEV,
    getFCF_ToMarketCap,
    getFiftyDayAverage,
    getGrossProfit,
    getGrossProfitPerShare,
    getMarketCap,
    getNetIncome,
    getNetIncomePerShare,
    getNumSharesAvail,
    getOCF,
    getOCF_PerShare,
    getOCF_ToEV,
    getOCF_ToMarketCap,
    getOCF_ToRevenue,
    getOperatingMargin,
    getPayoutRatio,
    getPE_RatioForward,
    getPE_RatioTrail,
    getPrice,
    getPriceToBook,
    getPriceToSales,
    getProfitMargin,
    getReturnToAssets,
    getReturnToEquity,
    getRevenue,
    getRevenueGrowth,
    getRevenueGrowthPerShare,
    getTwoHundredDayAverage,
    getYearlyHighPrice,
    getYearlyLowPrice,
)


class StockPriceMetrics:
    def __init__(self, info, num_dp):
        self.price = getPrice(info)
        self.marketCap = getMarketCap(info, num_dp)
        self.numSharesAvail = getNumSharesAvail(info, num_dp)
        self.yearlyLowPrice = getYearlyLowPrice(info)
        self.yearlyHighPrice = getYearlyHighPrice(info)
        self.fiftyDayMA = getFiftyDayAverage(info, num_dp)
        self.twoHundredDayMA = getTwoHundredDayAverage(info, num_dp)


class ValueMetrics:
    def __init__(self, info, num_dp):
        self.acquirersMultiple = getAcquirersMultiple(info, num_dp)
        self.currentRatio = getCurrentRatio(info, num_dp)
        self.enterpriseValue = getEnterpriseValue(info, num_dp)
        self.eps = getEPS(info, num_dp)
        self.evToEBITDA = getEV_ToEBITDA(info, num_dp)
        self.evToRev = getEV_ToRevenue(info, num_dp)
        self.peRatioTrail = getPE_RatioTrail(info, num_dp)
        self.peRatioForward = getPE_RatioForward(info, num_dp)
        self.priceToSales = getPriceToSales(info, num_dp)
        self.priceToBook = getPriceToBook(info, num_dp)


class DividendMetrics:
    def __init__(self, info, num_dp):
        self.dividendYield = getDividendYield(info, num_dp)
        self.dividendRate = getDividendRate(info, num_dp)
        self.exDivDate = getExDivdate(info)
        self.payoutRatio = getPayoutRatio(info, num_dp)


class BalanceSheetMetrics:
    def __init__(self, info, num_dp):
        self.bookValPerShare = getBookValuePerShare(info, num_dp)
        self.cash = getCash(info, num_dp)
        self.cashPerShare = getCashPerShare(info, num_dp)
        self.cashToMarketCap = getCashToMarketCap(info, num_dp)
        self.cashToDebt = getCashToDebt(info, num_dp)
        self.debt = getDebt(info, num_dp)
        self.debtToMarketCap = getDebtToMarketCap(info, num_dp)
        self.debtToEquityRatio = getDebtToEquity(info, num_dp)
        self.returnOnAssets = getReturnToAssets(info, num_dp)
        self.returnOnEquity = getReturnToEquity(info, num_dp)


class IncomeRelatedMetrics:
    def __init__(self, info, num_dp):
        self.ebitda = getEBITDA(info, num_dp)
        self.ebitdaPerShare = getEBITDA_PerShare(info, num_dp)
        self.earningsGrowth = getEarningsGrowth(info, num_dp)
        self.grossProfit = getGrossProfit(info, num_dp)
        self.grossProfitPerShare = getGrossProfitPerShare(info, num_dp)
        self.netIncome = getNetIncome(info, num_dp)
        self.netIncomePerShare = getNetIncomePerShare(info, num_dp)
        self.operatingMargin = getOperatingMargin(info, num_dp)
        self.profitMargin = getProfitMargin(info, num_dp)
        self.revenue = getRevenue(info, num_dp)
        self.revenueGrowth = getRevenueGrowth(info, num_dp)
        self.revenuePerShare = getRevenueGrowthPerShare(info, num_dp)


class CashFlowMetrics:
    def __init__(self, info, num_dp):
        self.fcf = getFCF(info, num_dp)
        self.fcfToMarketCap = getFCF_ToMarketCap(info, num_dp)
        self.fcfPerShare = getFCF_PerShare(info, num_dp)
        self.fcfToEV = getFCF_ToEV(info, num_dp)
        self.ocf = getOCF(info, num_dp)
        self.ocfToRevenueRatio = getOCF_ToRevenue(info, num_dp)
        self.ocfToMarketCap = getOCF_ToMarketCap(info, num_dp)
        self.ocfPerShare = getOCF_PerShare(info, num_dp)
        self.ocfToEV = getOCF_ToEV(info, num_dp)


class US_StockClass:
    """
    Class for US only stocks
    """

    def __init__(self, ticker: str):
        self.country = "us"
        self.num_dp = 3
        self.ticker = ticker
        self.obj = yf.Ticker(self.ticker)
        self.info = self.obj.info

        # Initialize metric classes
        self.stockPriceMetrics = StockPriceMetrics(self.info, self.num_dp)
        self.valueMetrics = ValueMetrics(self.info, self.num_dp)
        self.dividendMetrics = DividendMetrics(self.info, self.num_dp)
        self.balanceSheetMetrics = BalanceSheetMetrics(self.info, self.num_dp)
        self.incomeRelatedMetrics = IncomeRelatedMetrics(self.info, self.num_dp)
        self.cashFlowMetrics = CashFlowMetrics(self.info, self.num_dp)

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
