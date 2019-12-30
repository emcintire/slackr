import re
import smtplib
import random
from server.error import ValueError, AccessError
from appdata import data, valid_tokens, reset_codes, getUserByEmail, resetReq

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

def auth_passwordreset_request(email):
    try:
        # Check email is provided and is valid
        if email is None:
            raise ValueError("Invalid Email Format")    

        if not re.search(regex,email):
            raise ValueError("Invalid Email Format")    
        
        # Generate a reset code for the corresponding user
        u_id = getUserByEmail(email)['u_id']
        resetReq(u_id)
        return {}
        
    except ValueError as e:
        raise e
