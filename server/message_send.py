import jwt
from appdata import data, valid_tokens, channels, index, decodeToken, getChannel, addMessage, isUserChan
from server.error import ValueError, AccessError
from datetime import datetime, timezone

# Send a message from authorised_user to the channel specified by channel_id
def message_send(token, channel_id, message):
    global data
    global valid_tokens
    global channels

    try:
        u_id = decodeToken(token)
        channel = getChannel(channel_id)
        isUserChan(u_id, channel) #Will raise error if fails
        if len(message) > 1000:
            raise ValueError("Message can not be greather than 1000 character limit")
        elif len(message) == 0: #this appears to be handled by front end...
            raise ValueError("Message can not be empty")
        else:
            return addMessage(channel, message, u_id)

    except ValueError as e:
        raise e
    except AccessError as e:
        raise e


