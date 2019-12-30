import jwt
from appdata import data, valid_tokens, channels, decodeToken
from server.error import ValueError, AccessError

def channels_listall(token):
    global channels
    try:
        decodeToken(token)
        channelList = {"channels":[]}

        for channel in channels:
            channelList['channels'].append({"channel_id":channel['channel_id'], "name":channel['name']})

        return channelList

    except AccessError as e:
        raise e



