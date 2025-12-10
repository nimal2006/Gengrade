import json
import os
import bcrypt
from datetime import datetime

USER_DATA_FILE = 'database/users.json'

def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_user(email, password, name=None):
    users = load_users()
    if email in users:
        return False, "User already exists"
    
    users[email] = {
        'email': email,
        'password': hash_password(password),
        'name': name or email.split('@')[0],
        'created_at': datetime.now().isoformat(),
        'last_login': None
    }
    save_users(users)
    return True, "User created successfully"

def authenticate_user(email, password):
    users = load_users()
    print(f"DEBUG: Loaded users keys: {list(users.keys())}")
    print(f"DEBUG: Looking for email: {email}")
    if email not in users:
        print(f"DEBUG: User {email} not found in users")
        return False, "User not found"

    user = users[email]
    print(f"DEBUG: Found user: {user['email']}")
    if check_password(password, user['password']):
        # Update last login
        user['last_login'] = datetime.now().isoformat()
        save_users(users)
        return True, user
    print(f"DEBUG: Password check failed for {email}")
    return False, "Invalid password"

def get_user(email):
    users = load_users()
    return users.get(email)
