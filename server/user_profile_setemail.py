import jwt
import re
from appdata import data, valid_tokens, decodeToken
from server.error import ValueError, AccessError

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

def user_profile_setemail(token, email):
    global data
    try:
        u_id = decodeToken(token)
        #check if email is already in use
        for user in data:
            if user['email'] == email:
                raise ValueError("Email already in use")
        #check email is valid
        if not re.search(regex,email):  
            raise ValueError("Invalid Email")
        # set email
        for user in data:
            if user['u_id'] == int(u_id):
                user['email'] = email
                return {}
        raise ValueError("Not a valid user") #technically impossible to reach

    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

