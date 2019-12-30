from appdata import reset, index
from .message_edit import message_edit
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_join import channel_join
from .channel_messages import channel_messages
from .message_send import message_send
from .message_remove import message_remove
from server.error import AccessError, ValueError
import pytest

def test_message_edit_1(): #legal edit
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    messageID = message_send(myToken, myChannelID, "test") #send test message
    message_edit(myToken, messageID, "new message") #edit the most recent message just sent
    myMessages = channel_messages(myToken, "0", "1")["messages"]
    lastMessage = myMessages[0]["message"] #get the edited message
    assert lastMessage == "new message" # check the message was edited successfully

def test_message_edit_delete(): #legal edit
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    messageID = message_send(myToken, myChannelID, "test") #send test message
    message_edit(myToken, messageID, "") #edit the most recent message just sent
    with pytest.raises(ValueError, match=r".*"):
        channel_messages(myToken, "0", "1")

def test_message_edit_2(): #editing a non-existant message? ASSUMED
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = str(channels_create(myToken, "test", True)) #create test channel
    messageID = message_send(myToken, myChannelID, "test") #send test message
    message_remove(myToken, messageID) #0 is the most recent message which is the one we just sent
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised ASSUMED OUT OF SPEC
        message_edit(myToken, messageID, "new message") #edit the deleted message
    
def test_message_edit_3(): #editing of someone else's message for AccessError as normal MEMBER
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myToken2 = auth_register("valid2@email.com", "securepassword2", "user", "two")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, str(myChannelID)) #join that channel
    channel_join(myToken2, str(myChannelID)) #both join the channel
    messageID = message_send(myToken, myChannelID, "test") #owner sends test message
    with pytest.raises(AccessError, match=r".*"): #check ValueError raised #SHOULDNT THIS BE ACCESSERROR?
        message_edit(myToken2, messageID, "i edited your message :P") #try to edit OWNER's message as normal MEMBER
    

def test_message_edit_4(): #editing of someone else's message as channel owner
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myToken2 = auth_register("valid2@email.com", "securepassword2", "user", "two")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken2, str(myChannelID)) #both join the channel
    messageID = message_send(myToken2, myChannelID, "test") #MEMBER sends test message
    message_edit(myToken, messageID, "new message") #OWNER edits the most recent message just sent
    myMessages = channel_messages(myToken, str(myChannelID), 0)["messages"]
    lastMessage = myMessages[0]["message"] #get the edited message
    assert lastMessage == "new message" # check the message was edited successfully

def test_message_edit_5(): #editing of someone else's message as OWNER
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myToken2 = auth_register("valid2@email.com", "securepassword2", "user", "two")["token"] #generate token for valid user
    myChannelID = channels_create(myToken2, "test", True) #create test channel
    messageID = message_send(myToken2, myChannelID, "test") #MEMBER sends test message
    message_edit(myToken, messageID, "new message") #OWNER edits the most recent message just sent
    myMessages = channel_messages(myToken, str(myChannelID), 0)["messages"]
    lastMessage = myMessages[0]["message"] #get the edited message
    assert lastMessage == "new message" # check the message was edited successfully
    
def test_message_edit_6(): #editing a random message
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    message_send(myToken, myChannelID, "message 1") #send test message 1
    messageID = message_send(myToken, myChannelID, "message 2") #send test message 2
    message_send(myToken, myChannelID, "message 3") #send test message 3
    message_edit(myToken, messageID , "edited") #edit the middle message
    myMessages = channel_messages(myToken, str(myChannelID), 0)["messages"] #get list of messages sent
    assert myMessages[1]["message"] == "edited" # check the message was edited successfully'

def test_invalid_token():
    reset()
    with pytest.raises(AccessError, match=r".*"): #check ValueError raised #SHOULDNT THIS BE ACCESSERROR?
        message_edit("lmao", 0, 0)
