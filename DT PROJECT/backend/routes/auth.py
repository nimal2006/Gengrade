from flask import Blueprint, request, jsonify
from models.user import create_user, authenticate_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    email = data['email'].strip().lower()
    password = data['password']
    name = data.get('name', '').strip()
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400
    
    success, message = create_user(email, password, name)
    if success:
        return jsonify({'message': message}), 201
    else:
        return jsonify({'error': message}), 409

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    email = data['email'].strip().lower()
    password = data['password']
    
    success, result = authenticate_user(email, password)
    if success:
        user_data = {
            'email': result['email'],
            'name': result['name'],
            'created_at': result['created_at'],
            'last_login': result['last_login']
        }
        return jsonify({'message': 'Login successful', 'user': user_data}), 200
    else:
        return jsonify({'error': result}), 401
