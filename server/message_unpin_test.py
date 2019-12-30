from .auth_register import auth_register
from .channels_create import channels_create
from .channel_leave import channel_leave
from .channel_join import channel_join
from .message_send import message_send
from .message_remove import message_remove
from .message_pin import message_pin
from .message_unpin import message_unpin
from .error import AccessError, ValueError
from appdata import reset
import pytest

def test_successful_unpin():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel therefore am admin
    messageID = message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    message_pin(token, messageID) #Pin message
    assert message_unpin(token, messageID) == {} #Successful unpin

def test_invalid_message():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel therefore am admin
    messageID = message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    message_pin(token, messageID) #Pin message
    invalidMessageID = -1
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        message_unpin(token, invalidMessageID) #Unpin fails as messageID invalid

def test_not_pinned():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel therefore am admin
    messageID = message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        message_unpin(token, messageID) #Unpin fails as message already unpinned

def test_not_admin():
    reset()
    token1 = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    token2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token1, "Channel_name", True) #Create a new channel therefore am admin
    messageID = message_send(token1, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    channel_join(token2, channel_id) #User joins channel
    message_pin(token1, messageID) #Admin pins message
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised 
        message_unpin(token2, messageID) #Fails to pin as user is not an admin

def test_not_a_member():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token, "Channel_name", False)#Create a new channel therefore am admin
    messageID = message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    message_pin(token, messageID)
    channel_leave(token, channel_id)
    with pytest.raises(AccessError, match=r".*"): #Check Access Error Raised (Value Error is Placeholder)
        message_unpin(token, messageID) #Fails to pin as not part of channel

def test_invalid_token():
    with pytest.raises(AccessError, match=r".*"): #Check Access Error Raised (Value Error is Placeholder)
        message_unpin("ayy lmao", 1) #Fails to pin as not part of channel
