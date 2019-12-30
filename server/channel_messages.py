import jwt
from appdata import data, channels, decodeToken, getChannel
from server.error import ValueError, AccessError

def channel_messages(token, channel_id, start):
    global channels
    try:
        u_id = decodeToken(token)
        # Channel operations
        channel = getChannel(channel_id)
        for users in channel['all_members']:
            if users['u_id'] == u_id or data[u_id]['permission_id'] < 3:
                if int(start) > len(channel['messages']):
                    raise ValueError("Start is greater than the number of messages")
                newMsg = channel['messages']  #inject is_user_reacts into messages to return
                for messages in newMsg:
                    for reacts in messages['reacts']:
                        reacts['is_this_user_reacted'] = False #default
                        for react_users in reacts['u_ids']:
                            if react_users == u_id:
                                reacts['is_this_user_reacted'] = True #if user has reacted
                if len(newMsg) <= int(start) + 50:
                    return {'messages':newMsg[len(channel['messages'])-int(start)::-1], 'start':start, 'end': -1}
                else:
                    return {'messages':newMsg[len(channel['messages']):len(channel['messages']) - 51:-1], 'start':start, 'end':int(start)+50}                
        raise AccessError("Must be a member of channel to see messages")
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

