from flask import Blueprint, request, jsonify, Response
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

def auto_trade_loop():
    """Continuously check all active traders and execute buy/sell operations."""
    with app.app_context():  # Ensure app context for database access
        session = Session()  # Open a new session for this loop
        while True:
            time.sleep(30)  # Check all trades every 30 seconds
            with balance_lock:
                current_prices = check_api()
                
                # Get all active traders
                active_traders = session.query(Trader).all()
                for trader in active_traders:
                    user = session.query(User).with_for_update().get(trader.user_id)
                    if user:
                        assets = user.assets
                        for asset in assets:
                            current_asset_price = current_prices.get(asset.symbol)
                            price_difference = current_asset_price / asset.purchase_price 
                            
                            if price_difference < BUY_THRESHOLD:
                                execute_buy(user, asset, current_asset_price, session, current_prices)
                            elif price_difference > SELL_THRESHOLD:
                                execute_sell(user, asset, current_asset_price, session, current_prices)
            session.commit()  # Commit any changes made during trading operations

# Start the global auto trade thread only once
auto_trade_thread = threading.Thread(target=auto_trade_loop, daemon=True)
auto_trade_thread.start()

@trader_bp.route('/user-actions/enable-auto-invest', methods=['POST'])
@jwt_required()
def create_trade():
    """Handle trade creation."""
    data = request.get_json()
    if not data or not all(key in data for key in ['pin']):
        return Response("All fields are required.", status=400, mimetype='text/plain')    
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    pin = data.get('pin')
    if not pin:
        return Response("PIN cannot be null or empty", status=400, mimetype='text/plain')    
    if not user.check_pin(pin):  # Implement check_pin method in User model
        return Response("Invalid PIN.", status=403, mimetype='text/plain')    
    # Create a new trader entry to represent the user's auto trade
    new_trade = Trader(
        user_id=user.id,
    )
    
    db.session.add(new_trade)
    db.session.commit()
    return Response("Automatic investment enabled successfully.", status=200, mimetype='text/plain')    
