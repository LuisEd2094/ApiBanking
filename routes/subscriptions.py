# imports and other setup remain the same
from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
import time
import threading
from threading import Lock
from datetime import datetime, timedelta, timezone
from app import app, db, Session
from models import Subscription, User, Transaction

subscription_bp = Blueprint('subscription', __name__)
balance_lock = Lock()

def subscription_deduction_loop():
    """Continuously check active subscriptions and deduct amounts as necessary."""
    with app.app_context():
        session = Session() 
        while True:
            time.sleep(1)
            with balance_lock:
                active_subscriptions = session.query(Subscription).filter_by(active=True).all()
                current_time = datetime.now(timezone.utc)

                for subscription in active_subscriptions:
                    user = session.query(User).with_for_update().get(subscription.user_id)
                    last_deducted = subscription.last_deducted.replace(tzinfo=timezone.utc)
                    if current_time >= last_deducted + timedelta(seconds=subscription.interval_seconds):
                        if user and user.balance >= subscription.amount:
                            user.balance -= subscription.amount
                            new_transaction = Transaction(
                                amount=subscription.amount,
                                transaction_type="SUBSCRIPTION",
                                source_account_number=user.account_number,
                            )
                            session.add(new_transaction)
                            
                            # Update last_deducted to current time
                            subscription.last_deducted = current_time
                        else:
                            # Deactivate the subscription if funds are insufficient
                            subscription.active = False
                    # Commit all changes after processing each subscription
                session.commit()
# Start the global subscription thread only once
subscription_thread = threading.Thread(target=subscription_deduction_loop, daemon=True)
subscription_thread.start()

@subscription_bp.route('/user-actions/subscribe', methods=['POST'])
@jwt_required()
def create_subscription():
    """Handle subscription creation."""
    data = request.get_json()
    if not data or not all(key in data for key in ['pin', 'intervalSeconds', 'amount']):
        return Response("All fields are required.", status=400, mimetype='text/plain')    
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    pin = data.get('pin')
    
    try:
        amount = float(data.get('amount'))
        interval_seconds = int(data.get('intervalSeconds'))
        if amount <= 0 or interval_seconds <= 0:
            return Response("Amount must be a positive integer.", status=400, mimetype='text/plain')
    except (ValueError, TypeError):
            return Response("Invalid amount. Please enter a positive integer.", status=400, mimetype='text/plain')
    if not user.check_pin(pin):
        return Response("Invalid PIN.", status=403, mimetype='text/plain')
    # Create a new subscription
    new_subscription = Subscription(
        user_id=user.id,
        amount=amount,
        interval_seconds=interval_seconds,
        last_deducted=datetime.now(timezone.utc)  # Initialize last_deducted to now, making it aware

    )
    
    db.session.add(new_subscription)
    db.session.commit()
    return Response("Subscription created successfully.", status=200, mimetype='text/plain')