import jwt
from appdata import data, valid_tokens, channels, decodeToken, getUser, getChannel
from server.error import ValueError, AccessError

def channel_removeowner(token, channel_id, u_id):
    try:
        # Get user information
        userID = decodeToken(token)
        users = getUser(int(u_id))
        target = {'u_id':int(u_id), 'name_first':users['name_first'], 'name_last':users['name_last'], "profile_img_url": users['profile_img_url']}
        users = getUser(userID)
        granter = {'u_id':userID, 'name_first':users['name_first'], 'name_last':users['name_last'], "profile_img_url": users['profile_img_url']}
        permissions = users['permission_id']

        # Channel operations
        channel = getChannel(channel_id)
        if granter in channel['owner_members'] or permissions < 3:
            if target not in channel['owner_members']:
                raise ValueError("User not an owner")
            else:
                channel['owner_members'].remove(target)
                return {}
        raise AccessError("User is not an owner")

    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

