from .message_send import message_send
from .auth_register import auth_register
from .channels_create import channels_create
from .channel_join import channel_join
from .channel_details import channel_details
from server.error import ValueError, AccessError
from appdata import reset
import pytest

def test_channel_details_test_1(): #valid case
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    myToken = user["token"]
    uID = user["u_id"]
    myChannelID = channels_create(myToken, "test", True) #create test channel
    #channel_join(myToken, str(myChannelID)) #join that channel
    print(channel_details(myToken, str(myChannelID))["all_members"])
    assert channel_details(myToken, str(myChannelID))["name"] == "test" #check details
    assert channel_details(myToken, str(myChannelID))["owner_members"] == [{'u_id': uID,'name_first': 'user','name_last': 'name', 'profile_img_url': None}] #check details
    assert channel_details(myToken, str(myChannelID))["all_members"] == [{"u_id": uID,"name_first": "user","name_last": "name", 'profile_img_url': None}] #check details
    
def test_channel_details_test_2(): #valueError for wrong channelID
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, str(myChannelID)) #join that channel
    invalidChannelID = 69
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised 
        channel_details(myToken, str(invalidChannelID)) #get details for an invalid channel
        
def test_channel_details_test_3(): #AccessError for not being in the channel
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    user2 = auth_register("valid2@email.com", "securepassword2", "user", "two")#generate token for valid user 2
    myToken2 = user2["token"] 
    myChannelID = channels_create(myToken, "test", True) #create test channel
    #channel_join(myToken, str(myChannelID)) #join that channel
    with pytest.raises(AccessError, match=r".*"): #check ValueError raised 
        channel_details(myToken2, str(myChannelID)) #user2 is not in the channel but requests for details prompting accesserror
        
def test_channel_details_test_4(): #test with 3 users
    reset()
    user = auth_register("valid@email.com", "securepassword", "user", "name") #generate token for valid user
    myToken = user["token"]
    uID = user["u_id"]
    user2 = auth_register("valid2@email.com", "securepassword2", "user", "two")#generate token for valid user 2
    myToken2 = user2["token"] 
    uID2 = user2["u_id"]
    user3 = auth_register("valid3@email.com", "securepassword3", "user", "three")#generate token for valid user 3
    myToken3 = user3["token"] 
    uID3 = user3["u_id"]
    myChannelID = channels_create(myToken, "test420", True) #create test channel
    #channel_join(myToken, str(myChannelID)) #join that channel
    channel_join(myToken2, str(myChannelID)) #join user2
    channel_join(myToken3, str(myChannelID)) #join user3
    details = channel_details(myToken, str(myChannelID))
    assert details["name"] == "test420"
    assert details["owner_members"] == [{"u_id": uID,"name_first": "user","name_last": "name", 'profile_img_url': None}]
    assert details["all_members"] == [{"u_id": uID,"name_first": "user","name_last": "name", 'profile_img_url': None}, {"u_id": uID2,"name_first": "user","name_last": "two", 'profile_img_url': None}, {"u_id": uID3,"name_first": "user","name_last": "three", 'profile_img_url': None}]

def test_this_is_incredibly_invalid():
    with pytest.raises(AccessError, match = r".*"):
        channel_details("big chungus", str(69420))
