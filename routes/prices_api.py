import requests
API_URL = "https://faas-lon1-917a94a7.doserverless.co/api/v1/web/fn-e0f31110-7521-4cb9-86a2-645f66eefb63/default/market-prices-simulator"


def fetch_asset_price(asset_symbol):
    prices = check_api()
    if not prices:
        return None
    return prices.get(asset_symbol)

def check_api():
    try:
        # Make a GET request to the API
        response = requests.get(API_URL, timeout=5)
        
        # Check if the response is successful
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None
