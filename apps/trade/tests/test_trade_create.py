import json
import uuid

from django.test import TestCase

from apps.portfolio.constants import TradeType, SecurityType
from apps.portfolio.tests.factories.portfolio_factory import PortfolioFactory
from apps.portfolio.tests.factories.ticker_factory import create_random_ticker_order


class TradeTestSuite(TestCase):

    def setUp(self) -> None:
        self.portfolio = PortfolioFactory.create_batch(size=1)[0]

    def test_create_trade(self):
        endpoint = '/api/v1/trade/'

        user_id = self.portfolio.user_id
        portfolio_id = self.portfolio.id
        order_data = create_random_ticker_order()
        ticker = order_data.get('ticker')
        amount = order_data.get('amount')
        volume = order_data.get('volume')

        data = {
            "user_id": user_id,
            "portfolio": portfolio_id,
            "trade_type": TradeType.BUY,
            "security_type": SecurityType.stock,
            "ticker": ticker,
            "volume": volume,
            "amount": amount,
            "status": "success"
        }

        response = self.client.post(path=endpoint, data=json.dumps(data), content_type="application/json")
        assert response.status_code == 201

    def test_create_unique_trade(self):
        endpoint = '/api/v1/trade/'

        user_id = self.portfolio.user_id
        portfolio_id = self.portfolio.id
        order_data = create_random_ticker_order()
        ticker = order_data.get('ticker')
        amount = order_data.get('amount')
        volume = order_data.get('volume')

        ref_id = str(uuid.uuid4())
        data = {
            "ref_id": ref_id,
            "user_id": user_id,
            "portfolio": portfolio_id,
            "trade_type": TradeType.BUY,
            "security_type": SecurityType.stock,
            "ticker": ticker,
            "volume": volume,
            "amount": amount,
            "status": "success"
        }

        response = self.client.post(path=endpoint, data=json.dumps(data), content_type="application/json")
        assert response.status_code == 201

        response = self.client.post(path=endpoint, data=json.dumps(data), content_type="application/json")
        assert response.status_code == 400
