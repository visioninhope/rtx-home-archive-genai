import bcrypt

def hash_password(password):
    # Hashing the password and returning a string
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode('utf-8')  # Convert byte string to UTF-8 string

def check_password(hashed_password, password):
    # Converting hashed_password back to byte string for comparison
    return bcrypt.checkpw(password.encode(), hashed_password.encode('utf-8'))