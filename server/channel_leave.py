import jwt
from appdata import channels, decodeToken, getChannel
from server.error import ValueError, AccessError

def channel_leave(token, channel_id):
    try:
        u_id = decodeToken(token)
        # Channel operations
        channel = getChannel(channel_id)
        for user in channel['all_members']:
            if user['u_id'] == u_id:
                channel['all_members'].remove(user)
                if user in channel['owner_members']:
                    channel['owner_members'].remove(user)
                return {}
        raise AccessError('User is not a member')
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e
