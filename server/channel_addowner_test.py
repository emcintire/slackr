from .message_send import message_send
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_join import channel_join
from .channel_addowner import channel_addowner

from .channel_details import channel_details
from server.error import AccessError, ValueError
from appdata import reset
import pytest

def test_channel_addowner_test_1(): #valid case
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    user2 = auth_register("valid2@email.com", "securepassword2", "user", "two")#generate token for valid user 2
    uID2 = user2["u_id"]
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, str(myChannelID)) #join that channel
    assert channel_addowner(myToken, str(myChannelID), str(uID2)) == {} #try to add user2 as owner
    
def test_channel_addowner_test_2(): #valueError for wrong channelID
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    user2 = auth_register("valid2@email.com", "securepassword2", "user", "two")#generate token for valid user 2
    uID2 = user2["u_id"]
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, str(myChannelID)) #join that channel
    invalidChannelID = 69
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised 
        channel_addowner(myToken, str(invalidChannelID), str(uID2)) #try to add user2 as owner to an INVALID channel
        
def test_channel_addowner_test_3(): #valueError for adding an owner who is an owner already
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    user2 = auth_register("valid2@email.com", "securepassword2", "user", "two")#generate token for valid user 2
    uID2 = user2["u_id"]
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, str(myChannelID)) #join that channel
    channel_addowner(myToken, str(myChannelID), str(uID2)) #add user2 as owner
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised 
        channel_addowner(myToken, str(myChannelID), str(uID2)) #add user2 as owner AGAIN
        
def test_channel_addowner_test_4(): #AccessError for adding an owner who is an owner already
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    user2 = auth_register("valid2@email.com", "securepassword2", "user", "two")#generate token for valid user 2
    myToken2 = user2["token"] 
    user3 = auth_register("valid3@email.com", "securepassword3", "user", "three")#generate token for valid user 3
    myToken3 = user3["token"] 
    uID3 = user3["u_id"]
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, str(myChannelID)) #join that channel
    channel_join(myToken2, str(myChannelID)) #join user2
    channel_join(myToken3, str(myChannelID)) #join user3
    with pytest.raises(AccessError, match=r".*"): #check AccessError raised 
        channel_addowner(myToken2, str(myChannelID), str(uID3)) #user2 who is not OWNER attempts to add user3 as OWNER

def test_invalid_token(): #valueError for adding an owner who is an owner already
    reset()
    with pytest.raises(AccessError, match=r".*"): #check ValueError raised 
        channel_addowner("bleugh", "1", "1") #add user2 as owner AGAIN

def test_add_member(): #valid case
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    user2 = auth_register("valid2@email.com", "securepassword2", "user", "two")#generate token for valid user 2
    myToken2 = user2["token"] 
    uID2 = user2["u_id"]
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken2, str(myChannelID)) #join that channel
    assert channel_addowner(myToken, str(myChannelID), str(uID2)) == {}

def test_channel_not_owner(): #valid case
    reset()
    user1 = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    user2 = auth_register("valid2@email.com", "securepassword2", "user", "two")#generate token for valid user 2
    myToken2 = user2["token"] 
    myChannelID = channels_create(user1['token'], "test", True) #create test channel
    channel_join(user1['token'], str(myChannelID)) #join that channel
    with pytest.raises(AccessError, match=r".*"):
        channel_addowner(myToken2, str(myChannelID), str(user1['u_id']))
