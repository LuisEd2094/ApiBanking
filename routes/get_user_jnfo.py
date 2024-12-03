from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User

get_user_info_bp = Blueprint('get_user_info', __name__)


@get_user_info_bp.route('/dashboard/user', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()

    if user:
        return jsonify({
            "name": user.name,
            "email": user.email,
            "phoneNumber": user.phone_number,
            "address": user.address,
            "accountNumber": user.account_number,
            "hashedPassword": user.hashed_password
        }), 200
    else:
        return jsonify({"message": "User not found."}), 404