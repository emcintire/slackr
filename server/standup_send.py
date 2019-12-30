import jwt
from appdata import data, valid_tokens, channels, index, decodeToken, getChannel
from server.error import ValueError, AccessError
from datetime import datetime, timezone

def standup_send(token, channel_id, message):  
    try:
        u_id = decodeToken(token)
        # Check length is OK
        if len(message) > 1000:
            raise ValueError("Length is too long")
        # Get user permissions
        for user in data:
            if user['u_id'] == u_id:
                permissions = user['permission_id']
                name_first = user['name_first']
        # Prepare a new message
        newMessage = name_first + ': ' + message + ' '
        # Add the new message if allowed
        channel = getChannel(channel_id)
        for member in channel['all_members']:
            if member['u_id'] == u_id or permissions < 3:
                if channel['standup_status']:
                    channel['standup_message'] += newMessage
                    return {}
                raise ValueError("Standup not running!")
        raise AccessError("User is not an owner!")
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

def standup_finish(channel_id, u_id):
    # Send the message at the end
    global index
    timeStamp = datetime.now(timezone.utc).timestamp()
    channel = getChannel(channel_id)
    channel['messages'].append({"message_id":index, "u_id":u_id, "message": channel['standup_message'], "time_created": timeStamp, "reacts":[]})
    channel['standup_status'] = False
    channel['standup_message'] = ""
    channel['time_finish'] = None
    index += 1
