from flask import Blueprint, request, jsonify
from flask_mail import Message
from app import mail, db
from models import User, Asset, Transaction
from flask_jwt_extended import jwt_required, get_jwt_identity
from routes.prices_api import check_api
from collections import defaultdict
from routes.assets_email import send_investment_purchase_confirmation, send_investment_sale_confirmation

"""/api/account/buy-asset
/api/account/sell-asset """

assets_bp = Blueprint('assets', __name__)

@assets_bp.route('/account/buy-asset', methods=['POST'])
@jwt_required()
def buy_assets():    
    data = request.get_json()
    if not data or not all(key in data for key in ['assetSymbol', 'pin', 'amount']):
        return jsonify({"message": "All fields are required."}), 400
    asset_symbol = data.get('assetSymbol')
    pin = data.get('pin')
    amount = data.get('amount')
    if not asset_symbol or not pin:
        return jsonify({"message": "Invalid request data."}), 400
    try:
        amount = float(data.get('amount'))
        if amount <= 0:
            return jsonify({"message": "Amount must be a positive integer."}), 400
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid amount. Please enter a positive integer."}), 400
    
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify({"msg": "User not found."}), 404
    if not user.check_pin(pin):
        return jsonify({"message": "Invalid PIN."}), 403
    if user.balance < amount:
        return jsonify({"message": "Internal error occurred while purchasing the asset."}), 500   
    
    prices = check_api()
    if not prices:
        return jsonify({"message": "Internal error occurred while purchasing the asset."}), 500

    asset_price = prices.get(asset_symbol)
    if asset_price is None:
        return jsonify({"message": f"Asset '{asset_symbol}' not found."}), 500

    units_purchased = amount / asset_price
    asset = Asset(user_id=user.id, symbol=asset_symbol, quantity=units_purchased, purchase_price=asset_price, total_investment=amount)
    db.session.add(asset)
    user.balance -= amount
    db.session.commit()
    
    Transaction.new_transaction(
        amount=amount,
        transaction_type='ASSET_PURCHASE', 
        source_account_number=user.account_number)

    # Send confirmation email
    send_investment_purchase_confirmation(user, units_purchased, asset_symbol, amount, prices)
    return jsonify("Asset purchase successful."), 200


@assets_bp.route('/account/net-worth', methods=['GET'])
@jwt_required()
def get_net_worth():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify({"message": "User not found."}), 404
    net_worth = user.get_networth(check_api())  # Call method to calculate net worth
    return jsonify(net_worth), 200


@assets_bp.route('/account/assets', methods=['GET'])
@jwt_required()
def get_assets():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify({"message": "User not found."}), 404
    assets_dict = defaultdict(float)
    for asset in user.assets:
        assets_dict[asset.symbol] += asset.quantity
    # Convert the defaultdict to a regular dictionary for JSON serialization
    return jsonify(dict(assets_dict)), 200



@assets_bp.route('/account/sell-asset', methods=['POST'])
@jwt_required()
def sell_asset():
    data = request.get_json()
    # Validate request body
    if not data or not all(key in data for key in ['assetSymbol', 'pin', 'quantity']):
        return jsonify({"msg": "Internal error occurred while selling the asset."}), 500
    
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()

    pin = data.get('pin')
    
    quantity = data.get('quantity')

    asset_symbol = data.get('assetSymbol')

    if not user:
        return jsonify({"msg": "Internal error occurred while selling the asset."}), 500
    if not user.check_pin(pin):
        return jsonify({"msg": "Invalid PIN."}), 403
    try:
        quantity = float(quantity)
        if quantity <= 0:
            return jsonify({"msg": "Internal error occurred while selling the asset."}), 500
    except (ValueError, TypeError):
        return jsonify({"msg": "Internal error occurred while selling the asset."}), 500
    # Find the asset
    assets = Asset.query.filter(
        Asset.user_id == user.id,
        Asset.symbol == asset_symbol
    ).order_by(Asset.purchase_price.asc()).all()    
    if not assets:
        return jsonify({"msg": "Asset not found."}), 404
    total_quantity = sum(asset.quantity for asset in assets)

    if total_quantity < quantity:
        return jsonify({"msg": "Internal error occurred while selling the asset."}), 500

    # Calculate sale details
    total_gain_loss = 0
    quantity_remaining = quantity

    prices = check_api()

    for asset in assets:
        if quantity_remaining <= 0:
            break
        sale_price = prices.get(asset.symbol)
        amount = 0.0
        if asset.quantity >= quantity_remaining:
            # If the asset has enough quantity to cover the sale
            total_gain_loss += (sale_price - asset.purchase_price) * quantity_remaining
            asset.quantity -= quantity_remaining
            amount = sale_price * quantity_remaining
            user.balance += amount
            quantity_remaining = 0
        else:
            # Sell all of this asset
            total_gain_loss += (sale_price - asset.purchase_price) * asset.quantity
            quantity_remaining -= asset.quantity
            amount = sale_price * asset.quantity
            user.balance += amount
            asset.quantity = 0  # All sold
        Transaction.new_transaction(
            amount=amount,
            transaction_type='ASSET_SELL', 
            source_account_number=user.account_number)
    db.session.commit()

    # Send confirmation email
    send_investment_sale_confirmation(user, quantity, asset_symbol, total_gain_loss, total_quantity, prices)
    return jsonify({"msg": "Asset sale successful."}), 200

