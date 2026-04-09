from flask import Blueprint, request, jsonify
from models import db, User, Patient
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    existing_user = User.query.filter_by(username=data['username']).first()

    if existing_user:
        return {"message": "Username already taken"}, 400

    user = User(
        username=data['username'],
        password=data['password'],
        role='patient'
    )

    db.session.add(user)
    db.session.commit()

    patient = Patient(
        user_id=user.id,
        name=data.get('name', ''),
        contact=data.get('contact', '')
    )

    db.session.add(patient)
    db.session.commit()

    return {"message": "User registered successfully"}, 201


@auth_bp.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user.is_blacklisted:
        return {"message": "User is blacklisted"}, 403
    
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user.id),additional_claims={'role': user.role})

    return jsonify({
        'token': access_token,
        'role': user.role
    }), 200