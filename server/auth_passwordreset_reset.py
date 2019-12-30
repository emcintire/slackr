import jwt
from server.error import ValueError, AccessError
from appdata import setPassword, resetRemove, reset_codes

def auth_passwordreset_reset(reset_code, new_password):

    try:
        # Check new password is satisfactory            
        if new_password is None:
            raise ValueError("New password is too short")
        
        if len(new_password) < 5:
            raise ValueError("New password is too short")

        # Check reset code is valid and reset
        for reset_dict in reset_codes:
            if reset_dict['reset_code'] == int(reset_code):
                u_id = reset_dict['u_id']
                setPassword(u_id, new_password)
                resetRemove(reset_dict)
                return {}
        raise ValueError("Invalid code")

    except ValueError as e:
        raise e
