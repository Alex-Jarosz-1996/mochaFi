from sqlalchemy.exc import IntegrityError

from db_service.db import DB_Client
from models.stock_model import StockModel
from yf_service.stats.utils.controller import StockController

class StockDB_Client(DB_Client):
    def __init__(self):
        super().__init__()

    
    def get_all_stocks(self):
        """
        Retrieves all stocks from the database.
        """
        try:
            all_stocks = self.session.query(StockModel).all()

            return all_stocks if all_stocks else None

        except Exception as e:
            self.session.rollback()
            raise e

    
    def add_single_stock(self, json_data: dict):
        """
        Adds a single stock to the database if it does not already exist.
        """
        try:
            code = json_data.get("stock")
            country = json_data.get("country")

            if not code or not country:
                raise ValueError("Both 'code' and 'country' are required.")
            
            stock_obj = StockController(code, country)
            
            new_stock = StockModel(
                code=stock_obj.si.ticker,
                country=stock_obj.si.country,
                price=getattr(stock_obj.si.stockPriceMetrics, 'price', None),
                marketCap=getattr(stock_obj.si.stockPriceMetrics, 'marketCap', None),
                numSharesAvail=getattr(stock_obj.si.stockPriceMetrics, 'numSharesAvail', None),
                yearlyLowPrice=getattr(stock_obj.si.stockPriceMetrics, 'yearlyLowPrice', None),
                yearlyHighPrice=getattr(stock_obj.si.stockPriceMetrics, 'yearlyHighPrice', None),
                fiftyDayMA=getattr(stock_obj.si.stockPriceMetrics, 'fiftyDayMA', None),
                twoHundredDayMA=getattr(stock_obj.si.stockPriceMetrics, 'twoHundredDayMA', None),
                acquirersMultiple=getattr(stock_obj.si.valueMetrics, 'acquirersMultiple', None),
                currentRatio=getattr(stock_obj.si.valueMetrics, 'currentRatio', None),
                enterpriseValue=getattr(stock_obj.si.valueMetrics, 'enterpriseValue', None),
                eps=getattr(stock_obj.si.valueMetrics, 'eps', None),
                evToEBITDA=getattr(stock_obj.si.valueMetrics, 'evToEBITDA', None),
                evToRev=getattr(stock_obj.si.valueMetrics, 'evToRev', None),
                peRatioTrail=getattr(stock_obj.si.valueMetrics, 'peRatioTrail', None),
                peRatioForward=getattr(stock_obj.si.valueMetrics, 'peRatioForward', None),
                priceToSales=getattr(stock_obj.si.valueMetrics, 'priceToSales', None),
                priceToBook=getattr(stock_obj.si.valueMetrics, 'priceToBook', None),
                dividendYield=getattr(stock_obj.si.dividendMetrics, 'dividendYield', None),
                dividendRate=getattr(stock_obj.si.dividendMetrics, 'dividendRate', None),
                exDivDate=getattr(stock_obj.si.dividendMetrics, 'exDivDate', None),
                payoutRatio=getattr(stock_obj.si.dividendMetrics, 'payoutRatio', None),
                bookValPerShare=getattr(stock_obj.si.balanceSheetMetrics, 'bookValPerShare', None),
                cash=getattr(stock_obj.si.balanceSheetMetrics, 'cash', None),
                cashPerShare=getattr(stock_obj.si.balanceSheetMetrics, 'cashPerShare', None),
                cashToMarketCap=getattr(stock_obj.si.balanceSheetMetrics, 'cashToMarketCap', None),
                cashToDebt=getattr(stock_obj.si.balanceSheetMetrics, 'cashToDebt', None),
                debt=getattr(stock_obj.si.balanceSheetMetrics, 'debt', None),
                debtToMarketCap=getattr(stock_obj.si.balanceSheetMetrics, 'debtToMarketCap', None),
                debtToEquityRatio=getattr(stock_obj.si.balanceSheetMetrics, 'debtToEquityRatio', None),
                returnOnAssets=getattr(stock_obj.si.balanceSheetMetrics, 'returnOnAssets', None),
                returnOnEquity=getattr(stock_obj.si.balanceSheetMetrics, 'returnOnEquity', None),
                ebitda=getattr(stock_obj.si.incomeRelatedMetrics, 'ebitda', None),
                ebitdaPerShare=getattr(stock_obj.si.incomeRelatedMetrics, 'ebitdaPerShare', None),
                earningsGrowth=getattr(stock_obj.si.incomeRelatedMetrics, 'earningsGrowth', None),
                grossProfit=getattr(stock_obj.si.incomeRelatedMetrics, 'grossProfit', None),
                grossProfitPerShare=getattr(stock_obj.si.incomeRelatedMetrics, 'grossProfitPerShare', None),
                netIncome=getattr(stock_obj.si.incomeRelatedMetrics, 'netIncome', None),
                netIncomePerShare=getattr(stock_obj.si.incomeRelatedMetrics, 'netIncomePerShare', None),
                operatingMargin=getattr(stock_obj.si.incomeRelatedMetrics, 'operatingMargin', None),
                profitMargin=getattr(stock_obj.si.incomeRelatedMetrics, 'profitMargin', None),
                revenue=getattr(stock_obj.si.incomeRelatedMetrics, 'revenue', None),
                revenueGrowth=getattr(stock_obj.si.incomeRelatedMetrics, 'revenueGrowth', None),
                revenuePerShare=getattr(stock_obj.si.incomeRelatedMetrics, 'revenuePerShare', None),
                fcf=getattr(stock_obj.si.cashFlowMetrics, 'fcf', None),
                fcfToMarketCap=getattr(stock_obj.si.cashFlowMetrics, 'fcfToMarketCap', None),
                fcfPerShare=getattr(stock_obj.si.cashFlowMetrics, 'fcfPerShare', None),
                fcfToEV=getattr(stock_obj.si.cashFlowMetrics, 'fcfToEV', None),
                ocf=getattr(stock_obj.si.cashFlowMetrics, 'ocf', None),
                ocfToRevenueRatio=getattr(stock_obj.si.cashFlowMetrics, 'ocfToRevenueRatio', None),
                ocfToMarketCap=getattr(stock_obj.si.cashFlowMetrics, 'ocfToMarketCap', None),
                ocfPerShare=getattr(stock_obj.si.cashFlowMetrics, 'ocfPerShare', None),
                ocfToEV=getattr(stock_obj.si.cashFlowMetrics, 'ocfToEV', None)
            )
            
            self.session.add(new_stock)
            self.session.commit()
            return True

        except IntegrityError as ie:
            self.session.rollback()
            raise ie
        
        except TypeError as te:
            self.session.rollback()
            raise te
        
        except ValueError as ve:
            self.session.rollback()
            raise ve

        except Exception as e:
            self.session.rollback()
            raise e


    def delete_all_stocks(self) -> bool:
        """
        Removes all stocks from the database.
        """
        try:
            rows_deleted = self.session.query(StockModel).delete()
            self.session.commit()

            return rows_deleted > 0

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to delete all stocks: {e}")

    
    def delete_single_stock(self, stock_id: int) -> bool:
        """
        Removes a single stock from the database.
        """
        try:
            stock = self.session.query(StockModel).get(stock_id)

            if not stock:
                return False
            
            self.session.delete(stock)
            self.session.commit()

            return True

        except Exception as e:
            self.session.rollback()
            raise Exception(f"Failed to delete single stock: {e}")

stockDB_Client = StockDB_Client()