import jwt
from appdata import data, decodeToken
from server.error import ValueError, AccessError

def user_profile(token, u_id):
    global data
    try:
        decodeToken(token)
        # return info on the target user
        for user in data:
            if user['u_id'] == int(u_id):
                return {            
                    'email':user['email'],
                    'name_first':user['name_first'],
                    'name_last':user['name_last'],
                    'handle_str':user['handle'],
                    'profile_img_url':user['profile_img_url']
                }
        raise ValueError("Not a valid user")
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e
        