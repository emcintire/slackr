import jwt
from appdata import data, decodeToken
from server.error import ValueError, AccessError

def users_all(token):
    global data
    try:
        decodeToken(token)
        result = []
        # accumulate users
        for user in data:
            result.append(
                {
                    'u_id':user['u_id'],            
                    'email':user['email'],
                    'name_first':user['name_first'],
                    'name_last':user['name_last'],
                    'handle_str':user['handle'],
                    'profile_img_url':user['profile_img_url']
                }
                )
        if result == []:
            raise ValueError("No Users")
        else:
            return {"users":result}
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e
    

