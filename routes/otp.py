from flask import Blueprint, request, jsonify, Response
from flask_mail import Message
from app import mail, db
from models import OTP, PasswordResetToken, User, bcrypt
import uuid
from datetime import datetime, timedelta, timezone
import secrets

otp_bp = Blueprint('otp', __name__)

def generate_numeric_otp(length=6):
    # Generate a random numeric OTP of a given length
    otp = ''.join([str(secrets.randbelow(10)) for _ in range(length)])    
    return otp

@otp_bp.route('/auth/password-reset/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    if not data or not all(key in data for key in ['identifier']):
        return jsonify({"message": "All fields are required."}), 400
    identifier = data.get('identifier')
    otp = generate_numeric_otp()
    otp_record = OTP(identifier=identifier, otp=otp, expires_at=datetime.now(timezone.utc) + timedelta(minutes=5))
    db.session.add(otp_record)
    db.session.commit()
    msg = Message("Your OTP Code", recipients=[identifier])
    msg.body = f"OTP:{otp}"
    mail.send(msg)

    return jsonify({"message": f"OTP sent successfully to: {identifier}"}), 200


@otp_bp.route('/auth/password-reset/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()

    if not data or 'identifier' not in data or 'otp' not in data:
        return jsonify({"message": "Identifier and OTP are required."}), 400

    identifier = data['identifier']
    otp = data['otp']

    otp_record = OTP.query.filter_by(identifier=identifier, otp=otp).first()

    if not otp_record:
        return jsonify({"message": "Invalid OTP."}), 400
    
    if otp_record.is_expired():
        return jsonify({"message": "OTP has expired."}), 400
    password_reset_token = str(uuid.uuid4())
    reset_token_record = PasswordResetToken(identifier=identifier, reset_token=password_reset_token, expires_at=datetime.now(timezone.utc) + timedelta(minutes=5))
    db.session.add(reset_token_record)
    db.session.delete(otp_record)
    db.session.commit()

    return jsonify({"passwordResetToken": password_reset_token}), 200


def validate_reset_token(identifier, reset_token):
    token_record = PasswordResetToken.query.filter_by(identifier=identifier, reset_token=reset_token).first()
    if token_record and not token_record.is_expired():
        return True
    return False

@otp_bp.route('/auth/password-reset', methods=['POST'])
def reset_password():
    data = request.get_json()
    if not data or not all(key in data for key in ['identifier', 'resetToken', 'newPassword']):
        return jsonify({"message": "Identifier, reset token, and new password are required."}), 400
    identifier = data['identifier']
    reset_token = data['resetToken']
    new_password = data['newPassword']

    if not validate_reset_token(identifier, reset_token):
        return jsonify({"message": "Invalid or expired reset token."}), 400

    user = User.query.filter((User.email == identifier) | (User.account_number == identifier)).first()
    if not user:
        return jsonify({"message": "User not found for the given identifier."}), 404
    validation_error = User.validate_password(new_password)
    if validation_error:
        return Response(validation_error, status=400, mimetype='text/plain')
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.hashed_password = hashed_password
    db.session.commit()

    return jsonify({"message": "Password reset successfully"}), 200