from .channels_create import channels_create
from .auth_register import auth_register
from server.error import AccessError, ValueError
from appdata import reset
import pytest

def test_channels_create_1(): #create one public channel
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    assert channels_create(myToken, "test", True) == 0 #check channel_id is generated ASSUMING starts from 0
    
def test_channels_create_2(): #create one private channel
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    assert channels_create(myToken, "name", False) == 0 #check channel_id is generated ASSUMING starts from 0 and incremented
    
def test_channels_create_3(): #create two channels
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    assert channels_create(myToken, "hello", True) == 0 #check channel_id is generated ASSUMING starts from 0
    assert channels_create(myToken, "world", False) == 1 #check channel_id is generated ASSUMING starts from 0
    
def test_channels_create_4(): #create channels with same name
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    channelID1 = channels_create(myToken, "same", True) #create channel
    channelID2 = channels_create(myToken, "same", True) #create same name channel
    assert channelID1 != channelID2 #check two unique channels created

def test_channels_create_5(): #create channel with invalid token
    reset()
    invalidToken = "omgHAX" #arbitrary
    with pytest.raises(AccessError, match=r".*"):
        channels_create(invalidToken, "hackerz", True) #channel is not created ASSUMING N/A means None returned    
    
def test_channels_create_6(): #value error test
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised for illegaly long channel name
        channels_create(myToken, "this is an awfully long name for a channel name that is defs over the legal 20 characters lol :)", True) 

