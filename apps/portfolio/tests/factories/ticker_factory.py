import random


def get_random_ticker():
    return random.choice(['WIPRO', 'TCS', 'AMZN', 'GODREJIND'])


def get_random_amount():
    return round(random.random() * 100 * random.randint(1, 3), 2)


def get_random_volume():
    return 100 * random.randint(1, 3)


def create_random_ticker_order():
    return {
        'ticker': get_random_ticker(),
        'amount': get_random_amount(),
        'volume': get_random_volume()
    }
