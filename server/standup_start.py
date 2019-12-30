import jwt
from appdata import data, valid_tokens, channels, decodeToken, getUserPerm, getChannel
from server.error import ValueError, AccessError
from datetime import datetime, timezone

def standup_start(token, channel_id, length):
    try:
        u_id = decodeToken(token)
        permissions = getUserPerm(u_id)
        channel = getChannel(channel_id)
        for owner in channel['owner_members']:
            if owner['u_id'] == u_id or permissions < 3:
                if not channel['standup_status']:
                    time_finish = datetime.now(timezone.utc).timestamp() + length
                    channel['standup_status'] = True
                    channel['time_finish'] = time_finish
                    return {"time_finish":time_finish}
                raise ValueError("Standup already running!")
        raise AccessError("User is not an owner!")
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e
 
