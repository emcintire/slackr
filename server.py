"""Flask server"""
import sys
import jwt
import threading
from flask_cors import CORS
from json import dumps
from flask import Flask, request, send_from_directory
from flask_mail import Mail, Message
from urllib.parse import urlparse
from datetime import datetime, timezone
from werkzeug.exceptions import HTTPException
from appdata import data, valid_tokens, reset_codes, channels, index, setHostName
from server.auth_register import auth_register
from server.auth_login import auth_login
from server.auth_logout import auth_logout
from server.auth_passwordreset_request import auth_passwordreset_request
from server.auth_passwordreset_reset import auth_passwordreset_reset
from server.admin_userpermission_change import admin_userpermission_change
from server.channels_create import channels_create
from server.channel_details import channel_details
from server.channels_list import channels_list
from server.channels_listall import channels_listall
from server.channel_messages import channel_messages
from server.channel_join import channel_join
from server.channel_leave import channel_leave
from server.channel_addowner import channel_addowner
from server.channel_removeowner import channel_removeowner
from server.channel_invite import channel_invite
from server.message_send import message_send
from server.message_remove import message_remove
from server.message_edit import message_edit
from server.message_pin import message_pin
from server.message_unpin import message_unpin
from server.standup_start import standup_start
from server.standup_send import standup_send, standup_finish
from server.standup_active import standup_active
from server.message_react import message_react
from server.message_unreact import message_unreact
from server.message_sendlater import message_sendlater
from server.users_all import users_all
from server.admin_userpermission_change import admin_userpermission_change
from server.search import search
from server.user_profile import user_profile
from server.user_profile_setname import user_profile_setname
from server.user_profile_sethandle import user_profile_sethandle
from server.user_profile_setemail import user_profile_setemail
from server.user_profiles_uploadphoto import user_profiles_uploadphoto
from server.auth_register import auth_register
from server.error import ValueError, AccessError

def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.description,
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__, static_url_path = '/static/')
CORS(APP)
APP.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'comp1531tableflip@gmail.com',
    MAIL_PASSWORD = "comp1531"
)
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# THIS IS FOR DEBUGGING:
#auth_register("bchenyoung@gmail.com", "abc123", "Bill", "Chenyoung")
#auth_register("kappa@gmail.com", "abc123", "abcd", "efgh")

@APP.route('/echo/get', methods=['GET'])
def echo1():
    """ HTTP Request Echo GET: Returns the input """
    return dumps({
        'echo' : request.args.get('echo'),
    })

@APP.route('/echo/post', methods=['POST'])
def echo2():
    """ HTTP Request Echo POST: Returns the input """
    return dumps({
        'echo' : request.form.get('echo'),
    })

@APP.route('/auth/login', methods=['POST'])
def authlogin():
    '''Given a registered users' email and password and
    generates a valid token for the user to remain authenticated'''

    email = request.form.get('email')
    password = request.form.get('password')
    try:
        return dumps(auth_login(email, password))
    except ValueError as e:
        raise e

@APP.route('/auth/logout', methods=['POST'])
def authlogout():
    """ Given an active token, invalidates the taken to log the user out. If a valid token is given, and the user is successfully logged out, it returns true, otherwise false. """
    token = request.form.get('token')
    return dumps(auth_logout(token))

@APP.route('/auth/register', methods=['POST']) #do this first
def authregister():
    """ Given a user's first and last name, email address, and password, create a new account for them and return a new token for authentication in their session. A handle is generated that is the concatentation of a lowercase-only first name and last name. If the handle is already taken, a number is added to the end of the handle to make it unique. """
    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')

    # Generate u_id and token...
    registration = auth_register(email, password, name_first, name_last)
    u_id = registration["u_id"]
    token = registration["token"]

    # Save the registered user...
    try:
        return dumps({
            'u_id' : u_id,
            'token' : token
        })
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/auth/passwordreset/request', methods=['POST'])
def authpasswordresetrequest():
    '''Given an email address, if the user is a registered user, send's
    them a an email containing a specific secret code, that when entered
    in auth_passwordreset_reset, shows that the user trying to reset the
    password is the one who got sent this email.'''

    global reset_codes
    try:
        mail = Mail(APP)
        email = request.form.get('email')
        auth_passwordreset_request(email)
        reset_num = reset_codes[len(reset_codes) - 1]['reset_code']
        msg = Message("You're Password Reset Code", sender = "comp1531tableflip@gmail.com", recipients=[email])
        msg.body = "You're password reset code is " + str(reset_num)
        mail.send(msg)
        return dumps({})
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def authpasswordresetrequestreset():
    '''Given a reset code for a user, set that
    user's new password to the password provided'''

    reset_code = request.form.get('reset_code')
    new_password = request.form.get('new_password')
    try:
        return dumps(auth_passwordreset_reset(reset_code, new_password))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/channels/create', methods = ['POST'])
def channelsCreate():
    '''Creates channel with a name that is public or private'''

    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')

    #Generating channel_id
    channel_id = channels_create(token, name, is_public)
    try:
        return dumps({
            'channel_id': channel_id,
        })
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/channel/details', methods = ['GET'])
def channelDetails():
    '''Given a Channel with ID channel_id that the authorised user
    is part of, provide basic details about the channel'''

    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    try:
        return dumps(channel_details(token, channel_id))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/channels/list', methods = ['GET'])
def channelsList():
    '''Provide a list of all channels (and their associated details)
    that the authorised user is part of'''
    token = request.args.get('token')

    try:
        return dumps(channels_list(token))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/channels/listall', methods = ['GET'])
def channelsListAll():
    '''Provide a list of all channels (and their associated details)'''

    token = request.args.get('token')

    try:
        return dumps(channels_listall(token))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/channel/messages', methods = ['GET'])
def channelMessages():
    '''Given a Channel with ID channel_id that the authorised user is part of,
    return up to 50 messages between index "start" and "start + 50". Message
    with index 0 is the most recent message in the channel. This function
    returns a new index "end" which is the value of "start + 50", or, if this
    function has returned the least recent messages in the channel, returns -1
    in "end" to indicate there are no more messages to load after this return.'''

    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')

    try:
        return dumps(channel_messages(token, channel_id, start))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/channel/join', methods = ['POST'])
def channelJoin():
    '''Given a channel_id of a channel that the authorised
    user can join, adds them to that channel'''

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')

    try:
        return dumps(channel_join(token, channel_id))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/channel/leave', methods = ['POST'])
def channelLeave():
    '''Given a channel ID, the user removed as a member of this channel'''

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    try:
        return dumps(channel_leave(token, channel_id))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e


@APP.route('/user/profile', methods = ['GET'])
def userProfile():
    '''For a valid user, returns information about
    their email, first name, last name, and handle'''

    token = request.args.get('token')
    u_id = request.args.get('u_id')
    try:
        return dumps(user_profile(token, u_id))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/channel/addowner', methods = ['POST'])
def channelAddOwner():
    '''Make user with user id u_id an owner of this channel'''

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    try:
        return dumps(channel_addowner(token, channel_id, u_id))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/channel/removeowner', methods = ['POST'])
def channelRemoveOwner():
    '''Make user with user id u_id an owner of this channel'''

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')

    try:
        return dumps(channel_removeowner(token, channel_id, u_id))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/channel/invite', methods = ['POST'])
def channelInvite():
    '''Invites a user (with user id u_id) to join a channel with
    ID channel_id. Once invited the user is added to the channel immediately'''

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')

    try:
        return dumps(channel_invite(token, channel_id, u_id))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/message/send', methods = ['POST'])
def messageSend():
    '''Send a message from authorised_user to the channel specified by channel_id'''

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')

    try:
        return dumps({'message_id': message_send(token, channel_id, message)})
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/message/remove', methods = ['DELETE'])
def messageRemove():
    '''Given a message_id for a message, this message is removed from the channel'''

    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))

    try:
        return dumps(message_remove(token, message_id))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/message/edit', methods = ['POST', 'PUT']) ######################## THIS IS PUT BUT FOR FRONTEND
def messageEdit():
    '''Given a message, update it's text with new text. If the new
    message is an empty string, the message is deleted.'''

    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    message = request.form.get('message')

    try:
        return dumps(message_edit(token, message_id, message))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/message/pin', methods = ['POST'])
def messagePin():
    '''Given a message within a channel, mark it as "pinned"
    to be given special display treatment by the frontend'''

    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))

    try:
        return dumps(message_pin(token, message_id))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/message/unpin', methods = ['POST'])
def messageUnpin():
    '''Given a message within a channel, remove it's mark as unpinned'''

    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))

    try:
        return dumps(message_unpin(token, message_id))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/message/react', methods = ['POST'])
def messageReact():
    '''Given a message within a channel the authorised user is part of,
    add a "react" to that particular message'''

    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))

    try:
        return dumps(message_react(token, message_id, react_id))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/message/unreact', methods = ['POST'])
def messageUnreact():
    '''Given a message within a channel the authorised user is
    part of, remove a "react" to that particular message'''

    token = request.form.get('token')
    message_id = int(request.form.get('message_id'))
    react_id = int(request.form.get('react_id'))

    try:
        return dumps(message_unreact(token, message_id, react_id))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/search',methods=['GET'])
def messageSearch():
    '''Given a query string, return a collection of messages
    in all of the channels that the user has joined that match the query'''

    token = request.args.get('token')
    query_str = request.args.get('query_str')

    try:
        return dumps(search(token, query_str))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/admin/userpermission/change', methods = ['POST'])
def adminUserPermissionChange():
    '''Given a User by their user ID, set their permissions
    to new permissions described by permission_id'''

    token = request.form.get('token')
    u_id = request.form.get('u_id')
    permission_id = request.form.get('permission_id')

    try:
        return dumps(admin_userpermission_change(token, u_id, permission_id))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/standup/start', methods = ['POST'])
def standupStart():
    global start_time
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    length = int(request.form.get('length'))
    
    u_id = jwt.decode(token.encode('utf-8'), 'table_flip', algorithms=['HS256'])['u_id']
    time_finish = datetime.now(timezone.utc).timestamp() + length

    try:
        standup_start(token, channel_id, length)
        t = threading.Timer(length, standup_finish, [int(channel_id), u_id])
        t.start()
        return dumps({'time_finish':time_finish})
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/standup/send', methods = ['POST'])
def standupSend():
    '''Sending a message to get buffered in the standup
    queue, assuming a standup is currently active'''
    global channels
    global data
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')

    u_id = jwt.decode(token.encode('utf-8'), 'table_flip', algorithms=['HS256'])['u_id']
    for user in data:
        if user['u_id'] == u_id:
            name_first = user['name_first']

    try:
        return dumps(standup_send(token, channel_id, message))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/standup/active', methods=['GET'])
def standupActive():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    try:
        return dumps(standup_active(token, channel_id))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/message/sendlater', methods = ['POST'])
def messageSendLater():
    '''Send a message from authorised_user to the channel specified
    by channel_id automatically at a specified time in the future'''

    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')
    time_sent = request.form.get('time_sent') #[:-5]

    try:
        return dumps(message_sendlater(token, channel_id, message, float(time_sent)))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/user/profile/setname', methods = ['PUT'])
def userSetName():
    '''Update the authorised user's first and last name'''

    token = request.form.get('token')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    try:
        return dumps(user_profile_setname(token, name_first, name_last))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/user/profile/setemail', methods = ['PUT'])
def userSetEmail():
    '''Update the authorised user's email address'''

    token = request.form.get('token')
    email = request.form.get('email')
    try:
        return dumps(user_profile_setemail(token, email))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/user/profile/sethandle', methods = ['PUT'])
def userSetHandle():
    '''Update the authorised user's handle (i.e. display name)'''

    token = request.form.get('token')
    handle_str = request.form.get('handle_str')
    try:
        return dumps(user_profile_sethandle(token, handle_str))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

@APP.route('/user/profiles/uploadphoto', methods = ['POST'])
def userProfilesUploadPhoto():
    token = request.form.get('token') 
    img_url = request.form.get('img_url')
    x_start = int(request.form.get('x_start'))
    y_start = int(request.form.get('y_start'))
    x_end = int(request.form.get('x_end'))
    y_end = int(request.form.get('y_end'))
    setHostName(urlparse(request.base_url).netloc)
   
    try:
        return dumps(user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e 

@APP.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('', path)

@APP.route('/users/all', methods = ['GET'])
def usersAll():
    token = request.args.get('token') 
    try:
        return dumps(users_all(token))
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e

if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
