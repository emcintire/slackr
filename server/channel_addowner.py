import jwt
from appdata import data, valid_tokens, channels, decodeToken, getUser, getChannel
from server.error import ValueError, AccessError


def channel_addowner(token, channel_id, u_id):
    global channels

    try:
        # Get user information
        userID = decodeToken(token)
        users = getUser(int(u_id))
        target = {'u_id':int(u_id), 'name_first':users['name_first'], 'name_last':users['name_last'], "profile_img_url": users['profile_img_url']}
        grantusers = getUser(userID)
        granter = {'u_id':userID, 'name_first':grantusers['name_first'], 'name_last':grantusers['name_last'], "profile_img_url": grantusers['profile_img_url']}
        permissions = grantusers['permission_id']

        # Channel operations
        channel = getChannel(channel_id)
        if granter in channel['owner_members'] or permissions < 3:
            if target in channel['owner_members']:
                raise ValueError("User already an owner")
            elif target in channel['all_members']:
                channel['owner_members'].append(target)
                return {}
            else:
                channel['owner_members'].append(target)
                channel['all_members'].append(target)
                return {}
        raise AccessError("User is not an owner")

    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

