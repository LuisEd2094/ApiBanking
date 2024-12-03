from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User

get_account_info_bp = Blueprint('get_account_info', __name__)


@get_account_info_bp.route('/dashboard/account', methods=['GET'])
@jwt_required()
def get_account_info():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if user:
        return jsonify({
        "accountNumber": user.account_number,
        "balance": round(user.balance, 2)
        }), 200
    else:
        return jsonify({"message": "User not found."}), 404