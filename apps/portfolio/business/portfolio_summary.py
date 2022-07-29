import logging

from django.db import transaction

from apps.portfolio.constants import TradeStatus, TradeType
from apps.portfolio.models import Portfolio
from apps.portfolio.models import PortfolioSummary

logger = logging.getLogger(__name__)


def get_weighted_average(amounts):
    """
    Returns average_amount, total_volume
    """
    total_sum = 0
    total_volume = 0
    for item in amounts:
        amount, volume = item
        total_sum += amount * volume
        total_volume += volume

    if not total_volume:
        return 0, 0

    return round(total_sum / total_volume, 2), total_volume


def get_portfolio_tickers_summary(portfolio: Portfolio, tickers: list) -> dict:
    """
    given a list of tickers and a portfolio calculate their weighted average

    1. fetch all the trades which are:
        BUY, success and contains tickers from the list of tickers in params
    2. calculate their weighted average
    3. return a map of tickers with their calculated avg amount and volume

    Params:
        portfolio: Portfolio
        tickers: list of ticker symbol eg: [TCS, WIPRO]

    Returns:
        portfolio summary object: PortfolioSummary
    """
    if not tickers:
        tickers = []

    # fetch amounts and quantities
    ticker_amount_volume_map = {}
    for trade in portfolio.trades.filter(ticker__in=tickers,
                                         status=TradeStatus.success,
                                         trade_type=TradeType.BUY):
        if trade.ticker in ticker_amount_volume_map:
            ticker_amount_volume_map[trade.ticker].append((trade.amount, trade.volume))
        else:
            ticker_amount_volume_map[trade.ticker] = [(trade.amount, trade.volume)]

    # aggregate
    summary = {}
    for k, v in ticker_amount_volume_map.items():
        avg_amount, total_volume = get_weighted_average(v)
        summary[k] = {'amount': avg_amount,
                      'volume': total_volume}

    return summary


def fetch_portfolio_ticker_summary_obj(user_id, portfolio, ticker):
    """
    fetch or create new portfolio_summary_obj
    using this to always have a row to take a lock on when updating the portfolio_summary on any trade

    Returns:
        portfolio summary object: PortfolioSummary
    """
    portfolio_summary_obj, is_created = PortfolioSummary.objects.get_or_create(
        user_id=user_id,
        portfolio=portfolio,
        ticker=ticker
    )

    if is_created:
        logger.debug('created portfolio_summary_obj: %s', portfolio_summary_obj)

    return portfolio_summary_obj


def update_portfolio_ticker_summary(ticker, portfolio_summary_obj):
    """
    given a ticker and a portfolio try to recalculate the summary and update in db

    1. takes lock on the portfolio summary row corresponding to the ticker to avoid race conditions on concurrent trades
    2. attempts to perform concurrent updates on a (user, portfolio, ticker) will throw error; this is to be handled at client
    3. calculates the weighted average for the given ticker and updates in db

    Params:
        ticker: ticker symbol eg: TCS
        portfolio_summary_obj: PortfolioSummary

    Returns:
        portfolio summary object: PortfolioSummary
    """
    logger.debug('update summary for ticker: %s', ticker)

    with transaction.atomic():
        logger.debug('try take lock on fetch portfolio_summary_obj: %s', portfolio_summary_obj)

        portfolio_summary_obj = PortfolioSummary.objects.filter(
            id=portfolio_summary_obj.id
        ).select_for_update(
            nowait=True
        ).get()

        logger.debug('success take lock on fetch portfolio_summary_obj: %s', portfolio_summary_obj)

        portfolio = portfolio_summary_obj.portfolio

        summary = get_portfolio_tickers_summary(portfolio=portfolio, tickers=[ticker])

        logger.debug('got new ticker summary: %s', summary)

        ticker_summary = summary.get(ticker)
        if not ticker_summary:
            return

        average_amount = ticker_summary.get('amount')
        volume = ticker_summary.get('volume')

        portfolio_summary_obj.average_amount = average_amount or 0
        portfolio_summary_obj.volume = volume

        portfolio_summary_obj.save(update_fields=['average_amount', 'volume', 'updated_at'])

    return portfolio_summary_obj


def recalculate_portfolio_ticker_summary(portfolio: Portfolio):
    """
    given a portfolio try to recalculate the summary of all tickers
     - to be used for testing
     - ideally on every trade the summary gets updated as a single transaction (atomic operation)
    """
    logger.debug('recalculate summary for portfolio: %s', portfolio)

    with transaction.atomic():
        logger.debug('try lock on portfolio: %s', portfolio)

        portfolio = Portfolio.objects.filter(
            id=portfolio.id
        ).select_for_update(
            nowait=False
        ).get()

        logger.debug('got lock on portfolio: %s', portfolio)

        user_id = portfolio.user_id
        for item in portfolio.trades.all().values('ticker').distinct():
            ticker = item.get('ticker')

            with transaction.atomic():
                portfolio_ticker_summary_obj = fetch_portfolio_ticker_summary_obj(
                    user_id=user_id,
                    portfolio=portfolio,
                    ticker=ticker
                )

                transaction.on_commit(
                    lambda: update_portfolio_ticker_summary(ticker, portfolio_ticker_summary_obj)
                )

    return portfolio
