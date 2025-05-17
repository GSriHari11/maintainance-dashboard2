from database import add_user, get_user
from utils.security import hash_password, check_password

def signup_user(email, password):
    if not email.endswith("@hpcl.in"):
        return False, "Only @hpcl.in emails are allowed"
    hashed_pw = hash_password(password)
    success = add_user(email, hashed_pw)
    return (success, "Account created!" if success else "User already exists!")

def login_user(email, password):
    user = get_user(email)
    if user and check_password(password, user[1]):
        return True, "Login successful"
    return False, "Invalid email or password"
