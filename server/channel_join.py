import jwt
from appdata import data, valid_tokens, channels, decodeToken, getUser, getChannel
from server.error import ValueError, AccessError

def channel_join(token, channel_id):
    global channels
    try:
        # Get user information
        u_id = decodeToken(token)
        users = getUser(u_id)
        permission = users['permission_id']
        userDetails = {"u_id":u_id, "name_first": users['name_first'], "name_last":users['name_last'], "profile_img_url": users['profile_img_url']}
               
        # Channel operations
        channel = getChannel(channel_id)
        if not channel['is_public'] and permission == 3:      #Checks if channel is public
            raise AccessError("You do not have access to this channel")
        else:
            channel['all_members'].append(userDetails)
            if userDetails not in channel['owner_members'] and permission < 3:
                channel['owner_members'].append(userDetails)
            return {}

    except ValueError as e:
        raise e
    except AccessError as e:
        raise e
