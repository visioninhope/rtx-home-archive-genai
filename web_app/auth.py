import json
from functools import wraps
from flask import request, redirect, url_for
from flask import make_response

# Path to your JSON file
USERS_FILE = r'C:\Users\tarun\private_contents\users.json'

def read_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def write_users(data):
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def authenticate(username, password):
    users = read_users()['users']
    user = next((user for user in users if user['username'] == username and user['password'] == password), None)
    return user



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.cookies.get('user_id')
        if user_id is None or not get_user_by_id(user_id):
            # Redirect to login if the user is not authenticated
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def roles_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = request.cookies.get('user_id')
            user = get_user_by_id(user_id)
            if user and user['role'] in allowed_roles:
                return f(*args, **kwargs)
            # Handle unauthorized access
            return make_response("Unauthorized", 401)
        return decorated_function
    return decorator

def get_user_by_id(user_id):
    users = read_users()['users']
    return next((user for user in users if user['userId'] == user_id), None)
