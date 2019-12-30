import jwt
from appdata import channels, data, valid_tokens, decodeToken
from server.error import ValueError, AccessError

def user_profile_setname(token, name_first, name_last):
    global data
    global channels
    try:
        u_id = decodeToken(token)
        #check length of names
        if (len(name_first) < 1) or (len(name_first) > 50):  #inclusive? assumed not to be
            raise ValueError("First name must be between 3 and 20 characters")
        if (len(name_last) < 1) or (len(name_last) > 50):  #inclusive? assumed not to be
            raise ValueError("Last name must be between 3 and 20 characters")
        # set data
        if int(u_id) < 0 or int(u_id) > len(data):
            raise ValueError("Not a valid user")
        for user in data:
            if user['u_id'] == int(u_id):
                user['name_first'] = name_first
                user['name_last'] = name_last
        for channel in channels:
            for user in channel['all_members']:
                if user['u_id'] == u_id:
                    user['name_first'] = name_first
                    user['name_last'] = name_last
            for user in channel['owner_members']:
                if user['u_id'] == u_id:
                    user['name_first'] = name_first
                    user['name_last'] = name_last
        return {}
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e
