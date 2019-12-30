import jwt
from appdata import data, valid_tokens, channels, decodeToken, getMessage, getMessageChannel, isUserChan
from server.error import ValueError, AccessError

def message_pin(token, message_id):
    global data
    global channels

    try:
        u_id = decodeToken(token)
        message = getMessage(message_id)
        channel = getMessageChannel(message_id)
        isUserChan(u_id, channel) #Raise error if fails
        for members in data: 
            if members["u_id"] == u_id:
                if int(members["permission_id"]) == 1 or int(members["permission_id"]) == 2: #check user is admin ############ ADMIN OR OWNER?
                    if not message["is_pinned"]: #check if pinned
                        message["is_pinned"] = True
                        return {}
                    raise ValueError("Message is already pinned!")
        raise ValueError("User does not have permission to pin!")                         

    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

