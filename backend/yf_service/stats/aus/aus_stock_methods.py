import re


def protectNanOrNone(value):
    """
    Allows return value of None if N/A or nan is present
    """
    return None if str(value) in {"N/A", "nan"} or value is None else value


def regexCheck(value):
    """
    Checks if any punctuation is present in return result
    """
    return None if protectNanOrNone(value) is None else re.sub("[,%]", "", str(value))


def protectDivideByZeroError(num, denom, numDP):
    """
    Returns None if either num or denom is eiher 0 or None
    """
    if num in [0, None] or denom in [0, None]:
        return None
    else:
        return round(num / denom, numDP)


def protectPercentageError(val):
    """
    Uses regexCheck() function to protect against percentage punctuation
    in return value.
    """
    value = regexCheck(val)
    return None if value is None else float(value)


def protectAgainstCharInFloatError(val):
    """
    Deals with 'k', 'M' or 'B' in value
    """
    value = regexCheck(val)

    if value is None:
        return None
    if "k" in str(value) or "K" in str(value):
        return round(float(value[:-1]) * pow(10, 3), 4)
    elif "m" in str(value) or "M" in str(value):
        return round(float(value[:-1]) * pow(10, 6), 4)
    elif "b" in str(value) or "B" in str(value):
        return round(float(value[:-1]) * pow(10, 9), 4)
    else:
        return float(value)


def kmb_ScalarMultiplyFactor(val):
    """
    Deals with 'k', 'M' or 'B' in value
    """
    valInput = regexCheck(val)

    if valInput is None:
        return None
    if "m" in str(valInput) or "M" in str(valInput):
        return round(float(valInput[:-1]), 4)
    elif "b" in str(valInput) or "B" in str(valInput):
        return round(float(valInput[:-1]) * pow(10, 3), 4)
    elif "k" in str(valInput) or "K" in str(valInput):
        return round(float(valInput[:-1]) * pow(10, -3), 4)
    else:
        return float(valInput)


def getMarketCap(yfData):
    """
    Returns Market Cap in $ million
    ex: Market Cap = $50 million
    """
    try:
        marketCapYF = str(yfData[0][1][0])
    except Exception as e:
        print("Error in getMarketCap() function")
        print(e)
        return None
    else:
        return None if marketCapYF is None else kmb_ScalarMultiplyFactor(marketCapYF)


def getNumberOfSharesOutstanding(yfData):
    """
    Returns Number of outstanding shares in $ million
    ex: Number of outstanding shares = $50 million
    """
    try:
        numSharesYF = str(yfData[2][1][2])
    except Exception as e:
        print("Error in getNumberOfSharesOutstanding() function")
        print(e)
        return None
    else:
        return None if numSharesYF is None else kmb_ScalarMultiplyFactor(numSharesYF)


def getPrice(yfDataPrice):
    """
    Returns share price (in $)
    ex: price = $50.0
    """
    try:
        price = yfDataPrice
    except Exception as e:
        print("Error in getPrice() function")
        print(e)
        return None
    else:
        return None if price is None else float(price)


def get52_WkLowPrice(yfData):
    """
    Returns 52 week low price in $
    ex: 52 week low price = $50.0
    """
    try:
        val = str(yfData[1][1][4])
    except Exception as e:
        print("Error in get52_WkLowPrice() function")
        print(e)
        return None
    else:
        return None if val is None else protectAgainstCharInFloatError(val)


def get52_WkHighPrice(yfData):
    """
    Returns 52 week high price in $
    ex: 52 week high price = $50.0
    """
    try:
        val = str(yfData[1][1][3])
    except Exception as e:
        print("Error in get52_WkHighPrice() function")
        print(e)
        return None
    else:
        return None if val is None else protectAgainstCharInFloatError(val)


def get50_DayMovingAverage(yfData):
    """
    Returns 50 Day Moving Average in $
    ex: 50 Day Moving Average = $50.0
    """
    try:
        val = str(yfData[1][1][5])
    except Exception as e:
        print("Error in get50_DayMovingAverage() function")
        print(e)
        return None
    else:
        return None if val is None else protectAgainstCharInFloatError(val)


def get200_DayMovingAverage(yfData):
    """
    Returns 200 Day Moving Average in $
    ex: 200 Day Moving Average = $50.0
    """
    try:
        val = str(yfData[1][1][6])
    except Exception as e:
        print("Error in get200_DayMovingAverage() function")
        print(e)
        return None
    else:
        return None if val is None else protectAgainstCharInFloatError(val)


def getAcquirersMultiple(yfData):
    """
    Returns Acquirers Multiple as $ million
    ex: Acquirers Multiple = $ 50.0 million
    """
    try:
        ev = getEnterpriseValue(yfData)
        ni = getNetIncome(yfData)

        if any(i is None for i in [ev, ni]):
            return None

    except Exception as e:
        print("Error in getAcquirersMultiple() function")
        print(e)
        return None
    else:
        return protectDivideByZeroError(ev, ni, 2)


def getEV_ToRevenue(yfData):
    """
    Returns EV/Revenue ratio as a dimensionless number
    ex: EV/Revenue = 10.0
    """
    try:
        val = str(yfData[0][1][7])
    except Exception as e:
        print("Error in getEV_ToRevenue() function")
        print(e)
        return None
    else:
        return None if val is None else protectAgainstCharInFloatError(val)


def getEV_ToEBITDA(yfData):
    """
    Returns EV/EBITDA ratio as a dimensionless number
    ex: EV/EBITDA = 10.0
    """
    try:
        val = str(yfData[0][1][8])
    except Exception as e:
        print("Error in getEV_ToEBITDA() function")
        print(e)
        return None
    else:
        return None if val is None else protectAgainstCharInFloatError(val)


def getEnterpriseValue(yfData):
    """
    Returns Enterprise Value as $ million
    ex: Enterprise Value = $ 100.00 million
    """
    try:
        mc = getMarketCap(yfData)
        cash = getCash(yfData)
        debt = getDebt(yfData)

        if any(i is None for i in (mc, cash, debt)):
            return None

        return mc + debt - cash
    
    except Exception as e:
        print("Error in getEnterpriseValue() function")
        print(e)
        return None
    

def getPE_ratioTrailing(yfData):
    """
    Returns trailing price/earnings ratio as a dimensionless number
    ex: (trailing) pe = 10.0
    """
    try:
        val = str(yfData[0][1][2])
    except Exception as e:
        print("Error in getPE_ratioTrailing() function")
        print(e)
        return None
    else:
        return None if val is None else protectAgainstCharInFloatError(val)


def getPE_ratioForward(yfData):
    """
    Returns forward price/earnings ratio as a dimensionless number
    ex: (forward) pe = 10.0
    """
    try:
        val = str(yfData[0][1][3])
    except Exception as e:
        print("Error in getPE_ratioForward() function")
        print(e)
        return None
    else:
        return None if val is None else protectAgainstCharInFloatError(val)


def getPriceToSales(yfData):
    """
    Returns price/sales ratio as a dimensionless number
    ex: price/sales = 10.0
    """
    try:
        val = str(yfData[0][1][5])
    except Exception as e:
        print("Error in getPriceToSales() function")
        print(e)
        return None
    else:
        return None if val is None else protectAgainstCharInFloatError(val)


def getPriceToBook(yfData):
    """
    Returns price/book ratio as a dimensionless number
    ex: price/book = 10.0
    """
    try:
        val = str(yfData[0][1][6])
    except Exception as e:
        print("Error in getPriceToBook() function")
        print(e)
        return None
    else:
        return None if val is None else protectAgainstCharInFloatError(val)


def getExDividendDate(yfData):
    """
    Returns Ex Dividend Date as string
    ex: Ex Dividend Date = 28 Feb 2022
    """
    try:
        exDivDate = str(yfData[3][1][7])
    except Exception as e:
        print("Error in getExDividendDate() function")
        print(e)
        return None
    else:
        return None if exDivDate is None else protectNanOrNone(exDivDate)


def getForwardDividendYield(yfData):
    """
    Returns forward dividend yield as %
    ex: forward dividend yield = 10.0 %
    """
    try:
        val = str(yfData[3][1][1])
    except Exception as e:
        print("Error in getForwardDividendYield() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getForwardDividendRate(yfData):
    """
    Returns forward dividend rate as $
    ex: forward dividend rate = $10.0
    """
    try:
        val = str(yfData[3][1][0])
    except Exception as e:
        print("Error in getForwardDividendRate() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getPayoutRatio(yfData):
    """
    Returns payout ratio as %
    ex: payout ratio = 75.0 %
    """
    try:
        val = str(yfData[3][1][5])
    except Exception as e:
        print("Error in getPayoutRatio() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getTrailingDividendYield(yfData):
    """
    Returns trailing dividend yield as %
    ex: trailing dividend yield = 10.0 %
    """
    try:
        val = str(yfData[3][1][3])
    except Exception as e:
        print("Error in getTrailingDividendYield() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getTrailingDividendRate(yfData):
    """
    Returns trailing dividend rate as $
    ex: trailing dividend rate = $10.0
    """
    try:
        val = str(yfData[3][1][2])
    except Exception as e:
        print("Error in getTrailingDividendRate() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getBookValuePerShare(yfData):
    """
    Returns Book value per share as a dimensionless number
    ex: Book value per share = 2.5
    """
    try:
        val = str(yfData[8][1][5])
    except Exception as e:
        print("Error in getBookValuePerShare() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getCash(yfData):
    """
    Returns available cash as $ million
    ex: cash = $100.0 million
    """
    try:
        cashYF = str(yfData[8][1][0])
    except Exception as e:
        print("Error in getCash() function")
        print(e)
        return None
    else:
        return None if cashYF is None else kmb_ScalarMultiplyFactor(cashYF)


def getCashPerShare(yfData):
    """
    Returns Cash per share as a $
    ex: Cash per share = 2.5
    """
    try:
        val = str(yfData[8][1][1])
    except Exception as e:
        print("Error in getCashPerShare() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getCashToMarketCap(yfData):
    """
    Returns Cash To Market Cap as dimensionless number
    ex: Cash To Market Cap = 3
    """
    try:
        cash = getCash(yfData)
        mc = getMarketCap(yfData)

        if any(i is None for i in [cash, mc]):
            return None

    except Exception as e:
        print("Error in getCashToMarketCap() function")
        print(e)
        return None
    else:
        return protectDivideByZeroError(cash, mc, 2)


def getCashToDebt(yfData):
    """
    Returns Cash to Debt as dimensionless number
    ex: Cash to Debt = 3
    """
    try:
        cash = getCash(yfData)
        debt = getDebt(yfData)

        if any(i is None for i in [cash, debt]):
            return None

    except Exception as e:
        print("Error in getCashToDebt() function")
        print(e)
        return None
    else:
        return protectDivideByZeroError(cash, debt, 2)


def getCurrentRatio(yfData):
    """
    Returns current ratio as a dimensionless number
    ex: current ratio = 2.5
    """
    try:
        val = str(yfData[8][1][4])
    except Exception as e:
        print("Error in getCurrentRatio() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getDebt(yfData):
    """
    Returns debt as $ million
    ex: debt = $100.0 million
    """
    try:
        debtYF = str(yfData[8][1][2])
    except Exception as e:
        print("Error in getDebt() function")
        print(e)
        return None
    else:
        return None if debtYF is None else kmb_ScalarMultiplyFactor(debtYF)


def getDebtToMarketCap(yfData):
    """
    Returns Debt To Market Cap as dimensionless number
    ex: Debt To Market Cap = 3
    """
    try:
        debt = getDebt(yfData)
        mc = getMarketCap(yfData)

        if any(i is None for i in [debt, mc]):
            return None

    except Exception as e:
        print("Error in getDebtToMarketCap() function")
        print(e)
        return None
    else:
        return protectDivideByZeroError(debt, mc, 2)


def getDebtEquityRatio(yfData):
    """
    Returns debt to equity ratio as dimensinless number
    ex: debt/equiyt = 0.5
    """
    try:
        val = str(yfData[8][1][3])
    except Exception as e:
        print("Error in getDebtEquityRatio() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getReturnOnAssets(yfData):
    """
    Returns return on assets as %
    ex: return on assets = 10.0 %
    """
    try:
        val = str(yfData[6][1][0])
    except Exception as e:
        print("Error in getReturnOnAssets() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getReturnOnEquity(yfData):
    """
    Returns return on equity as %
    ex: return on equity = 10.0 %
    """
    try:
        val = str(yfData[6][1][1])
    except Exception as e:
        print("Error in getReturnOnEquity() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getEarningsGrowth(yfData):
    """
    Returns earnings growth as %
    ex: earnings growth = 15.0%
    """
    try:
        val = str(yfData[7][1][7])
    except Exception as e:
        print("Error in getEarningsGrowth() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getEPS(yfData):
    """
    Returns EPS as $
    ex: EPS = $15.0
    """
    try:
        val = str(yfData[7][1][6])
    except Exception as e:
        print("Error in getEPS() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getEBITDA(yfData):
    """
    Returns gross profit as $ million ($M)
    ex: gross profit = $100.0 million
    """
    try:
        ebitdaYF = str(yfData[7][1][4])
    except Exception as e:
        print("Error in getEBITDA() function")
        print(e)
        return None
    else:
        return None if ebitdaYF is None else kmb_ScalarMultiplyFactor(ebitdaYF)


def getEBITDA_perShare(yfData):
    """
    Returns EBITDA on a per share basis in $ / share
    Ex: EBITDA per Share = $5 / share
    """
    try:
        ebitda = getEBITDA(yfData)
        numShares = getNumberOfSharesOutstanding(yfData)

        if any(i is None for i in [ebitda, numShares]):
            return None

    except Exception as e:
        print("Error in getEBITDA_perShare() function")
        print(e)
        return None
    else:
        return protectDivideByZeroError(ebitda, numShares, 2)


def getGrossProfit(yfData):
    """
    Returns gross profit as $ million ($M)
    ex: gross profit = $100.0 million
    """
    try:
        grossProfitYF = str(yfData[7][1][3])
    except Exception as e:
        print("Error in getGrossProfit() function")
        print(e)
        return None
    else:
        return (
            None if grossProfitYF is None else kmb_ScalarMultiplyFactor(grossProfitYF)
        )


def getGrossProfitPerShare(yfData):
    """
    Returns gross profit per share as $ / share
    ex: gross profit = $5 / share
    """
    try:
        gp = getGrossProfit(yfData)
        numShares = getNumberOfSharesOutstanding(yfData)

        if any(i is None for i in [gp, numShares]):
            return None

    except Exception as e:
        print("Error in getGrossProfitPerShare() function")
        print(e)
        return None
    else:
        return protectDivideByZeroError(gp, numShares, 2)


def getNetIncome(yfData):
    """
    Returns Net Income as $ million ($M)
    ex: Net Income = $100.0 million
    """
    try:
        netIncomeYF = str(yfData[7][1][5])
    except Exception as e:
        print("Error in getNetIncome() function")
        print(e)
        return None
    else:
        return None if netIncomeYF is None else kmb_ScalarMultiplyFactor(netIncomeYF)


def getNetIncomePerShare(yfData):
    """
    Returns Net Income PerShare as $ / share
    ex: Net Income PerShare = $5 / share
    """
    try:
        ni = getNetIncome(yfData)
        numShares = getNumberOfSharesOutstanding(yfData)

        if any(i is None for i in [ni, numShares]):
            return None

    except Exception as e:
        print("Error in getNetIncomePerShare() function")
        print(e)
        return None
    else:
        return protectDivideByZeroError(ni, numShares, 2)


def getNetIncomeMarginRatio(yfData):
    """
    Returns net income / net revenue as a ratio
    Ex: net income / net revenue = 5
    """
    try:
        ni = getNetIncome(yfData)
        rev = getRevenue(yfData)

        if any(i is None for i in [ni, rev]):
            return None

    except Exception as e:
        print("Error in getNetIncomeMarginRatio() function")
        print(e)
        return None
    else:
        return protectDivideByZeroError(ni, rev, 2)


def getOperatingMargin(yfData):
    """
    Returns operating margin as %
    ex: operating margin = 50.0 %
    """
    try:
        val = str(yfData[5][1][1])
    except Exception as e:
        print("Error in getOperatingMargin() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getProfitMargin(yfData):
    """
    Returns profit margin as %
    ex: profit margin = 50.0 %
    """
    try:
        val = str(yfData[5][1][0])
    except Exception as e:
        print("Error in getProfitMargin() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getRevenue(yfData):
    """
    Returns Revenue as $ million ($M)
    ex: Revenue = $100.0 million
    """
    try:
        revenueYF = str(yfData[7][1][0])
    except Exception as e:
        print("Error in getRevenue() function")
        print(e)
        return None
    else:
        return None if revenueYF is None else kmb_ScalarMultiplyFactor(revenueYF)


def getRevenuePerShare(yfData):
    """
    Returns revenue per share as dimensionless number
    ex: revenue per share = 15.0
    """
    try:
        val = str(yfData[7][1][1])
    except Exception as e:
        print("Error in getRevenuePerShare() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getRevenueGrowth(yfData):
    """
    Returns revenue growth as %
    ex: revenue growth = 15.0%
    """
    try:
        val = str(yfData[7][1][2])
    except Exception as e:
        print("Error in getRevenueGrowth() function")
        print(e)
        return None
    else:
        return None if val is None else protectPercentageError(val)


def getOperatingCashFlowToEnterpriseValue(yfData):
    """
    Returns Enterprise Value To Operating CashFlow as dimensionless number
    ex: Enterprise Value To Operating CashFlow =  10.0
    """
    try:
        ev = getEnterpriseValue(yfData)
        ocf = getOperatingCashFlow(yfData)

        if any(i is None for i in [ev, ocf]):
            return None

    except Exception as e:
        print("Error in getOperatingCashFlowToEnterpriseValue() function")
        print(e)
        return None
    else:
        return protectDivideByZeroError(ocf, ev, 2)


def getOCF_toRevenueRatio(yfData):
    """
    Returns FCF to Revenue as dimensionless number
    ex: FCF / Revenue = 5
    """
    try:
        ocf = getOperatingCashFlow(yfData)
        rev = getRevenue(yfData)

        if any(i is None for i in [ocf, rev]):
            return None

    except Exception as e:
        print("Error in getOCF_toRevenueRatio() function")
        print(e)
        return None
    else:
        return protectDivideByZeroError(ocf, rev, 2)


def getLeveredFreeCashFlow(yfData):
    """
    Returns levered free cash flow as $ million
    ex: levered free cash flow = $ 100 million
    """
    try:
        lfcfYF = str(yfData[9][1][1])
    except Exception as e:
        print("Error in getLeveredFreeCashFlow() function")
        print(e)
        return None
    else:
        return None if lfcfYF is None else kmb_ScalarMultiplyFactor(lfcfYF)


def getLeveredFreeCashFlowToMarketCap(yfData):
    """
    Returns Levered Free Cash Flow To Market Cap as dimensionless number
    ex: Levered Free Cash Flow To Market Cap = 3
    """
    try:
        lfcf = getLeveredFreeCashFlow(yfData)
        mc = getMarketCap(yfData)

        if any(i is None for i in [lfcf, mc]):
            return None

    except Exception as e:
        print("Error in getLeveredFreeCashFlowToMarketCap() function")
        print(e)
        return None
    else:
        return protectDivideByZeroError(lfcf, mc, 2)


def getLeveredFreeCashFlowPerShare(yfData):
    """
    Returns Levered Free CashFlow PerShare as $ / share
    ex: Operating CashFlow PerShare = $5 / share
    """
    try:
        lfcf = getLeveredFreeCashFlow(yfData)
        numShares = getNumberOfSharesOutstanding(yfData)

        if any(i is None for i in [lfcf, numShares]):
            return None

    except Exception as e:
        print("Error in getLeveredFreeCashFlowPerShare() function")
        print(e)
        return None
    else:
        return protectDivideByZeroError(lfcf, numShares, 2)


def getFreeCashFlowToEnterpriseValue(yfData):
    """
    Returns Enterprise Value To Free CashFlow as dimensionless number
    ex: Enterprise Value To Free CashFlow =  10.0
    """
    try:
        ev = getEnterpriseValue(yfData)
        lfcf = getLeveredFreeCashFlow(yfData)

        if any(i is None for i in [ev, lfcf]):
            return None

    except Exception as e:
        print("Error in getFreeCashFlowToEnterpriseValue() function")
        print(e)
        return None
    else:
        return protectDivideByZeroError(lfcf, ev, 2)


def getOperatingCashFlow(yfData):
    """
    Returns operating cash flow as $ million
    ex: operating cash flow = $ 100 million
    """
    try:
        ocfYF = str(yfData[9][1][0])
    except Exception as e:
        print("Error in getOperatingCashFlow() function")
        print(e)
        return None
    else:
        return None if ocfYF is None else kmb_ScalarMultiplyFactor(ocfYF)


def getOperatingCashFlowToMarketCap(yfData):
    """
    Returns Operating Cash Flow To Market Cap as dimensionless number
    ex: Operating Cash Flow To Market Cap = 3
    """
    try:
        ocf = getOperatingCashFlow(yfData)
        mc = getMarketCap(yfData)

        if any(i is None for i in [ocf, mc]):
            return None

    except Exception as e:
        print("Error in getOperatingCashFlowToMarketCap() function")
        print(e)
        return None
    else:
        return protectDivideByZeroError(ocf, mc, 2)


def getOperatingCashFlowPerShare(yfData):
    """
    Returns Operating CashFlow PerShare as $ / share
    ex: Operating CashFlow PerShare = $5 / share
    """
    try:
        ocf = getOperatingCashFlow(yfData)
        numShares = getNumberOfSharesOutstanding(yfData)

        if any(i is None for i in [ocf, numShares]):
            return None

    except Exception as e:
        print("Error in getOperatingCashFlowPerShare() function")
        print(e)
        return None
    else:
        return protectDivideByZeroError(ocf, numShares, 2)
