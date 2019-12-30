import jwt
from appdata import data, valid_tokens, channels, decodeToken, getMessage, getUser, getMessageChannel
from server.error import ValueError, AccessError
from server.message_remove import message_remove


def message_edit(token, message_id, new_message):
    global channels

    try:
        u_id = decodeToken(token)
        message = getMessage(message_id)
        channel = getMessageChannel(message_id)
        if message["u_id"] == u_id: #check if user is the sender
            doEdit(message, new_message, token)
            return {}        
        for members in channel["owner_members"]: #user is owner of channel
            if members["u_id"] == u_id:
                doEdit(message, new_message, token)
                return {}
        users = getUser(u_id) #user is admin
        if users["permission_id"] == 1 or users["permission_id"] == 2:
            doEdit(message, new_message, token)
            return {}
        raise AccessError("User does not have permission to edit message!")

    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

  
def doEdit(message, new_message, token):
    if new_message != "":
        message["message"] = new_message
    else:
        message_remove(token, message["message_id"]) # NEW: delete the message
