from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt
from models import User, TokenBlacklist
from app import  db
from sqlalchemy import func

session_bp = Blueprint('login', __name__)


@session_bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(key in data for key in ['identifier', 'password']):
        return Response(f"Bad credentials", status=401, mimetype='text/plain')
        
    identifier = data.get('identifier')
    password = data.get('password')

    # Query the user by email or account number
    user = User.query.filter(
        (func.binary(User.email) == identifier) | 
        (func.binary(User.account_number) == identifier)
    ).first()
    if user is None:
        return Response(f"User not found for the given identifier: {identifier}", status=400, mimetype='text/plain')
    if not user.check_password(password):
        return Response(f"Bad credentials", status=401, mimetype='text/plain')
    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token}), 200

@session_bp.route('/users/logout', methods=['GET'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    blacklisted_token = TokenBlacklist(token=jti)
    db.session.add(blacklisted_token)
    db.session.commit()

    return jsonify({"message": "Successfully logged out."}), 200
