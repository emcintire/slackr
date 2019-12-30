from .message_send import message_send
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_join import channel_join
from .channel_details import channel_details
from .channel_leave import channel_leave
from .channels_list import channels_list
from server.error import AccessError, ValueError
from appdata import reset
import pytest

def test_channels_list_test_1(): #no channels
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    myToken = user['token']
    assert channels_list(myToken) == {"channels":[]} #empty list expected cause no channels
    
def test_channels_list_test_2(): #one channel
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    myToken = user["token"]
    myChannelID = channels_create(myToken, "test", True)#create test channel
    assert channels_list(myToken) == {"channels":[{"channel_id":myChannelID, "name":"test"}]} #one channel
    
def test_channels_list_test_3(): #two channels
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    myToken = user["token"]
    myChannelID = channels_create(myToken, "test", True) #create test channel
    myChannelID2 = channels_create(myToken, "private", False) #create PRIVATE test channel
    assert channels_list(myToken) == {"channels":[{"channel_id":myChannelID, "name":"test"}, {"channel_id":myChannelID2, "name":"private"}]} #list both channels assuming that private channels show up
    
def test_channels_list_test_4(): #invalid token
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    myToken = user["token"]
    channels_create(myToken, "test", True) #create test channel
    invalidToken = ""
    with pytest.raises(AccessError, match=r".*"):
        channels_list(invalidToken)#ASSUMED INVALID TOKEN returns none

def test_multiple_users():
    reset()
    user1 = auth_register("valid@email.com", "securepassword", "user", "name")
    user2 = auth_register("valid1@email.com", "securepassword", "user", "name")
    myChannelID = str(channels_create(user1['token'], "hello", True))
    channel_join(user2['token'], myChannelID)
    channels_list(user1['token'])