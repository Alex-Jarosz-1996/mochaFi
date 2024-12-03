import unittest
from unittest.mock import patch, MagicMock
from mochaFi.backend.app import app, db, StockModel, StockPriceHistoryModel
from datetime import datetime

class TestStockEndpoints(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Push the application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Create all the tables in the in-memory SQLite database
        db.create_all()

    def tearDown(self):
        # Remove the session and drop all tables after each test
        db.session.remove()
        db.drop_all()

        # Pop the application context
        self.app_context.pop()

    @patch('app.StockModel.query.filter_by')
    @patch('app.db.session.add')
    @patch('app.db.session.commit')
    def test_add_stock_success(self, mock_commit, mock_add, mock_filter_by):
        # Mocking StockModel.query.filter_by to return None (indicating stock does not exist)
        mock_filter_by.return_value.first.return_value = None

        # Sample payload for adding stock
        payload = {
            "stock": "AAPL",
            "country": "US"
        }

        # Sending POST request to the /stock endpoint
        response = self.client.post('/stock', json=payload)

        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"Stock added successfully", response.data)
        mock_add.assert_called_once()
        mock_commit.assert_called_once()

    # @patch('app.StockModel.query.filter_by')
    # def test_add_stock_conflict(self, mock_filter_by):
    #     # Mocking StockModel.query.filter_by to return an existing stock (conflict)
    #     mock_filter_by.return_value.first.return_value = StockModel()

    #     payload = {
    #         "stock": "AAPL",
    #         "country": "US"
    #     }

    #     response = self.client.post('/stock', json=payload)

    #     self.assertEqual(response.status_code, 409)
    #     self.assertIn(b"Stock already exists", response.data)

    @patch('app.StockModel.query.all')
    def test_get_stocks(self, mock_query_all):
        # Mocking the response of StockModel.query.all()
        mock_query_all.return_value = [
            StockModel(id=1, code="AAPL", country="US", price=150.0, marketCap=2000000.0)
        ]

        response = self.client.get('/stocks')

        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'AAPL', response.data)
        # self.assertIn(b'150.0', response.data)

    @patch('app.StockModel.query.get')
    @patch('app.db.session.commit')
    @patch('app.db.session.delete')
    def test_delete_stock_success(self, mock_delete, mock_commit, mock_get):
        # Mocking StockModel.query.get to return a stock object
        mock_get.return_value = StockModel(id=1, code="AAPL", country="US")

        # Sample payload for adding stock
        payload = {
            "stock": "AAPL",
            "country": "US"
        }

        # Sending POST request to the /stock endpoint
        response = self.client.post('/stock', json=payload)
        
        response = self.client.delete('/stock/1')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Stock deleted successfully', response.data)

    @patch('app.StockModel.query.get')
    def test_delete_stock_not_found(self, mock_get):
        # Mocking StockModel.query.get to return None (stock not found)
        mock_get.return_value = None

        response = self.client.delete('/stock/999')

        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Stock not found', response.data)

    @patch('app.db.session.commit')
    @patch('app.db.session.query')
    def test_delete_all_stocks(self, mock_query, mock_commit):
        response = self.client.delete('/stocks')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Deleted all stocks successfully', response.data)
        mock_commit.assert_called_once()

    
    def test_add_stock_prices_success(self):
        # Sample payload
        payload = {
            "code": "AAPL",
            "country": "US",
            "time_period": "1y",
            "time_interval": "1d"
        }

        response = self.client.post('/stock_price', json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Stock prices added successfully for AAPL', response.data)
        # mock_add.assert_called()
        # mock_commit.assert_called_once()

    # @patch('app.StockModel.query.filter_by')
    # def test_get_stock_prices(self, mock_filter_stock):
    #     # Mock stock query to return a stock
    #     mock_filter_stock.return_value.first.return_value = StockModel(code="AAPL", country="US")

    #     # Mock stock price query to return price history
    #     with patch('app.StockPriceHistoryModel.query.filter_by') as mock_filter_prices:
    #         mock_filter_prices.return_value.order_by.return_value.all.return_value = [
    #             StockPriceHistoryModel(code="AAPL", date=datetime.today().strftime('%Y-%m-%d'), open_price=100.0, close_price=102.0)
    #         ]

    #         response = self.client.get('/stock_price/AAPL')

    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn(b'prices', response.data)
    #         self.assertIn(b'AAPL', response.data)
    #         self.assertIn(b'2023-01-01', response.data)

    @patch('app.db.session.commit')
    @patch('app.db.session.query')
    def test_delete_all_stock_price_histories(self, mock_query, mock_commit):
        response = self.client.delete('/stock_price_delete')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Deleted all stock price histories successfully', response.data)
        mock_commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
