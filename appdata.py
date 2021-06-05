import jwt
import hashlib
import random
from datetime import datetime, timezone
# from server.error import ValueError, AccessError

'''Contains user data of form
user = {
        "u_id": u_id,
        "token" : token, #Technically tokens wont be stored in the user data
        "handle": handle,
        "email" : email,
        "password" : password,
        "name_first" : name_first,
        "name_last" : name_last
    }

'''
global data
data = []

'''A list of logged in tokens
Please add to every function:

if jwt.decode(token.encode('utf-8'), 'table_flip', algorithms=['HS256'])['u_id'] != u_id
    raise ValueError("Token is invalid")

if token not in valid_tokens:
    raise AccessError("Invalid token or user is not logged in")

'''
global valid_tokens
valid_tokens = []

'''A list of reset codes and their corresponding user_id in the form
reset_code = {
                'reset_code': reset_code,
                'u_id': u_id
            }
'''
global reset_codes
reset_codes = []

'''Stores a list of channels of the form:
channel = {
            'channel_id' = channel_id,
            'name' : name,
            'is_public' : is_public,
            'owner_members' : [owner_members],
            'all_members' : [all_members],
            'messages' : [],
            'standup_status': False
}
'''
global channels
channels = []

'''Store the global index of messages'''
global index
index = 0

# Resets the state of the server for testing


def reset():
    global index
    global channels
    global valid_tokens
    global data
    data.clear()
    channels.clear()
    valid_tokens.clear()
    reset_codes.clear()
    index = 0


''' Server Implemenations '''
global start_time
start_time = []

host_name = ''


def setHostName(hostName):
    global host_name
    host_name = hostName


def getHostName():
    global host_name
    return host_name


''' Authentication abstract functions'''
# decodes u_id from a valid token


def decodeToken(token):
    if token not in valid_tokens:
        raise AccessError("Invalid token or user is not logged in")
    return jwt.decode(token.encode('utf-8'), 'table_flip', algorithms=['HS256'])['u_id']
# add a reset token for a u_id


def addToken(u_id):
    token = jwt.encode({"u_id": u_id, "login_time": str(datetime.now(
    ))}, "table_flip", algorithm='HS256')  # .decode('utf-8')  # Generate a new token
    valid_tokens.append(token)
    return token
# remove a valid reset token given the token


def removeToken(token):
    if token in valid_tokens:
        valid_tokens.remove(token)
        return True
    else:
        return False


''' GET abstract functions '''
# get user from u_id


def getUser(u_id):
    for users in data:
        if users['u_id'] == u_id:
            return users
    raise ValueError("User ID does not exist")
# get user from email


def getUserByEmail(email):
    for user in data:
        if user['email'].lower() == email.lower():
            return user
    raise ValueError("User with email does not exist")
# get channel from channel_id


def getChannel(channel_id):
    for channel in channels:
        if channel['channel_id'] == int(channel_id):
            return channel
    raise ValueError("Channel is invalid or does not exist")
# get message from message_id


def getMessage(message_id):
    for channel in channels:
        for message in channel["messages"]:
            if message["message_id"] == message_id:
                return message
    raise ValueError("Message does not exist")
# get channel from message_id


def getMessageChannel(message_id):
    for channel in channels:
        for message in channel["messages"]:
            if message["message_id"] == message_id:
                return channel
    raise ValueError("Message does not exist")
# get user's permission ID from u_id


def getUserPerm(u_id):
    for user in data:
        if user['u_id'] == u_id:
            return user['permission_id']
    raise ValueError("Invalid user ID")


''' SET abstract functions '''
# set user permission by u_id


def setPermission(u_id, permission_id):
    target = getUser(int(u_id))
    target['permission_id'] = int(permission_id)
# set user password by u_id


def setPassword(u_id, new_password):
    data[u_id]['password'] = new_password


''' RESET abstract functions '''
# generate a new reset token


def resetReq(u_id):
    reset_num = random.randint(100000, 999999)
    reset_codes.append({"u_id": u_id, "reset_code": reset_num})
# removes a reset token


def resetRemove(reset_dict):
    reset_codes.remove(reset_dict)


''' CREATE abstract functions '''
# creates a new user


def createUser(email, password, name_first, name_last, handle):
    u_id = len(data)
    token = addToken(u_id)
    authRegisterDict = {'u_id': u_id, 'token': token}

    if u_id == 0:
        permissions = 1
    else:
        permissions = 3

    hashPass = hashlib.sha256(password.encode()).hexdigest()

    data.append({
        "u_id": u_id,
        "handle": handle,
        "email": email,
        "password": hashPass,
        "name_first": name_first,
        "name_last": name_last,
        "permission_id": permissions,
        "profile_img_url": None
    })

    return authRegisterDict
# creates a new channel


def newChannel(channel_id, name, is_public, owner_members, all_members):
    channels.append({
        'channel_id': channel_id,
        'name': name,
        'is_public': is_public,
        'owner_members': owner_members,
        'all_members': all_members,
        'messages': [],
        'standup_status': False,
        'standup_message': "",
        'time_finish': None
    })

    return channel_id
# adds a new message to a channel


def addMessage(channel, message, u_id):
    global index
    messageID = index
    index += 1
    timeStamp = datetime.now(timezone.utc).timestamp()  # generate timestamp
    newMessage = {"message_id": messageID, "u_id": u_id, "message": message,
                  "time_created": timeStamp, "reacts": [], "is_pinned": False}
    channel["messages"].append(newMessage)  # add the message
    return messageID


''' MISC abstract functions'''
# checks if a user is in a channel


def isUserChan(u_id, channel):
    for users in channel['all_members']:
        if users['u_id'] == u_id:
            return True
    raise AccessError("User is not a member of the channel!")
