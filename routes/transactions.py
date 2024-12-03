from flask import Blueprint, request, jsonify
from models import  User, Transaction
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_



transactions_bp = Blueprint('transactions', __name__)
"""/api/account/deposit
/api/account/withdraw
/api/account/fund-transfer
/api/account/transactions
"""

@transactions_bp.route('/account/deposit', methods=['POST'])
@jwt_required()
def deposit():
    data = request.get_json()
    if not data or not all(key in data for key in ['pin', 'amount']):
        return jsonify("All fields are required."), 400
    
    pin = data.get('pin')
    amount = data.get('amount')
    if not pin or not amount:
        return jsonify("PIN and amount are required."), 400
    try:
        amount = float(data.get('amount'))
        if amount <= 0:
            return jsonify("Amount must be a positive integer."), 400
    except (ValueError, TypeError):
        return jsonify("Invalid amount. Please enter a positive integer."), 400
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify("User not found."), 404
    if not user.check_pin(pin):
        return jsonify("Invalid PIN"), 403
    user.balance += amount
    db.session.commit()
    Transaction.new_transaction(amount=amount, transaction_type='CASH_DEPOSIT', source_account_number=user.account_number)
    return jsonify({"msg": "Cash deposited successfully"}), 200


@transactions_bp.route('/account/withdraw', methods=['POST'])
@jwt_required()
def withdraw():
    data = request.get_json()
    if not data or not all(key in data for key in ['pin', 'amount']):
            return jsonify("All fields are required."), 400
    pin = data.get('pin')
    amount = data.get('amount')
    if not pin or not amount:
        return jsonify("PIN and amount are required."), 400
    try:
        amount = float(data.get('amount'))
        if amount <= 0:
            return jsonify("Amount must be a positive integer."), 400
    except (ValueError, TypeError):
        return jsonify("Invalid amount. Please enter a positive integer."), 400
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify("User not found."), 404
    if not user.check_pin(pin):
        return jsonify("Invalid PIN"), 403
    if user.balance < amount:
        return jsonify("Insufficient balance"), 400
    user.balance -= amount
    Transaction.new_transaction(amount=amount, transaction_type='CASH_WITHDRAWAL', source_account_number=user.account_number)
    db.session.commit()
    return jsonify({"msg": "Cash withdrawn successfully"}), 200


@transactions_bp.route('/account/fund-transfer', methods=['POST'])
@jwt_required()
def fund_transfer():
    data = request.get_json()
    if not data or not all(key in data for key in ['pin', 'amount', 'targetAccountNumber']):
            return jsonify("All fields are required."), 400
    pin = data.get('pin')
    amount = data.get('amount')
    target_account_number = data.get('targetAccountNumber')
    if not pin or not amount or not target_account_number:
        return jsonify("PIN, amount and target account number are required."), 400
    try:
        amount = float(data.get('amount'))
        if amount <= 0:
            return jsonify("Amount must be a positive integer."), 400
    except (ValueError, TypeError):
        return jsonify("Invalid amount. Please enter a positive integer."), 400
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify("User not found."), 404
    if not user.check_pin(pin):
        return jsonify("Invalid PIN"), 403
    if user.balance < amount:
        return jsonify("Insufficient balance"), 400
    
    target_user = User.query.filter_by(account_number=target_account_number).first()
    if not target_user:
        return jsonify("Target account not found."), 404
    
    user.balance -= amount
    target_user.balance += amount
    db.session.commit()
    Transaction.new_transaction(amount=amount, transaction_type='CASH_TRANSFER', source_account_number=user.account_number, target_account_number=target_user.account_number)
    return jsonify({"msg": "Fund transferred successfully"}), 200


@transactions_bp.route('/account/transactions', methods=['GET'])
@jwt_required()
def transaction_history():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify("User not found."), 404
    
    transactions = Transaction.query.filter(or_(
            Transaction.source_account_number == user.account_number,
            Transaction.target_account_number == user.account_number
        )
    ).all()    
    return jsonify([transaction.to_dict() for transaction in transactions]), 200