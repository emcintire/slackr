import jwt
from appdata import data, valid_tokens, channels, decodeToken
from server.error import ValueError, AccessError

def channels_list(token):
    global channels
    try:
        u_id = decodeToken(token)
        channelList = {"channels":[]}

        for channel in channels:
            for user in channel['all_members']:
                if user['u_id'] == u_id:
                    channelList['channels'].append({"channel_id":channel['channel_id'], "name":channel['name']})

        return channelList
    except AccessError as e:
        raise e



