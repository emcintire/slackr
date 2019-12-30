import jwt
from appdata import data, valid_tokens, channels, decodeToken, getMessage, getMessageChannel, isUserChan
from server.error import ValueError, AccessError

def message_unreact(token, message_id, react_id):
    global channels
    try:
        u_id = decodeToken(token)
        #check if react_id is valid at the start
        if react_id != 1:
            raise ValueError("Invalid react ID!")

        channel = getMessageChannel(message_id)
        message = getMessage(message_id)
        isUserChan(u_id, channel) #Will raise error if fails
        for react in message["reacts"]: 
            for react_users in react["u_ids"]: #check that the user hasn't already reacted
                if react_users == u_id:
                    react["u_ids"].remove(u_id)
                    return {}
        raise ValueError("User already has no active react for this message!")

    except ValueError as e:
        raise e
    except AccessError as e:
        raise e
