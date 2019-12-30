from .message_send import message_send
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_join import channel_join
from .channel_details import channel_details
from .channel_leave import channel_leave
from server.error import ValueError, AccessError 
from appdata import reset
import pytest

def test_channel_join_test_1(): #valid case for owner
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    myToken = user["token"]
    uID = user["u_id"]
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_leave(myToken, str(myChannelID))
    channel_join(myToken, str(myChannelID)) #join that channel
    assert channel_details(myToken, str(myChannelID))["name"] == "test" #check details
    assert channel_details(myToken, str(myChannelID))["owner_members"] == [{"u_id": uID,"name_first": "user","name_last": "name","profile_img_url":None}] #check details
    assert channel_details(myToken, str(myChannelID))["all_members"] == [{"u_id": uID,"name_first": "user","name_last": "name","profile_img_url":None}] #check details
    
def test_channel_join_test_2(): #valueError for wrong channelID
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myToken2 = auth_register("valid2@email.com", "securepassword", "user", "two")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, str(myChannelID)) #join that channel
    invalidChannelID = 69
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised 
        channel_join(myToken2, str(invalidChannelID)) #try to join an invalid channel as user2
        
def test_channel_join_test_3(): #AccessError for private channel
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    user2 = auth_register("valid2@email.com", "securepassword2", "user", "two")#generate token for valid user 2
    myToken2 = user2["token"] 
    myChannelID = channels_create(myToken, "test", False) #create PRIVATE test channel
    channel_join(myToken, str(myChannelID)) #join that channel
    with pytest.raises(AccessError, match=r".*"): #check ValueError raised 
        channel_join(myToken2, str(myChannelID)) #try to join user's private channel as a normal user

def test_pepelaugh():
    with pytest.raises(AccessError, match=r".*"):
        channel_join("pepeWide", "0")
