from datetime import datetime
from typing import Dict, Optional, Union


def getPrice(obj: Dict[str, Optional[Union[int, float, str]]]) -> float:
    """
    Returns share price (in $)
    ex: price = $50.0
    """
    try:
        price = obj.get("currentPrice", None)
    except Exception as e:
        print("Error in getPrice() function")
        print(e)
        return None
    else:
        return None if price is None else float(price)


def getMarketCap(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns Cash To Market Cap as dimensionless number
    ex: Cash To Market Cap = 3
    """
    try:
        mc = obj.get("marketCap", None)
    except Exception as e:
        print("Error in getMarketCap() function")
        print(e)
        return None
    else:
        return None if mc is None else round(float(mc) * 10**-6, num_dp)


def getNumSharesAvail(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns total number of shares outstanding for the stock
    ex: Num Shares Available = 25 million
    """
    try:
        numShares = obj.get("sharesOutstanding", None)
    except Exception as e:
        print("Error in getNumSharesAvail() function")
        print(e)
        return None
    else:
        return None if numShares is None else round(float(numShares) * 10**-6, num_dp)


def getYearlyLowPrice(obj: Dict[str, Optional[Union[int, float, str]]]) -> float:
    """
    Returns 52 week low price in $
    ex: 52 week low price = $50.0
    """
    try:
        ylp = obj.get("fiftyTwoWeekLow", None)
    except Exception as e:
        print("Error in getYearlyLowPrice() function")
        print(e)
        return None
    else:
        return None if ylp is None else float(ylp)


def getYearlyHighPrice(obj: Dict[str, Optional[Union[int, float, str]]]) -> float:
    """
    Returns 52 week high price in $
    ex: 52 week high price = $50.0
    """
    try:
        yhp = obj.get("fiftyTwoWeekHigh", None)
    except Exception as e:
        print("Error in getYearlyHighPrice() function")
        print(e)
        return None
    else:
        return None if yhp is None else float(yhp)


def getFiftyDayAverage(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns 50 Day Moving Average in $
    ex: 50 Day Moving Average = $50.0
    """
    try:
        fiftyDayAvg = obj.get("fiftyDayAverage", None)
    except Exception as e:
        print("Error in getFiftyDayAverage() function")
        print(e)
        return None
    else:
        return None if fiftyDayAvg is None else round(float(fiftyDayAvg), num_dp)


def getTwoHundredDayAverage(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns 200 Day Moving Average in $
    ex: 200 Day Moving Average = $50.0
    """
    try:
        twoHundredDayAvg = obj.get("twoHundredDayAverage", None)
    except Exception as e:
        print("Error in getTwoHundredDayAverage() function")
        print(e)
        return None
    else:
        return (
            None if twoHundredDayAvg is None else round(float(twoHundredDayAvg), num_dp)
        )


def getAcquirersMultiple(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns Acquirers Multiple as $ million
    ex: Acquirers Multiple = $ 50.0 million
    """
    try:
        mc = obj.get("marketCap", None)
        td = obj.get("totalDebt", None)
        tc = obj.get("totalCash", None)
        ni = obj.get("netIncomeToCommon", None)

        if any(i is None for i in [mc, td, tc, ni]):
            return None

        am = (mc + td - tc) / ni
    except Exception as e:
        print("Error in getAcquirersMultiple() function")
        print(e)
        return None
    else:
        return None if am is None else round(float(am), num_dp)


def getCurrentRatio(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns current ratio as a dimensionless number
    ex: current ratio = 2.5
    """
    try:
        cr = obj.get("currentRatio", None)
    except Exception as e:
        print("Error in getCurrentRatio() function")
        print(e)
        return None
    else:
        return None if cr is None else round(float(cr), num_dp)


def getEnterpriseValue(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns Enterprise Value as $ million
    ex: Enterprise Value = $ 100.00 million
    """
    try:
        mc = obj.get("marketCap", None)
        td = obj.get("totalDebt", None)
        tc = obj.get("totalCash", None)

        if any(i is None for i in [mc, td, tc]):
            return None

        ev = mc + td - tc
    except Exception as e:
        print("Error in getEnterpriseValue() function")
        print(e)
        return None
    else:
        return None if ev is None else round(float(ev) * 10**-6, num_dp)


def getEPS(obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int) -> float:
    """
    Returns EPS as $
    ex: EPS = $15.0
    """
    try:
        eps = obj.get("trailingEps", None)
    except Exception as e:
        print("Error in getEPS() function")
        print(e)
        return None
    else:
        return None if eps is None else round(float(eps), num_dp)


def getEV_ToEBITDA(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns EV/EBITDA ratio as a dimensionless number
    ex: EV/EBITDA = 10.0
    """
    try:
        mc = obj.get("marketCap", None)
        td = obj.get("totalDebt", None)
        tc = obj.get("totalCash", None)
        ebitda = obj.get("ebitda", None)

        if any(i is None for i in [mc, td, tc, ebitda]):
            return None

        ev2ebitda = (mc + td - tc) / ebitda
    except Exception as e:
        print("Error in getEV_ToEBITDA() function")
        print(e)
        return None
    else:
        return None if ev2ebitda is None else round(float(ev2ebitda), num_dp)


def getEV_ToRevenue(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns EV/Revenue ratio as a dimensionless number
    ex: EV/Revenue = 10.0
    """
    try:
        mc = obj.get("marketCap", None)
        td = obj.get("totalDebt", None)
        tc = obj.get("totalCash", None)
        rev = obj.get("totalRevenue", None)

        if any(i is None for i in [mc, td, tc, rev]):
            return None

        ev2rev = (mc + td - tc) / rev
    except Exception as e:
        print("Error in getEV_ToRevenue() function")
        print(e)
        return None
    else:
        return None if ev2rev is None else round(float(ev2rev), num_dp)


def getPE_RatioTrail(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns trailing price/earnings ratio as a dimensionless number
    ex: (trailing) pe = 10.0
    """
    try:
        peTrail = obj.get("trailingPE", None)
    except Exception as e:
        print("Error in getPE_RatioTrail() function")
        print(e)
        return None
    else:
        return None if peTrail is None else round(float(peTrail), num_dp)


def getPE_RatioForward(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns forward price/earnings ratio as a dimensionless number
    ex: (forward) pe = 10.0
    """
    try:
        peForward = obj.get("forwardPE", None)
    except Exception as e:
        print("Error in getPE_RatioForward() function")
        print(e)
        return None
    else:
        return None if peForward is None else round(float(peForward), num_dp)


def getPriceToSales(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns price/sales ratio as a dimensionless number
    ex: price/sales = 10.0
    """
    try:
        price2Sales = obj.get("priceToSalesTrailing12Months", None)
    except Exception as e:
        print("Error in getPriceToSales() function")
        print(e)
        return None
    else:
        return None if price2Sales is None else round(float(price2Sales), num_dp)


def getPriceToBook(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns price/book ratio as a dimensionless number
    ex: price/book = 10.0
    """
    try:
        price2Book = obj.get("priceToBook", None)
    except Exception as e:
        print("Error in getPriceToBook() function")
        print(e)
        return None
    else:
        return None if price2Book is None else round(float(price2Book), num_dp)


def getDividendYield(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns dividend yield as %
    ex: dividend yield = 10.0 %
    """
    try:
        divYield = obj.get("trailingAnnualDividendYield", None)
    except Exception as e:
        print("Error in getDividendYield() function")
        print(e)
        return None
    else:
        return None if divYield is None else round(float(divYield), num_dp)


def getDividendRate(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns trailing dividend rate as $
    ex: trailing dividend rate = $10.0
    """
    try:
        divRate = obj.get("dividendRate", None)
    except Exception as e:
        print("Error in getDividendRate() function")
        print(e)
        return None
    else:
        return None if divRate is None else round(float(divRate), num_dp)


def getExDivdate(obj: Dict[str, Optional[Union[int, float, str]]]) -> str:
    """
    Returns Ex Dividend Date as string
    ex: Ex Dividend Date = 28 Feb 2022
    """
    try:
        exDivDate = obj.get("exDividendDate", None)

        if exDivDate is None:
            return exDivDate

    except Exception as e:
        print("Error in getExDivdate() function")
        print(e)
        return None
    else:
        exDivDate_tstamp = datetime.fromtimestamp(exDivDate)
        exDivDate_formatted = f"{exDivDate_tstamp.day:02d}/{exDivDate_tstamp.month:02d}/{exDivDate_tstamp.year}"
        date_object = datetime.strptime(str(exDivDate_formatted), "%d/%m/%Y")
        return date_object.strftime("%d %b %Y")


def getPayoutRatio(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> str:
    """
    Returns payout ratio as %
    ex: payout ratio = 75.0 %
    """
    try:
        payoutRatio = obj.get("payoutRatio", None)
    except Exception as e:
        print("Error in getPayoutRatio() function")
        print(e)
        return None
    else:
        return None if payoutRatio is None else round(float(payoutRatio), num_dp)


def getBookValuePerShare(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns Book value per share as a dimensionless number
    ex: Book value per share = 2.5
    """
    try:
        bv = obj.get("bookValue", None)
        ns = obj.get("sharesOutstanding", None)

        if any(i is None for i in [bv, ns]):
            return None

        bv2shares = bv / ns
    except Exception as e:
        print("Error in getBookValuePerShare() function")
        print(e)
        return None
    else:
        return None if bv2shares is None else round(float(bv2shares), num_dp)


def getCash(obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int) -> float:
    """
    Returns available cash as $ million
    ex: cash = $100.0 million
    """
    try:
        cash = obj.get("totalCash", None)
    except Exception as e:
        print("Error in getCash() function")
        print(e)
        return None
    else:
        return None if cash is None else round(float(cash) * 10**-6, num_dp)


def getCashPerShare(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns Cash per share as a $
    ex: Cash per share = 2.5
    """
    try:
        cashPerShare = obj.get("totalCashPerShare", None)
    except Exception as e:
        print("Error in getCashPeShare() function")
        print(e)
        return None
    else:
        return None if cashPerShare is None else round(float(cashPerShare), num_dp)


def getCashToMarketCap(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns Cash To Market Cap as dimensionless number
    ex: Cash To Market Cap = 3
    """
    try:
        tc = obj.get("totalCash", None)
        mc = obj.get("marketCap", None)

        if any(i is None for i in [tc, mc]):
            return None

        cash2mc = tc / mc
    except Exception as e:
        print("Error in getCashToMarketCap() function")
        print(e)
        return None
    else:
        return None if cash2mc is None else round(float(cash2mc), num_dp)


def getCashToDebt(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns Cash to Debt as dimensionless number
    ex: Cash to Debt = 3
    """
    try:
        tc = obj.get("totalCash", None)
        td = obj.get("totalDebt", None)

        if any(i is None for i in [tc, td]):
            return None

        cash2debt = tc / td
    except Exception as e:
        print("Error in getCashToDebt() function")
        print(e)
        return None
    else:
        return None if cash2debt is None else round(float(cash2debt), num_dp)


def getDebt(obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int) -> float:
    """
    Returns debt as $ million
    ex: debt = $100.0 million
    """
    try:
        td = obj.get("totalDebt", None)
    except Exception as e:
        print("Error in getDebt() function")
        print(e)
        return None
    else:
        return None if td is None else round(float(td) * 10**-6, num_dp)


def getDebtToMarketCap(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns Debt To Market Cap as dimensionless number
    ex: Debt To Market Cap = 3
    """
    try:
        td = obj.get("totalDebt", None)
        mc = obj.get("marketCap", None)

        if any(i is None for i in [mc, td]):
            return None

        debt2marketCap = td / mc
    except Exception as e:
        print("Error in getDebtToMarketCap() function")
        print(e)
        return None
    else:
        return None if debt2marketCap is None else round(float(debt2marketCap), num_dp)


def getDebtToEquity(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns debt to equity ratio as dimensinless number
    ex: debt/equity = 0.5
    """
    try:
        de = obj.get("debtToEquity", None)
    except Exception as e:
        print("Error in getDebtToEquity() function")
        print(e)
        return None
    else:
        return None if de is None else round(float(de), num_dp)


def getReturnToAssets(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns return on assets as %
    ex: return on assets = 10.0 %
    """
    try:
        roa = obj.get("returnOnAssets", None)
    except Exception as e:
        print("Error in getReturnToAssets() function")
        print(e)
        return None
    else:
        return None if roa is None else round(float(roa), num_dp)


def getReturnToEquity(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns return on equity as %
    ex: return on equity = 10.0 %
    """
    try:
        roe = obj.get("returnOnEquity", None)
    except Exception as e:
        print("Error in getReturnToEquity() function")
        print(e)
        return None
    else:
        return None if roe is None else round(float(roe), num_dp)


def getEBITDA(obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int) -> float:
    """
    Returns gross profit as $ million ($M)
    ex: gross profit = $100.0 million
    """
    try:
        ebitda = obj.get("ebitda", None)
    except Exception as e:
        print("Error in getEBITDA() function")
        print(e)
        return None
    else:
        return None if ebitda is None else round(float(ebitda) * 10**-6, num_dp)


def getEBITDA_PerShare(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns EBITDA on a per share basis in $ / share
    Ex: EBITDA per Share = $5 / share
    """
    try:
        ebitda = obj.get("ebitda", None)
        numShares = obj.get("sharesOutstanding", None)

        if any(i is None for i in [ebitda, numShares]):
            return None

        ebitdaPerShare = ebitda / numShares
    except Exception as e:
        print("Error in getEBITDA_PerShare() function")
        print(e)
        return None
    else:
        return None if ebitdaPerShare is None else round(float(ebitdaPerShare), num_dp)


def getEarningsGrowth(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns earnings growth as %
    ex: earnings growth = 15.0%
    """
    try:
        eg = obj.get("earningsGrowth", None)
    except Exception as e:
        print("Error in getEarningsGrowth() function")
        print(e)
        return None
    else:
        return None if eg is None else round(float(eg), num_dp)


def getGrossProfit(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns gross profit as $ million ($M)
    ex: gross profit = $100.0 million
    """
    try:
        profits = obj.get("grossProfits", None)
    except Exception as e:
        print("Error in getGrossProfit() function")
        print(e)
        return None
    else:
        return None if profits is None else round(float(profits) * 10**-6, num_dp)


def getGrossProfitPerShare(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns gross profit per share as $ / share
    ex: gross profit = $5 / share
    """
    try:
        profits = obj.get("grossProfits", None)
        ns = obj.get("sharesOutstanding", None)

        if any(i is None for i in [profits, ns]):
            return None

        profitsPerShare = profits / ns
    except Exception as e:
        print("Error in getGrossProfitPerShare() function")
        print(e)
        return None
    else:
        return (
            None if profitsPerShare is None else round(float(profitsPerShare), num_dp)
        )


def getNetIncome(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns Net Income as $ million ($M)
    ex: Net Income = $100.0 million
    """
    try:
        ni = obj.get("netIncomeToCommon", None)
    except Exception as e:
        print("Error in getNetIncome() function")
        print(e)
        return None
    else:
        return None if ni is None else round(float(ni) * 10**-6, num_dp)


def getNetIncomePerShare(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns Net Income PerShare as $ / share
    ex: Net Income PerShare = $5 / share
    """
    try:
        ni = obj.get("netIncomeToCommon", None)
        ns = obj.get("sharesOutstanding", None)

        if any(i is None for i in [ni, ns]):
            return None

        niPerShare = ni / ns
    except Exception as e:
        print("Error in getNetIncomePerShare() function")
        print(e)
        return None
    else:
        return None if niPerShare is None else round(float(niPerShare), num_dp)


def getOperatingMargin(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns operating margin as %
    ex: operating margin = 50.0 %
    """
    try:
        om = obj.get("operatingMargins", None)
    except Exception as e:
        print("Error in getOperatingMargin() function")
        print(e)
        return None
    else:
        return None if om is None else round(float(om), num_dp)


def getProfitMargin(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns profit margin as %
    ex: profit margin = 50.0 %
    """
    try:
        pm = obj.get("profitMargins", None)
    except Exception as e:
        print("Error in getProfitMargin() function")
        print(e)
        return None
    else:
        return None if pm is None else round(float(pm), num_dp)


def getRevenue(obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int) -> float:
    """
    Returns Revenue as $ million ($M)
    ex: Revenue = $100.0 million
    """
    try:
        rev = obj.get("totalRevenue", None)
    except Exception as e:
        print("Error in getRevenue() function")
        print(e)
        return None
    else:
        return None if rev is None else round(float(rev) * 10**-6, num_dp)


def getRevenueGrowth(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns revenue growth as %
    ex: revenue growth = 15.0%
    """
    try:
        revGrowth = obj.get("revenueGrowth", None)
    except Exception as e:
        print("Error in getRevenueGrowth() function")
        print(e)
        return None
    else:
        return None if revGrowth is None else round(float(revGrowth), num_dp)


def getRevenueGrowthPerShare(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns revenue growth as %
    ex: revenue growth = 15.0%
    """
    try:
        rgs = obj.get("revenuePerShare", None)
    except Exception as e:
        print("Error in getRevenueGrowthPerShare() function")
        print(e)
        return None
    else:
        return None if rgs is None else round(float(rgs), num_dp)


def getFCF(obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int) -> float:
    """
    Returns free cash flow as $ million
    ex: free cash flow = $ 100 million
    """
    try:
        fcf = obj.get("freeCashflow", None)
    except Exception as e:
        print("Error in getFCF() function")
        print(e)
        return None
    else:
        return None if fcf is None else round(float(fcf) * 10**-6, num_dp)


def getFCF_ToMarketCap(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns Free Cash Flow To Market Cap as dimensionless number
    ex: Free Cash Flow To Market Cap = 3
    """
    try:
        fcf = obj.get("freeCashflow", None)
        mc = obj.get("marketCap", None)

        if any(i is None for i in [fcf, mc]):
            return None

        fcf2mc = fcf / mc
    except Exception as e:
        print("Error in getFCF_ToMarketCap() function")
        print(e)
        return None
    else:
        return None if fcf2mc is None else round(float(fcf2mc), num_dp)


def getFCF_PerShare(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns Free CashFlow PerShare as $ / share
    ex: Free CashFlow PerShare = $5 / share
    """
    try:
        fcf = obj.get("freeCashflow", None)
        ns = obj.get("sharesOutstanding", None)

        if any(i is None for i in [fcf, ns]):
            return None

        fcf2ns = fcf / ns
    except Exception as e:
        print("Error in getFCF_PerShare() function")
        print(e)
        return None
    else:
        return None if fcf2ns is None else round(float(fcf2ns), num_dp)


def getFCF_ToEV(obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int) -> float:
    """
    Returns Enterprise Value To Free CashFlow as dimensionless number
    ex: Enterprise Value To Free CashFlow =  10.0
    """
    try:
        fcf = obj.get("freeCashflow", None)
        mc = obj.get("marketCap", None)
        td = obj.get("totalDebt", None)
        tc = obj.get("totalCash", None)

        if any(i is None for i in [fcf, mc, td, tc]):
            return None

        fcf2EV = fcf / (mc + td - tc)
    except Exception as e:
        print("Error in getFCF_ToEV() function")
        print(e)
        return None
    else:
        return None if fcf2EV is None else round(float(fcf2EV), num_dp)


def getOCF(obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int) -> float:
    """
    Returns operating cash flow as $ million
    ex: operating cash flow = $ 100 million
    """
    try:
        ocf = obj.get("operatingCashflow", None)
    except Exception as e:
        print("Error in getOCF() function")
        print(e)
        return None
    else:
        return None if ocf is None else round(float(ocf) * 10**-6, num_dp)


def getOCF_ToRevenue(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns FCF to Revenue as dimensionless number
    ex: FCF / Revenue = 5
    """
    try:
        ocf = obj.get("operatingCashflow", None)
        rev = obj.get("totalRevenue", None)

        if any(i is None for i in [ocf, rev]):
            return None

        ocf2rev = ocf / rev
    except Exception as e:
        print("Error in getOCF_ToRevenue() function")
        print(e)
        return None
    else:
        return None if ocf2rev is None else round(float(ocf2rev), num_dp)


def getOCF_ToMarketCap(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns Operating Cash Flow To Market Cap as dimensionless number
    ex: Operating Cash Flow To Market Cap = 3
    """
    try:
        ocf = obj.get("operatingCashflow", None)
        mc = obj.get("marketCap", None)

        if any(i is None for i in [ocf, mc]):
            return None

        ocf2mc = ocf / mc
    except Exception as e:
        print("Error in getOCF_ToMarketCap() function")
        print(e)
        return None
    else:
        return None if ocf2mc is None else round(float(ocf2mc), num_dp)


def getOCF_PerShare(
    obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int
) -> float:
    """
    Returns Operating CashFlow PerShare as $ / share
    ex: Operating CashFlow PerShare = $5 / share
    """
    try:
        ocf = obj.get("operatingCashflow", None)
        ns = obj.get("sharesOutstanding", None)

        if any(i is None for i in [ocf, ns]):
            return None

        ocf2ns = ocf / ns
    except Exception as e:
        print("Error in getOCF_PerShare() function")
        print(e)
        return None
    else:
        return None if ocf2ns is None else round(float(ocf2ns), num_dp)


def getOCF_ToEV(obj: Dict[str, Optional[Union[int, float, str]]], num_dp: int) -> float:
    """
    Returns Operating CashFlow to Enterprise Value as dimensionless number
    ex: Operating CashFlow to Enterprise Value =  10.0
    """
    try:
        ocf = obj.get("operatingCashflow", None)
        mc = obj.get("marketCap", None)
        td = obj.get("totalDebt", None)
        tc = obj.get("totalCash", None)

        if any(i is None for i in [ocf, mc, td, tc]):
            return None

        ocf2EV = ocf / (mc + td - tc)
    except Exception as e:
        print("Error in getOCF_ToEV() function")
        print(e)
        return None
    else:
        return None if ocf2EV is None else round(float(ocf2EV), num_dp)
