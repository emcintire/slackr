import jwt
from appdata import data, valid_tokens, channels, decodeToken, getUser, getChannel
from server.error import ValueError, AccessError

def channel_details(token, channel_id):
    try:
        # Get user details
        u_id = decodeToken(token)
        user = getUser(u_id)
        permissions = user['permission_id']

        # Get channel details
        channel = getChannel(channel_id)
        if channel['is_public'] == 'true' or permissions < 3:
            return {"name":channel['name'], "owner_members":channel['owner_members'], "all_members":channel['all_members']}
        raise AccessError("User is not member of channel")

    except ValueError as e:
        raise e
    except AccessError as e:
        raise e
   
