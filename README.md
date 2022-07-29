# trakkit 
## Portfolio tracker
A simple django app hosted on heroku that demonstrates storage of user trades and the updating of the portfolio trade summary in an atomic transaction under a row level db lock to prevent race conditions while updating the portfolio summary

## Additional improvements
    - Add more test cases
    - Implement live ticker buy value using redis as the storage and updating redis via crons
    - Modify the service as a platform for managing portfolio tracking requirements of different clients

### api docs can be found at: https://trackit-pro.herokuapp.com/docs/

# Some api examples
### Create portfolio

    Request:
    curl --location --request POST 'https://trackit-pro.herokuapp.com/api/v1/portfolio/' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "user_id": "some-user-uuid",
            "name": "name-of-the-portfolio"
        }'
    
    Response:
    {
        "id": 1,
        "user_id": "some-user-uuid",
        "name": "name-of-the-portfolio",
        "created_at": "2022-07-29T08:12:12.797643Z",
        "updated_at": "2022-07-29T08:12:12.797685Z"
    }

### Create trade

    Request:
    curl --location --request POST 'https://trackit-pro.herokuapp.com/api/v1/trade/' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "ref_id": "ref_id",
            "user_id": "some-user-uuid",
            "portfolio": "portfolio.id",
            "trade_type": 1,
            "security_type": "stock",
            "ticker": "GODREJIND",
            "volume": 10,
            "amount": 100,
            "status": "success"
        }'
    
    Response:
    {
        "ref_id": "ref_id",
        "user_id": "some-user-uuid",
        "portfolio": "portfolio.id",
        "trade_type": 1,
        "security_type": "stock",
        "ticker": "GODREJIND",
        "volume": 10,
        "amount": "100.00",
        "status": "success",
        "created_at": "2022-07-29T08:13:10.869359Z",
        "updated_at": "2022-07-29T08:13:10.869394Z"
    }

### Update trade

    Request:
    curl --location --request PATCH 'https://trackit-pro.herokuapp.com/api/v1/trade/ref_id/' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "volume": 100,
            "amount": "1000.00",
            "status": "failed"
        }'

    Response:
    {
        "ref_id": "ref_id",
        "user_id": "some-user-uuid",
        "portfolio": "portfolio.id",
        "trade_type": 1,
        "security_type": "stock",
        "ticker": "GODREJIND",
        "volume": 100,
        "amount": "1000.00",
        "status": "failed",
        "created_at": "2022-07-29T08:13:10.869359Z",
        "updated_at": "2022-07-29T08:13:10.869394Z"
    }


### Fetch portfolio summary

    Request:
    curl --location --request GET 'https://trackit-pro.herokuapp.com/api/v1/portfolio-summary/?user_id=u-1&portfolio_id=1'
    
    Response:
    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "ticker": "AMZN",
                "average_amount": "1000.00",
                "volume": 100,
                "updated_at": "2022-07-28T20:26:41.710508Z"
            },
            {
                "ticker": "GODREJIND",
                "average_amount": "438.57",
                "volume": 7,
                "updated_at": "2022-07-28T21:54:15.041245Z"
            }
        ]
    }


### Fetch portfolio returns
    
    Request
    curl --location --request GET 'https://trackit-pro.herokuapp.com/api/v1/portfolio/1/cumulative-returns/'
    
    Response:
    {
        "return_value": -15000.0
    }