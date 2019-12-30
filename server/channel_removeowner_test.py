from .message_send import message_send
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_join import channel_join
from .channel_addowner import channel_addowner
from .channel_removeowner import channel_removeowner
from server.error import AccessError, ValueError
from appdata import reset
import pytest

def test_channel_removeowner_test_1(): #valid case
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    user2 = auth_register("valid2@email.com", "securepassword2", "user", "two")#generate token for valid user 2
    uID2 = user2["u_id"]
    myChannelID = str(channels_create(myToken, "test", True)) #create test channel
    channel_join(myToken, myChannelID) #join that channel
    channel_addowner(myToken, myChannelID, str(uID2)) #add user2 as owner
    assert channel_removeowner(myToken, myChannelID, str(uID2)) == {} #remove him again
    
def test_channel_removeowner_test_2(): #valueError for wrong channelID
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    user2 = auth_register("valid2@email.com", "securepassword2", "user", "two")#generate token for valid user 2
    uID2 = user2["u_id"]
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, myChannelID) #join that channel
    invalidChannelID = 69
    channel_addowner(myToken, myChannelID, uID2) #add user2 as owner
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised 
        channel_removeowner(myToken, str(invalidChannelID), str(uID2)) #try to remove user2 as owner to an INVALID channel
        
def test_channel_removeowner_test_3(): #valueError for removing an owner who is not actually an owner
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    user2 = auth_register("valid2@email.com", "securepassword2", "user", "two")#generate token for valid user 2
    uID2 = str(user2["u_id"])
    myChannelID = str(channels_create(myToken, "test", True)) #create test channel
    channel_join(myToken, myChannelID) #join that channel
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised 
        channel_removeowner(myToken, myChannelID, uID2) #remove user3 as owner when hes not an owner
        
def test_channel_removeowner_test_4(): #AccessError for adding an owner who is an owner already
    reset()
    user1 = auth_register("valid@email.com", "securepassword", "user", "name") #generate user
    myToken = user1["token"]
    uID = user1["u_id"]
    user2 = auth_register("valid2@email.com", "securepassword2", "user", "two")#generate token for valid user 2
    myToken2 = user2["token"] 
    myChannelID = str(channels_create(myToken, "test", True)) #create test channel
    channel_join(myToken, myChannelID) #join that channel
    channel_join(myToken2, myChannelID) #join user2
    with pytest.raises(AccessError, match=r".*"): #check AccessError raised 
        channel_removeowner(myToken2, myChannelID, str(uID)) #user2 who is not OWNER attempts to remove user who is an owner

def test_invalid_token():
    reset()
    with pytest.raises(AccessError, match=r".*"): #check AccessError raised 
        channel_removeowner("Garen Yuumi is cancer", "0", "0")
