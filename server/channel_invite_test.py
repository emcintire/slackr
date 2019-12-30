import pytest
from .channel_invite import channel_invite
from .channels_create import channels_create
from .auth_register import auth_register
from server.error import ValueError, AccessError 
from appdata import reset

def test_success(): 
    reset()
    user1 = auth_register("validemail3@gmail.com", "validpassword1", "validname", "validname")
    user2 = auth_register("validemail4@gmail.com", "validpassword1", "validname", "validname")
    channelId = channels_create(user1['token'], "test", True)  	
    channel_invite(user1['token'], str(channelId), str(user2['u_id']))

def test_multiple_channels(): 
    reset()
    user1 = auth_register("validemail3@gmail.com", "validpassword1", "validname", "validname")
    user2 = auth_register("validemail4@gmail.com", "validpassword1", "validname", "validname")
    channels_create(user1['token'], "test", True)  	
    channelId = channels_create(user1['token'], "test2", True)  	
    channel_invite(user1['token'], str(channelId), str(user2['u_id']))
 
def test_invalid_token(): #invite user with invalid token
    reset()
    user1 = auth_register("validemail3@gmail.com", "validpassword1", "validname", "validname")
    uId = user1['u_id']
    token1 = user1['token']
    invalidToken = "lol"  #arbtrariy invalid token for testing
    channelId = channels_create(token1, "test", True)  	
    with pytest.raises(AccessError, match=r".*"):
        channel_invite(invalidToken, str(channelId), str(uId))
      
 
def test_invalid_token2(): #invite user with NONE token
    reset()
    user1 = auth_register("validemail3@gmail.com", "validpassword1", "validname", "validname")
    uId = user1['u_id']
    token1 = user1['token']
    channelId = channels_create(token1, "test", True)      
    with pytest.raises(AccessError, match=r".*"):
        channel_invite(None,str(channelId),str(uId))
 
 
def test_invalid_u_id(): #invite user with invalid userID
    reset()
    user1 = auth_register("validemail3@gmail.com", "validpassword1", "validname", "validname")
    token1 = user1['token']
    channelId = channels_create(token1, "test", True)     
    invalidUID = 69
    with pytest.raises(ValueError, match=r".*"):
        channel_invite(token1,str(channelId),str(invalidUID))
           
def test_invalid_channel_id(): #invite user to invalid channel
    reset()
    user1 = auth_register("validemail3@gmail.com", "validpassword1", "validname", "validname")
    user2 = auth_register("validemail4@gmail.com", "validpassword1", "validname", "validname")
    token1 = user1['token']
    invalidChannelID = 69   
    with pytest.raises(ValueError, match=r".*"):
        channel_invite(token1,str(invalidChannelID),str(user2['u_id']))
 
def test_not_member():
    reset()
    user1 = auth_register("validemail3@gmail.com", "validpassword1", "validname", "validname")
    user2 = auth_register("validemail4@gmail.com", "validpassword1", "validname", "validname")
    user3 = auth_register("validemail5@gmail.com", "validpassword1", "validname", "validname")
    channelId = channels_create(user2['token'], "test", True)     
    with pytest.raises(AccessError, match=r".*"):
        channel_invite(user1['token'],str(channelId),str(user3['u_id']))

 
def test_add_yourself(): #valid case
    reset()
    user1 = auth_register("validemail3@gmail.com", "validpassword1", "validname", "validname")
    uId = user1['u_id']
    token1 = user1['token']
    channelId = channels_create(token1, "test", True)
    with pytest.raises(ValueError, match=r".*"):
        channel_invite(token1,channelId,uId) #assuming this works   
