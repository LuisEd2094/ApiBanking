from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import time
import threading
from threading import Lock
from routes.prices_api import check_api
from routes.assets_email import send_investment_purchase_confirmation, send_investment_sale_confirmation
from app import app, db, Session
from models import Trader, User, Transaction, Asset

trader_bp = Blueprint('trader', __name__)
balance_lock = Lock()
BUY_THRESHOLD = 0.9  # 20% drop triggers buy
SELL_THRESHOLD = 1.1  # 20% increase triggers sell


def execute_buy(user, user_asset, asset_price, session, prices):
    budget = user.balance * 0.1  # 10% of the user's balance
    units_to_buy = budget / asset_price
    asset = Asset(user_id=user.id, symbol=user_asset.symbol, quantity=units_to_buy, purchase_price=asset_price, total_investment=budget)
    session.add(asset)
    user.balance -= budget
    new_transaction = Transaction(
        amount=budget,
        transaction_type="ASSET_PURCHASE",
        source_account_number=user.account_number,
    )
    session.add(new_transaction)
    session.commit() 
    send_investment_purchase_confirmation(user, units_to_buy, user_asset.symbol, budget, prices)

def execute_sell(user, user_asset, asset_price, session, prices):
    units_to_sell = user_asset.quantity * 0.1  # 10% of the user's asset quantity
    budget = units_to_sell * asset_price

    new_transaction = Transaction(
        amount=budget,
        transaction_type="ASSET_SELL",
        source_account_number=user.account_number,
    )

    user.balance += budget
    user_asset.quantity -= units_to_sell
    session.add(new_transaction)
    session.commit()
    send_investment_sale_confirmation(user, units_to_sell, user_asset.symbol, budget, user_asset.quantity, prices) 

def trader(trade_user_id):
    """Deduct trade amounts from the user balance at specified intervals."""
    with app.app_context():  # Ensure we have the app context for database access
        session = Session()  # Open a new session within the loop
        while True:
            time.sleep(30)  # Wait for the specified interval
            try:
                with balance_lock:
                    current_prices = check_api()
                    
                    # Re-fetch user by user ID to ensure it's attached to the session
                    user = session.query(User).with_for_update().get(trade_user_id)
                    assets = user.assets
                    for asset in assets:
                        current_asset_price = current_prices.get(asset.symbol)
                        price_difference = current_asset_price / asset.purchase_price 
                        
                        if price_difference < BUY_THRESHOLD:
                            # Create a new transaction record
                            execute_buy(user, asset, current_asset_price, session, current_prices)
                        elif price_difference > SELL_THRESHOLD:
                            execute_sell(user, asset, current_asset_price, session, current_prices)
            finally:
                session.close()


@trader_bp.route('/user-actions/enable-auto-invest', methods=['POST'])
@jwt_required()
def create_trade():
    """Handle trade creation."""
    data = request.get_json()
    if not data or not all(key in data for key in ['pin']):
        return jsonify("All fields are required."), 400
    
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    pin = data.get('pin')
    if not pin:
        return jsonify("PIN cannot be null or empty"), 400
    if not user.check_pin(pin):  # Implement check_pin method in User model
        return jsonify("Invalid PIN."), 403

    # Create a new trade
    new_trade = Trader(
        user_id=user.id,
    )
    
    db.session.add(new_trade)
    db.session.commit()

    # Start the trade deduction in a new thread
    thread = threading.Thread(target=trader, args=(user.id,))
    thread.start()

    return jsonify("Automatic investment enabled successfully."), 200