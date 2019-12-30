import re
import hashlib
from server.error import ValueError
from appdata import getUserByEmail, addToken

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

def auth_login(email, password):

    try:
        # Check email is provided and is valid
        if email is None:
            raise ValueError("Invalid Email Format")

        if not re.search(regex,email):
            raise ValueError("Invalid Email Format")

        # Hash the password
        hashPass = hashlib.sha256(password.encode()).hexdigest()

        # Find the user by email
        user = getUserByEmail(email)
        if user['password'] == hashPass: # Match their password
            token = addToken(user['u_id'])
            return {'u_id':user['u_id'], 'token': token} # Return them their new token
        raise ValueError("Password incorrect")

    except ValueError as e:
        raise e





