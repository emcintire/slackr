from .auth_register import auth_register
from .channels_create import channels_create
from .channel_leave import channel_leave
from .channel_join import channel_join
from .message_send import message_send
from .message_react import message_react
from .message_remove import message_remove
from .message_unreact import message_unreact
from .error import AccessError, ValueError
from appdata import reset
import pytest

def test_unreact_works():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel
    messageID = message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    validReactID = 1 #Assumption
    message_react(token, messageID, validReactID) #React to the message
    assert message_unreact(token, messageID, validReactID) == {} #Check that the message is unreacted

def test_message_no_reacts():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel
    messageID = message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    validReactID = messageID #Assumption
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        message_unreact(token, 0, validReactID) #Should fail as message has no reacts

def test_message_doesnt_exist():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channels_create(token, "Channel_name", False) #Create a new channel
    validReactID = 1 #Assumption
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        message_unreact(token, -1, validReactID) #Should fail as message doesn't exist

def test_invalid_react_ID():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel
    messageID = message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    validReactID = 1 #Assumption
    invalidReactID = -1 #Assumption
    message_react(token, messageID, validReactID) #React to the message
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        message_unreact(token, messageID, invalidReactID) #Should fail as reactID invalid

def test_invalidChannel():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel
    messageID = message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    validReactID = 1 #Assumption
    message_react(token, messageID, validReactID) #React to the message
    channel_leave(token, str(channel_id)) #Leave Channel
    with pytest.raises(AccessError, match=r".*"): #Check Value Error Raised
        message_unreact(token, messageID, validReactID) #Should fail as no longer part of channel
    #Note: Leaving channel hides it

def test_invalidToken():
    reset()
    invalidToken = "-1"
    message_id = 0 #Assume Valid and Exists
    validReactID = 0 #Assume Message is already reacted
    with pytest.raises(AccessError, match=r".*"):
        message_unreact(invalidToken, message_id, validReactID)

def test_unreact_without_possession():
    reset()
    token1 = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    token2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name")['token'] #Create a second account
    channel_id = channels_create(token2, "Channel_name", True) #Create a channel with the second account
    messageID = message_send(token2, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    validReactID = 1 #Assumption
    message_react(token2, messageID, validReactID) #React to the message with the second account
    channel_join(token1, channel_id)
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        message_unreact(token1, messageID, validReactID) #Should fail as the reaction was not token1's

def test_message_removed():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel
    messageID = message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    validReactID = 1 #Assumption
    message_react(token, messageID, validReactID) #React to the message
    message_remove(token, messageID)
    with pytest.raises(ValueError, match = r".*"): #Check Value Error Raised
        message_unreact(token, messageID, validReactID) #Fails as message doesn't exist

def test_multiple_messages():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel
    message_send(token, channel_id, "Message")
    message_send(token, channel_id, "Message")
    messageID = message_send(token, channel_id, "Message")
    message_react(token, messageID, 1) #React to the message
    message_unreact(token, messageID, 1)


