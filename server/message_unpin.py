import jwt
from appdata import data, valid_tokens, channels, decodeToken, getMessage, getMessageChannel, isUserChan
from server.error import ValueError, AccessError

def message_unpin(token, message_id):
    global data
    global valid_tokens
    global channels
    try:
        u_id = decodeToken(token)
        message = getMessage(message_id)
        channel = getMessageChannel(message_id)
        isUserChan(u_id, channel) #Will raise error if fails
        for members in data: 
            if members["u_id"] == u_id:
                if int(members["permission_id"]) == 1 or int(members["permission_id"]) == 2: #check user is admin ############ ADMIN OR OWNER?
                    if message["is_pinned"]: #check if pinned
                        message["is_pinned"] = False
                        return {}
                    raise ValueError("Message is not pinned!")
        raise ValueError("User does not have permission to unpin!")   
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e
