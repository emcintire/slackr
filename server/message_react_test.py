from .message_react import message_react
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_join import channel_join
from .channel_messages import channel_messages
from .message_send import message_send
from .error import AccessError, ValueError
from appdata import reset
import pytest

def test_message_remove_1(): #legal react
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    messageID = message_send(myToken, myChannelID, "test") #send test message
    validReactID = 1 #ASSUMPTION
    assert message_react(myToken, messageID, validReactID) == {} #valid react to the most recent sent message
    
def test_message_remove_2(): #invalid message in valid channel
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    message_send(myToken, myChannelID, "test") #send test message
    validReactID = 1 #ASSUMPTION
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised
        message_react(myToken, 999, validReactID)  #valid react to a non existant message
    
def test_message_remove_3(): #reactid invalid
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    #channel_join(myToken, myChannelID) #join that channel
    messageID = message_send(myToken, myChannelID, "test") #send test message
    invalidReactID = 69 #ASSUMPTION
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised
        message_react(myToken, messageID, invalidReactID) #invalid react to a valid message
    
def test_message_remove_4(): #message already has react
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    #channel_join(myToken, myChannelID) #join that channel
    messageID = message_send(myToken, myChannelID, "test") #send test message
    validReactID = 1 #ASSUMPTION
    message_react(myToken, messageID, validReactID) #valid react to the most recent sent message
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised
        message_react(myToken, messageID, validReactID)  #reacting again to the same message which has active react ID
    
def test_message_remove_5(): #illegal react in an unjoined private channel
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myToken2 = auth_register("valid2@email.com", "securepassword2", "user", "two")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", False) #create PRIVATE test channel
    messageID = message_send(myToken, myChannelID, "test") #send test message
    validReactID = 1 #ASSUMPTION
    with pytest.raises(AccessError, match=r".*"): #check ValueError raised ASSUMED
        message_react(myToken2, messageID, validReactID) #invalid reaction for wrong user


def test_invalid_token():
    with pytest.raises(AccessError, match=r".*"): #check ValueError raised ASSUMED
        message_react("lmao", 0, 1) #invalid reaction for wrong user
