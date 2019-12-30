import jwt
from appdata import channels, start_time, decodeToken, getUser, newChannel
from server.error import ValueError, AccessError

def channels_create(token, name, is_public):
    try:
        if len(name) > 20:
            raise ValueError("Name must be 20 characters or less.")

        # Get user information
        channel_id = len(channels)
        u_id = decodeToken(token)
        users = getUser(u_id)
        name_first = users['name_first']
        name_last = users['name_last']
        profile_img_url = users['profile_img_url']

        owner_members = [{"u_id":u_id, "name_first":name_first, "name_last":name_last, "profile_img_url":profile_img_url}]
        all_members = [{"u_id":u_id, "name_first":name_first, "name_last":name_last, "profile_img_url":profile_img_url}]

        newChannel(channel_id, name, is_public, owner_members, all_members)
        return channel_id

    except ValueError as e:
        raise e
    except AccessError as e:
        raise e
