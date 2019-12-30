import jwt
from appdata import channels, decodeToken
from server.channels_list import channels_list
from server.error import ValueError, AccessError

def search(token, query_str):
    try:
        decodeToken(token)
        retMessages = []    
        channelList = channels_list(token)['channels']
        # Loop through all channels and messages for matches
        for inChannel in channelList:
            for channel in channels:
                if inChannel['channel_id'] == channel['channel_id']:
                    for message in channel['messages']:
                        if query_str in message['message']:
                            retMessages.append(message)                  
        return {"messages":retMessages}
    except AccessError as e:
        raise e


