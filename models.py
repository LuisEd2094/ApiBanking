from datetime import datetime, timezone
from enum import Enum
from sqlalchemy.orm import relationship
import requests
from app import db, bcrypt
import random
import string
import uuid


API_URL = "https://faas-lon1-917a94a7.doserverless.co/api/v1/web/fn-e0f31110-7521-4cb9-86a2-645f66eefb63/default/market-prices-simulator"


def check_api():
    try:
        # Make a GET request to the API
        response = requests.get(API_URL, timeout=5)
        # Check if the response is successful
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        return None


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    account_number = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    balance = db.Column(db.Float, default=0.0)
    pin = db.Column(db.String(128), nullable=True)
    assets = relationship("Asset", back_populates="user")
    suscriptions = relationship("Subscription", back_populates="user")
    trades = relationship("Trader", back_populates="user")  # Updated to match "user" in Trader


    def __init__(self, name, email, phone_number, address, hashed_password):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.hashed_password = hashed_password
    
    @staticmethod
    def validate_password(password):
        # Check password length
        if len(password) < 8:
            return "Password must be at least 8 characters long"
        if len(password) > 128:
            return "Password must be less than 128 characters long"

        # Check for uppercase letter
        if not any(char.isupper() for char in password):
            return "Password must contain at least one uppercase letter"
        if not any(char.islower() for char in password):
            return "Password must contain at least one lowercase letter"
        if any(char.isspace() for char in password):
            return "Password cannot contain whitespace"
        # Check for digit and special character
        digit = any(char.isdigit() for char in password)
        special = any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/~`" for char in password)
        if not digit and not special:
            return "Password must contain at least one digit and one special character"
        elif not digit:
            return "Password must contain at least one digit"
        elif not special:
            return "Password must contain at least one special character"
        return None

    def check_password(self, password):
        if not password:
            return False
        return bcrypt.check_password_hash(self.hashed_password, password)
    
    def check_pin(self, pin):
        if not self.pin:
            return False
        return bcrypt.check_password_hash(self.pin, pin)
    
    def get_networth(self, current_prices):
        prices = current_prices        
        assets_summary = self.get_assets_summary()
        total_asset_value = sum([(info['total_quantity'] * prices.get(asset_symbol, 0.0))  for asset_symbol, info in assets_summary.items()])
        net_worth = self.balance + total_asset_value
        return net_worth

    def get_asset_quantity(self, asset_symbol):
        assets_summary = self.get_assets_summary()
        return assets_summary.get(asset_symbol, {}).get('total_quantity', 0.0)

    #f"{- {asset_symbol}: {asset.quantity:.2f} units purchased at ${asset.purchase_price:.2f}}\n\n"

    def get_current_assets_email(self):
        assets_summary = self.get_assets_summary()
        formatted_assets = []

        for asset_symbol, info in assets_summary.items():
            formatted_assets.append(
                f"- {asset_symbol}: {info['total_quantity']:.2f} units purchased at ${info['total_investment']:.2f}"
            )

        # Join all formatted asset strings with new lines
        return "\n".join(formatted_assets)

    def get_assets_summary(self):
        assets_summary = {}
        
        for asset in self.assets:
            asset_data = asset.to_dict() 
            if asset_data['symbol'] not in assets_summary:
                assets_summary[asset_data['symbol']] = {
                    'total_quantity': 0,
                    'total_investment': 0.0,
                    'purchase_price': asset_data['purchasePrice']
                }
            assets_summary[asset_data['symbol']]['total_quantity'] += asset_data['quantity']
            assets_summary[asset_data['symbol']]['total_investment'] += asset_data['totalInvestment']

        return assets_summary  # Return the summary of assets
    
class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(512), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<TokenBlacklist {self.token}>'
    

class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(100), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    def is_expired(self):
        return datetime.now() > self.expires_at
    
class PasswordResetToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(100), nullable=False) 
    reset_token = db.Column(db.String(36), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    def is_expired(self):
        return datetime.now() > self.expires_at
    

class TransactionType(Enum):
    CASH_DEPOSIT = "CASH_DEPOSIT"
    CASH_WITHDRAWAL = "CASH_WITHDRAWAL"
    CASH_TRANSFER = "CASH_TRANSFER"
    SUBSCRIPTION="SUBSCRIPTION"
    ASSET_PURCHASE="ASSET_PURCHASE"
    ASSET_SELL="ASSET_SELL"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    source_account_number = db.Column(db.String(36), nullable=False)
    target_account_number = db.Column(db.String(36), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "transactionType": self.transaction_type.value,
            "transactionDate": int(self.transaction_date.timestamp() * 1000),
            "sourceAccountNumber": self.source_account_number,
            "targetAccountNumber": self.target_account_number or "N/A"
        }
    @staticmethod
    def new_transaction(amount, transaction_type, source_account_number, target_account_number=None):
        transaction = Transaction(amount=amount, transaction_type=transaction_type, source_account_number=source_account_number, target_account_number=target_account_number)
        db.session.add(transaction)
        db.session.commit()
        return transaction


class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Float, default=0.0) 
    purchase_price = db.Column(db.Float, nullable=False) 
    total_investment = db.Column(db.Float, nullable=False, default=0.0)  
    purchase_date = db.Column(db.DateTime, default=db.func.current_timestamp()) 
    user = relationship("User", back_populates="assets")

    def __repr__(self):
        return f'<Asset {self.symbol}: {self.quantity} units at ${self.purchase_price}>'
    
    def to_dict(self): 
        return {
            "id": self.id,
            "symbol": self.symbol,
            "quantity": self.quantity,
            "purchasePrice": self.purchase_price,
            "totalInvestment": self.total_investment,
            "purchaseDate": int(self.purchase_date.timestamp() * 1000)
        }


class Subscription(db.Model):
    __tablename__ = 'suscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    interval_seconds = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
    last_deducted = db.Column(db.DateTime)
    user = relationship("User", back_populates="suscriptions")

    def __repr__(self):
        return f"<Subscription {self.id} - User {self.user_id}>"


class Trader(db.Model):
    __tablename__ = 'trader'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="trades")

    def __repr__(self):
        return f"<Subscription {self.id} - User {self.user_id}>"
