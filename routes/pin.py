from flask import Blueprint, request, jsonify
from models import User, bcrypt
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity


pin_bp = Blueprint('pin', __name__)
""" /api/account/pin/create
/api/account/pin/update """

@pin_bp.route('/account/pin/create', methods=['POST'])
@jwt_required()
def create_pin():
    data = request.get_json()
    if not data or not all(key in data for key in ['pin', 'password']):
        return jsonify({"msg": "All fields are required."}), 400
    
    pin = data.get('pin')
    password = data.get('password')
    if not pin or not password:
        return jsonify({"msg": "PIN and password are required."}), 400
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify({"msg": "User not found."}), 404
    if not user.check_password(password):
        return jsonify({"msg": "Access denied"}), 401
    
    # Hash the PIN and save it
    user.pin = bcrypt.generate_password_hash(pin).decode('utf-8')
    db.session.commit()

    return jsonify({"msg": "PIN created successfully"}), 200


@pin_bp.route('/account/pin/update', methods=['POST'])
@jwt_required()
def update_pin():
    data = request.get_json()
    if not data or not all(key in data for key in ['newPin', 'password', 'oldPin']):
        return jsonify({"msg": "All fields are required."}), 400
    
    new_pin = data.get('newPin')
    password = data.get('password')
    old_pin = data.get('oldPin')
    if not new_pin or not password or not old_pin:
        return jsonify({"msg": "PIN and password are required."}), 400
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify({"msg": "User not found."}), 404

    if not user.check_password(password) or not user.check_pin(old_pin):
        return jsonify({"msg": "Access denied"}), 401
    
    # Hash the PIN and save it
    user.pin = bcrypt.generate_password_hash(new_pin).decode('utf-8')
    db.session.commit()

    return jsonify({"msg": "PIN updated successfully"}), 200