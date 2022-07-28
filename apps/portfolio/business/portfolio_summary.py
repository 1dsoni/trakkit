import logging

from django.db import transaction

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
    if not tickers:
        tickers = []

    # fetch amounts and quantities
    ticker_amount_volume_map = {}
    for trade in portfolio.trades.filter(ticker__in=tickers):
        if trade.status != 'success':
            continue

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
    portfolio_summary_obj, is_created = PortfolioSummary.objects.get_or_create(
        user_id=user_id,
        portfolio=portfolio,
        ticker=ticker
    )

    if is_created:
        logger.info('created portfolio_summary_obj: %s', portfolio_summary_obj)

    return portfolio_summary_obj


def update_portfolio_ticker_summary(ticker, portfolio_summary_obj):
    logger.info('update summary for ticker: %s', ticker)

    with transaction.atomic():
        logger.info('try take lock and fetch portfolio_summary_obj: %s', portfolio_summary_obj)

        portfolio_summary_obj = PortfolioSummary.objects.filter(
            id=portfolio_summary_obj.id
        ).select_for_update(
            nowait=False
        ).get()

        logger.info('success take lock and fetch portfolio_summary_obj: %s', portfolio_summary_obj)

        portfolio = portfolio_summary_obj.portfolio

        summary = get_portfolio_tickers_summary(portfolio=portfolio, tickers=[ticker])

        logger.info('got new ticker summary: %s', summary)

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
    logger.info('recalculate summary for portfolio: %s', portfolio)

    with transaction.atomic():
        logger.info('try take lock and fetch portfolio: %s', portfolio)

        portfolio = Portfolio.objects.filter(
            id=portfolio.id
        ).select_for_update(
            nowait=False
        ).get()

        tickers = []
        for item in portfolio.trades.all().values('ticker').distinct():
            tickers.append(item.get('ticker'))

        if not tickers:
            return

        summaries = get_portfolio_tickers_summary(portfolio=portfolio, tickers=tickers)

        for k, v in summaries.items():
            ticker = k
            user_id = portfolio.user_id

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
