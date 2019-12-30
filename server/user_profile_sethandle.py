import jwt
from appdata import data, valid_tokens, decodeToken
from server.error import ValueError, AccessError

def user_profile_sethandle(token, handle_str):
    global data
    try:
        u_id = decodeToken(token)
        #check if handle is already in use
        for user in data:
            if user['handle'] == handle_str:
                raise ValueError("Handle already in use")
        #check handle is valid
        if (len(handle_str) < 3) or (len(handle_str) > 20):  #inclusive? assumed to be inclusive
            raise ValueError("Handle must be between 3 and 20 characters")
        # make the change
        for user in data:
            if user['u_id'] == int(u_id):
                user['handle'] = handle_str
                return {}
        raise ValueError("Not a valid user")
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e
