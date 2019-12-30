import jwt
from appdata import data, valid_tokens, channels, decodeToken, getMessage, getMessageChannel, getUserPerm
from server.error import ValueError, AccessError

def message_remove(token, message_id):
    global channels

    try:
        u_id = decodeToken(token)

        message = getMessage(message_id)
        channel = getMessageChannel(message_id)  
        if message["u_id"] == u_id: #check if user is the sender
            channel["messages"].remove(message)
            return {}
        for members in channel["owner_members"]: #user is owner of channel
            if members["u_id"] == u_id:
                channel["messages"].remove(message)
                return {}    
        if getUserPerm(u_id) == 2 or getUserPerm(u_id) == 1:
            channel["messages"].remove(message)
            return {}
        raise AccessError("User does not have permission to remove message!")

    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

