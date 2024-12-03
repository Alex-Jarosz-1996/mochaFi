import unittest
from datetime import date
from sqlalchemy import text
from mochaFi.backend.app import app, db, StockModel, StockPriceHistoryModel


class TestModels(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_stock(self):
        stock = StockModel(
            code="AAPL",
            country="US",
            price=150.0,
            marketCap=2_000_000_000_000.0,
            yearlyLowPrice=130.0,
            yearlyHighPrice=160.0
        )
        db.session.add(stock)
        db.session.commit()

        # Query stock and assert values
        result = StockModel.query.filter_by(code="AAPL").first()
        self.assertIsNotNone(result)
        self.assertEqual(result.code, "AAPL")
        self.assertEqual(result.country, "US")
        self.assertEqual(result.price, 150.0)
        self.assertEqual(result.marketCap, 2_000_000_000_000.0)
        self.assertEqual(result.yearlyLowPrice, 130.0)
        self.assertEqual(result.yearlyHighPrice, 160.0)

    def test_create_stock_price_history(self):
        # Create a stock
        stock = StockModel(code="AAPL", country="US")
        db.session.add(stock)
        db.session.commit()

        # Add stock price history
        history = StockPriceHistoryModel(
            code="AAPL",
            date=date(2023, 10, 1),
            open_price=140.0,
            high_price=145.0,
            low_price=138.0,
            close_price=143.0,
            adj_close_price=143.0,
            volume=1_000_000
        )
        db.session.add(history)
        db.session.commit()

        # Query stock price history
        result = StockPriceHistoryModel.query.filter_by(code="AAPL").first()
        self.assertIsNotNone(result)
        self.assertEqual(result.code, "AAPL")
        self.assertEqual(result.open_price, 140.0)
        self.assertEqual(result.high_price, 145.0)
        self.assertEqual(result.low_price, 138.0)
        self.assertEqual(result.close_price, 143.0)
        self.assertEqual(result.adj_close_price, 143.0)
        self.assertEqual(result.volume, 1_000_000)

    def test_stock_price_history_relationship(self):
        # Create stock and price history
        stock = StockModel(code="AAPL", country="US")
        db.session.add(stock)
        db.session.commit()

        history = StockPriceHistoryModel(
            code="AAPL",
            date=date(2023, 10, 1),
            open_price=140.0,
            high_price=145.0,
            low_price=138.0,
            close_price=143.0,
            adj_close_price=143.0,
            volume=1_000_000
        )
        db.session.add(history)
        db.session.commit()

        # Test relationship between StockModel and StockPriceHistoryModel
        result = StockModel.query.filter_by(code="AAPL").first()
        self.assertEqual(result.price_history.count(), 1)
        self.assertEqual(result.price_history.first().volume, 1_000_000)

    def test_unique_constraint_on_stock_price_history(self):
        # Create a stock
        stock = StockModel(code="AAPL", country="US")
        db.session.add(stock)
        db.session.commit()

        # Add first price history entry
        history1 = StockPriceHistoryModel(
            code="AAPL",
            date=date(2023, 10, 1),
            open_price=140.0,
            high_price=145.0,
            low_price=138.0,
            close_price=143.0,
            adj_close_price=143.0,
            volume=1_000_000
        )
        db.session.add(history1)
        db.session.commit()

        # Try adding a duplicate entry (same code and date)
        history2 = StockPriceHistoryModel(
            code="AAPL",
            date=date(2023, 10, 1),
            open_price=145.0,
            high_price=150.0,
            low_price=140.0,
            close_price=148.0,
            adj_close_price=148.0,
            volume=500_000
        )

        # Expecting exception due to unique constraint violation
        with self.assertRaises(Exception):
            db.session.add(history2)
            db.session.commit()

    def test_delete_stock_deletes_price_history(self):
        # Create stock and associated price history
        stock = StockModel(code="AAPL", country="US")
        db.session.add(stock)
        db.session.commit()

        history = StockPriceHistoryModel(
            code="AAPL",
            date=date(2023, 10, 1),
            open_price=140.0,
            high_price=145.0,
            low_price=138.0,
            close_price=143.0,
            adj_close_price=143.0,
            volume=1_000_000
        )
        db.session.add(history)
        db.session.commit()

        # Delete stock
        db.session.delete(stock)
        db.session.commit()

        # Verify stock and price history are deleted
        self.assertIsNone(StockModel.query.filter_by(code="AAPL").first())
        self.assertIsNone(StockPriceHistoryModel.query.filter_by(code="AAPL").first())


if __name__ == '__main__':
    unittest.main()
