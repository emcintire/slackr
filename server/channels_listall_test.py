from .channels_listall import channels_listall
from .auth_register import auth_register
from .channels_create import channels_create
from server.error import AccessError, ValueError
from .channel_join import channel_join
import pytest
from appdata import reset

def test_channels_listall_1(): #test no channels
    reset()
    myToken1 = auth_register("valid1@email.com", "securepassword1", "user", "one")["token"] #generate token for valid user
    assert channels_listall(myToken1)["channels"] == [] #get list of all channels. non created
    
def test_channels_listall_2(): #test one channel created
    reset()
    myToken2 = auth_register("valid2@email.com", "securepassword2", "user", "two")["token"] #generate token for valid user
    myChannelID1 = channels_create(myToken2, "test", True) #create new channel
    assert channels_listall(myToken2)["channels"] == [{"channel_id":myChannelID1, "name":"test"}] #list created channel

def test_channels_listall_3(): #test one joined channel and one unjoined channel
    reset()
    myToken2 = auth_register("valid2@email.com", "securepassword2", "user", "two")["token"]
    myToken3 = auth_register("valid3@email.com", "securepassword3", "user", "three")["token"] #generate token for valid user
    myChannelID1 = channels_create(myToken3, "test", True) #create channel
    channel_join(myToken3, myChannelID1) #join that channel
    myChannelID2 = channels_create(myToken3, "hello world", True) #create another channel
    assert channels_listall(myToken2)["channels"] == [{"channel_id":myChannelID1, "name":"test"}, {"channel_id":myChannelID2, "name":"hello world"}] #list both channels  
    
def test_channels_listall_4(): #test one public channel annd one PRIVATE channel *ASSUMING private channels show up but can't be joined
    reset()
    myToken3 = auth_register("valid3@email.com", "securepassword4", "user", "four")["token"]
    myToken4 = auth_register("valid4@email.com", "securepassword4", "user", "four")["token"] #generate token for valid user
    myChannelID1 = channels_create(myToken4, "test", False) #create PRIVATE channel
    channel_join(myToken3, myChannelID1) #join the PRIVATE channel
    myChannelID2 = channels_create(myToken4, "hello world", True) #create another channel
    assert channels_listall(myToken3)["channels"] == [{"channel_id":myChannelID1, "name":"test"}, {"channel_id":myChannelID2, "name":"hello world"}] #list both channels
    
def test_channels_listall_5(): #test with invalid token
    reset()
    invalidToken = "omgHAX" #arbitrary
    with pytest.raises(AccessError, match=r".*"):
        channels_listall(invalidToken) #returns nothing ASSUMING N/A implies this
    
def test_channels_listall_6(): #test with two users
    reset()
    myToken5 = auth_register("valid5@email.com", "securepassword5", "user", "five")["token"] #generate token for valid user
    myToken6 = auth_register("valid6@email.com", "securepassword6", "user", "six")["token"] #generate token for valid user
    myChannelID1 = channels_create(myToken5, "test", True) #create channel with user5
    assert channels_listall(myToken6)["channels"] == [{"channel_id":myChannelID1, "name":"test"}] #check user6 can see user5 channel 
