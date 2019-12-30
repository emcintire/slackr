import jwt
from appdata import data, valid_tokens, channels, decodeToken, getUser, getChannel
from server.error import ValueError, AccessError

def channel_invite(token, channel_id, u_id):
    try:
        # Get user information
        userID = decodeToken(token)
        grant_user = getUser(userID)
        granter = {'u_id':userID, 'name_first':grant_user['name_first'], 'name_last':grant_user['name_last'], "profile_img_url": grant_user['profile_img_url']}
        target_user = getUser(int(u_id))
        target = {'u_id':int(u_id), 'name_first':target_user['name_first'], 'name_last':target_user['name_last'], 'profile_img_url': target_user['profile_img_url']}

        # Can't invite yourself...
        if granter == target:
            raise ValueError("Can't invite yourself!")

        # Channel operations
        channel = getChannel(channel_id)
        if granter in channel['all_members']:
            channel['all_members'].append(target)
            return {}
        raise AccessError("User not a member of channel")
                    
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

 
