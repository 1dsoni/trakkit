import logging

from apps.portfolio.business.live_ticker import get_live_ticker_buy_value
from apps.portfolio.models import Portfolio

logger = logging.getLogger(__name__)


def fetch_portfolio_ticker_cumulative_returns(portfolio: Portfolio):
    logger.debug('fetch_portfolio_ticker_cumulative_summary for portfolio: %s', portfolio)

    return_value = 0

    for summary in portfolio.summary.filter(average_amount__gt=0,
                                            volume__gt=0):
        average_amount = summary.average_amount
        volume = summary.volume

        ticker = summary.ticker
        live_ticker_buy_value = get_live_ticker_buy_value(ticker)

        return_value += (live_ticker_buy_value - average_amount) * volume

    return return_value
