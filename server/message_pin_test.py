from .auth_register import auth_register
from .channels_create import channels_create
from .channel_leave import channel_leave
from .channel_join import channel_join
from .message_send import message_send
from .message_remove import message_remove
from .message_pin import message_pin
from .error import AccessError, ValueError
from appdata import reset
import pytest

def test_successful_pin():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel therefore am admin
    messageID = message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    assert message_pin(token, messageID) == {} #Successful pin

def test_message_not_valid():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channels_create(token, "Channel_name", False) #Create a new channel therefore am admin
    invalidMessageID = -1
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        message_pin(token, invalidMessageID) #Fails to pin as message doesn't exist

def test_not_a_member():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel therefore am admin
    messageID = message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    channel_leave(token, channel_id)
    with pytest.raises(AccessError, match=r".*"): #Check Access Error Raised (Value Error is Placeholder)
        message_pin(token, messageID) #Fails to pin as not part of channel

def test_already_pinned():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel therefore am admin
    messageID = message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    message_pin(token, messageID) #Pin the message
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised 
        message_pin(token, messageID) #Fails to pin as message is already pinned

def test_not_admin():
    reset()
    token1 = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    token2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token1, "Channel_name", True) #Create a new channel therefore am admin
    messageID = message_send(token1, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    channel_join(token2, str(channel_id))
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised 
        message_pin(token2, messageID) #Fails to pin as user is not an admin

def test_invalid_token():
    reset()
    with pytest.raises(AccessError, match=r".*"): #Check Value Error Raised 
        message_pin("lmao", 0) #Fails to pin as user is not an admin

def test_mult_messages():
    reset()
    token1 = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token1, "Channel_name", True) #Create a new channel therefore am admin
    message_send(token1, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    messageID = message_send(token1, channel_id, "Message2") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    assert message_pin(token1, messageID) == {} #Successful pin
