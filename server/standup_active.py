import jwt
from appdata import data, valid_tokens, channels, start_time, decodeToken
from server.error import ValueError, AccessError
from datetime import datetime, timezone

def standup_active(token, channel_id):
    global start_time
    try:
        decodeToken(token)
        # Check standup status
        for channel in channels:
            if channel['channel_id'] == int(channel_id):
                if not channel['standup_status']:
                    return {'is_active':False, 'time_finish':None}
                else:
                    return {'is_active':True, 'time_finish':channel['time_finish']}
        raise ValueError("Channel ID is invalid!")
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e  
