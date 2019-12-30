from .message_send import message_send
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_join import channel_join
from .channel_messages import channel_messages
from appdata import reset
from server.error import AccessError, ValueError
from .message_react import message_react
import pytest

def test_channel_messages_1(): #no messages
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    myToken = user["token"]
    myChannelID = str(channels_create(myToken, "test", True)) #create test channel
    myMessages = channel_messages(myToken, myChannelID, 0)
    assert myMessages["messages"] == [] #blank
    assert myMessages["start"] == 0
    assert myMessages["end"] == -1
    
def test_channel_messages_2(): #1 message
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    myToken = user["token"]
    myChannelID = str(channels_create(myToken, "test", True)) #create test channel
    message_send(myToken, myChannelID, "hello world")
    myMessages = channel_messages(myToken, myChannelID, 0)
    assert myMessages["messages"] != [] #check not blank but unable to match specific details
    assert myMessages["start"] == 0
    assert myMessages["end"] == -1
    
def test_channel_messages_3(): #1 message
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    myToken = user["token"]
    myChannelID = str(channels_create(myToken, "test", True))#create test channel
    channel_join(myToken, myChannelID) #join that channel
    for i in range(200): #send 200 MESSAGES #UnUsEd VaRiAbLe I
        message_send(myToken, myChannelID, "hello world")
    myMessages = channel_messages(myToken, myChannelID, 0)
    assert myMessages["messages"] != [] #check not blank but unable to match specific details
    assert myMessages["start"] == 0
    assert myMessages["end"] == 50 #check that more messages are available
    
def test_channel_messages_4(): #ValueError invalid channel
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    myToken = user["token"]
    myChannelID = str(channels_create(myToken, "test", True)) #create test channel
    channel_join(myToken, myChannelID) #join that channel
    message_send(myToken, myChannelID, "hello world")
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised 
        channel_messages(myToken, "420", 0) #check messages for invalid channel
        
def test_channel_messages_5(): #ValueError for start greater than messages
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    myToken = user["token"]
    myChannelID = str(channels_create(myToken, "test", True)) #create test channel
    channel_join(myToken, myChannelID) #join that channel
    message_send(myToken, myChannelID, "hello world")
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised 
        channel_messages(myToken, myChannelID, 69) #check with start greater than 1
        
def test_channel_messages_6(): #AccessError when not in the channel
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    myToken = user["token"]
    myToken2 = auth_register("valid2@email.com", "securepassword2", "user", "two")["token"]
    myChannelID = str(channels_create(myToken, "test", True)) #create test channel
    channel_join(myToken, myChannelID) #join that channel
    message_send(myToken, myChannelID, "hello world")
    with pytest.raises(AccessError, match=r".*"): #check AccessError raised 
        channel_messages(myToken2, myChannelID, 0) #check messages from user 2 who isn't in the channel
        
def test_invalid_token():
    with pytest.raises(AccessError, match=r".*"):
        channel_messages("pepelaugh", "0", "hello")

def test_message_react():
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name")
    user2 = auth_register("valid1@email.com", "securepassword", "user", "name")
    token = user['token']
    myChannelID = str(channels_create(token, "test", True))
    messageID = message_send(token, myChannelID, "hello world")
    channel_join(user2['token'], myChannelID)
    message_react(token, messageID, 1)
    message_react(user2['token'], messageID, 1)
    channel_messages(token, myChannelID, 0)
