from flask import Blueprint, jsonify
from routes.prices_api import check_api


"""/market/prices
/market/prices/{symbol}
"""

market_bp = Blueprint('market', __name__)

@market_bp.route('/market/prices', methods=['GET'])
def get_prices():
    prices = check_api()
    if not prices:
        return jsonify({"message": "Error fetching asset prices."}), 500    
    return jsonify(prices), 200

@market_bp.route('/market/prices/<string:symbol>', methods=['GET'])
def get_market_price(symbol):
    # Here, you would typically make a request to your price API
    # For demonstration purposes, let's return a mock response
    prices = check_api()
    if not prices:
        return jsonify({"message": "Error fetching asset prices."}), 500 
    
    price = prices.get(symbol.upper())  # Get the price for the symbol, case insensitive
    
    if price is not None:
        return jsonify(price), 200
    else:
        return jsonify({"message": "Symbol not found."}), 404


