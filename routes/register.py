# routes/user_routes.py

from flask import Blueprint, request, jsonify, Response
from models import User
from app import db, bcrypt
import re

user_bp = Blueprint('user', __name__)

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def is_valid_phone_number(phone_number):
    phone_regex = r'^\d+$'
    return re.match(phone_regex, phone_number) is not None



@user_bp.route('/users/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(key in data for key in ['name', 'password', 'email', 'address', 'phoneNumber']):
        return jsonify("All fields are required."), 400
    name = data['name'].strip()
    password = data['password']
    email = data['email'].strip()
    address = data['address'].strip()
    phone_number = data['phoneNumber'].strip()

    if not name or not password or not email or not address or not phone_number:
        return jsonify("No empty fields allowed"), 400
    
    if not is_valid_email(email):
        return Response(f'Invalid email: {email}', status=400, mimetype='text/plain')
    if not is_valid_phone_number(phone_number):
        return Response(f'Phone number must contain only numbers.', status=400, mimetype='text/plain')

    if User.query.filter_by(email=email).first():
        return Response("Email already exists", status=400, mimetype='text/plain')
    if User.query.filter_by(phone_number=phone_number).first():
        return Response("Phone number already exists", status=400, mimetype='text/plain')

    validation_error = User.validate_password(password)
    if validation_error:
        return Response(validation_error, status=400, mimetype='text/plain')

    # Create new user
    new_user = User(
        name=name,
        email=email,
        phone_number=phone_number,
        address=address,
        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
    )

    # Add user to the database
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        "name": new_user.name,
        "email": new_user.email,
        "phoneNumber": new_user.phone_number,
        "address": new_user.address,
        "accountNumber": new_user.account_number,
        "hashedPassword": new_user.hashed_password
    }), 200
