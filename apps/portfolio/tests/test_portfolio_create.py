import json

from django.test import TestCase


class PortfolioTestSuite(TestCase):

    def test_create_portfolio(self):
        endpoint = '/api/v1/portfolio/'
        data = {
            'name': 'test-portfolio-name-1',
            'user_id': 'u-1'
        }

        response = self.client.post(path=endpoint, data=json.dumps(data), content_type="application/json")
        assert response.status_code == 201

    def test_create_unique_portfolio(self):
        endpoint = '/api/v1/portfolio/'
        data = {
            'name': 'test-portfolio-name-2',
            'user_id': 'u-1'
        }
        response = self.client.post(path=endpoint, data=json.dumps(data), content_type="application/json")

        assert response.status_code == 201

        data = {
            'name': 'test-portfolio-name-2',
            'user_id': 'u-1'
        }

        response = self.client.post(path=endpoint, data=json.dumps(data), content_type="application/json")
        assert response.status_code == 400
