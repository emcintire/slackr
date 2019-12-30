from .message_send import message_send
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_join import channel_join
from .channel_details import channel_details
from .channel_leave import channel_leave
import pytest
from server.error import AccessError, ValueError
from appdata import reset

def test_channel_leave_test_1(): #valid case
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    myToken = user["token"]
    uID = user["u_id"]
    user2 = auth_register("valid2@email.com", "securepassword", "user", "two") #generate token for valid user 2
    myToken2 = user2["token"]
    myChannelID = str(channels_create(myToken, "test", True)) #create test channel
    channel_join(myToken2, myChannelID) #join as user2
    channel_leave(myToken2, myChannelID) #leave immediately as user2
    assert channel_details(myToken, myChannelID)["name"] == "test" #check that user2 has left
    assert channel_details(myToken, myChannelID)["owner_members"] == [{"u_id": uID,"name_first": "user","name_last": "name",  "profile_img_url":None}] #check that user2 has left
    assert channel_details(myToken, myChannelID)["all_members"] == [{"u_id": uID,"name_first": "user","name_last": "name",  "profile_img_url":None}] #check that user2 has left
    
def test_channel_leave_test_2(): #valueError for wrong channelID
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised 
        channel_leave(myToken, "69") #try to leave an invalid channel as user2

def test_channel_leave_test_3(): #leaving when not already joined ASSUMED: does nothing
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    myToken = user["token"]
    user2 = auth_register("valid2@email.com", "securepassword", "user", "two") #generate token for valid user 2
    myToken2 = str(user2["token"])
    myChannelID = str(channels_create(myToken, "test", True)) #create test channel
    with pytest.raises(AccessError, match=r".*"):
        channel_leave(myToken2, myChannelID) #leave the channel which you haven't joined ASSUMED

def test_invalid_token():
    reset()
    with pytest.raises(AccessError, match=r".*"):
        channel_leave("xQc OMEGALUL", "0")

def test_leave_second():
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    str(channels_create(user['token'], "test", True)) #create test channel
    myChannel2 = str(channels_create(user['token'], "test", True)) #create test channel
    channel_leave(user['token'], myChannel2)
