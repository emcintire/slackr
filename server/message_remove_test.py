from .message_remove import message_remove
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_join import channel_join
from .channel_messages import channel_messages
from .message_send import message_send
from .error import AccessError, ValueError
from appdata import reset
import pytest

def test_message_remove_1(): #legal removal
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, myChannelID) #join that channel
    messageID = message_send(myToken, myChannelID, "test") #send test message
    message_remove(myToken, messageID) #0 is the most recent message which is the one we just sent
    myMessages = channel_messages(myToken, myChannelID, 0)["messages"] #get list of messages sent
    assert len(myMessages) == 0 #check that no messages remain
    
def test_message_remove_2(): #ValueError after deleting deleted message
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, str(myChannelID)) #join that channel
    messageID = message_send(myToken, myChannelID, "test") #send test message
    message_remove(myToken, messageID) #0 is the most recent message which is the one we just sent
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised 
        message_remove(myToken, messageID) #try to delete that message AGAIN to throw error
    
def test_message_remove_3(): #removal of someone else's message for AccessError as normal MEMBER
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myToken2 = auth_register("valid2@email.com", "securepassword2", "user", "two")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, str(myChannelID)) #join that channel
    channel_join(myToken2, str(myChannelID)) #both join the channel
    messageID = message_send(myToken, myChannelID, "test") #owner sends test message
    with pytest.raises(AccessError, match=r".*"): #check AccessError raised 
        message_remove(myToken2, messageID) #try to delete OWNER's message as normal MEMBER
    
def test_message_remove_4(): #removal of someone else's message as admin
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myToken2 = auth_register("valid2@email.com", "securepassword2", "user", "two")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, str(myChannelID)) #join that channel
    channel_join(myToken2, str(myChannelID)) #both join the channel
    messageID = message_send(myToken2, myChannelID, "test") #MEMBER sends test message
    message_remove(myToken, messageID) #OWNER deletes MEMBER's message which is allowed
    myMessages = channel_messages(myToken, myChannelID, 0)["messages"] #get list of messages sent
    assert len(myMessages) == 0 #check that no messages remain
    
def test_message_remove_5(): #send 3 messages and delete 1
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, myChannelID) #join that channel
    message_send(myToken, myChannelID, "message 1") #send test message 1
    message_send(myToken, myChannelID, "message 2") #send test message 2
    messageID = message_send(myToken, myChannelID, "message 3") #send test message 3
    message_remove(myToken, messageID) #delete the first message
    myMessages = channel_messages(myToken, myChannelID, 0)["messages"] #get list of messages sent
    assert len(myMessages) == 2 #check that only the other 2 messages remain

def test_message_remove_6(): #removal of someone else's message as owner
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myToken2 = auth_register("valid2@email.com", "securepassword2", "user", "two")["token"] #generate token for valid user
    myChannelID = channels_create(myToken2, "test", True) #create test channel
    channel_join(myToken2, str(myChannelID)) #both join the channel
    messageID = message_send(myToken2, myChannelID, "test") #MEMBER sends test message
    message_remove(myToken, messageID) #OWNER deletes MEMBER's message which is allowed
    myMessages = channel_messages(myToken, myChannelID, 0)["messages"] #get list of messages sent
    assert len(myMessages) == 0 #check that no messages remain

def test_invalid_token():
    with pytest.raises(AccessError, match=r".*"): #check AccessError raised 
        message_remove("lmao", 0)
