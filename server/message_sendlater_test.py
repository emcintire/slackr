from .message_sendlater import message_sendlater
from .channels_create import channels_create
from .channel_join import channel_join
from .auth_register import auth_register
from appdata import reset
from server.error import AccessError, ValueError
from datetime import datetime
import pytest

def test_message_sendlater_1(): #valid example
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, myChannelID) #join that channel
    assert message_sendlater(myToken, myChannelID, "this is a scheduled message", datetime(4000, 1, 1, 1, 1).timestamp()) == 0 #schedule valid message for 1/1/4000 01:01AM
    #CAN'T PYTEST THAT THIS MESSAGE ACTUALLY SENDS

def test_multiple_channels(): #valid example
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    channels_create(myToken, "test", True) #create test channel
    myChannelID = channels_create(myToken, "test", True) #create test channel
    assert message_sendlater(myToken, myChannelID, "this is a scheduled message", datetime(4000, 1, 1, 1, 1).timestamp()) == 1 #schedule valid message for 1/1/4000 01:01AM
    #CAN'T PYTEST THAT THIS MESSAGE ACTUALLY SENDS

def test_message_empty(): #valid example
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, myChannelID) #join that channel
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised 
        message_sendlater(myToken, myChannelID, "", datetime(4000, 1, 1, 1, 1).timestamp())
    
def test_message_sendlater_2(): #invalid token
    reset()
    with pytest.raises(AccessError, match=r".*"): #check ValueError raised 
        message_sendlater('ayylmao', '1', "you got hacked", datetime(4000, 1, 1, 1, 1))
    
def test_message_sendlater_3(): #sending in someone else's private channel which you haven't joined
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myToken2 = auth_register("valid2@email.com", "securepassword", "user", "two")["token"] #generate token for valid user 2
    myChannelID = channels_create(myToken, "test", False) #create PRIVATE channel for user 1
    with pytest.raises(AccessError, match=r".*"): #check ValueError raised 
        message_sendlater(myToken2, myChannelID, "you got hacked again", datetime(4000, 1, 1, 1, 1))#no permission for user2 to do this ASSUMES no output!
    
def test_message_sendlater_4(): #valueerror channel ID does not exist
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    invalidChannelID = 420 #assumes this does not exist
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised 
        message_sendlater(myToken, invalidChannelID, "test", datetime(4000, 1, 1, 1, 1)) #raise exception with wrong channelID
        
def test_message_sendlater_5(): #valueerror more than 1000 chars
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, myChannelID) #join that channel
    illegalMessage = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut sit amet varius leo. In ornare dolor nunc. Donec facilisis vel diam sed faucibus. Praesent dictum dictum ligula quis porttitor. Maecenas sollicitudin felis in nibh mollis, quis convallis ante euismod. Morbi tristique est in tellus tristique feugiat. Phasellus eu tempor ante, vel lacinia eros. Donec iaculis lobortis nisi, nec convallis tortor dignissim blandit. Fusce velit libero, auctor quis eros ut, consequat mollis quam. Etiam placerat eros id pellentesque pharetra. Sed dictum eu tortor non vulputate. Quisque et mi varius, consequat turpis non, volutpat felis. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce commodo auctor ipsum vel finibus. Proin vulputate metus id ipsum finibus rutrum. Aliquam auctor interdum congue. Phasellus tempus purus non tincidunt tincidunt. Phasellus lacinia, magna vel ultrices tincidunt, enim odio maximus elit, ut tempus dui ante quis orci. Nunc sed tristique velit, sit amet accumsan nunc. Etiam dignissim eget risus quis rutrum. Nulla vitae bibendum nisl. Suspendisse faucibus justo lectus, non efficitur leo fringilla nec. Nullam posuere elementum leo, vitae congue eros pharetra in. Ut nec lacinia nunc. Fusce ornare tempus turpis, et bibendum justo pellentesque a. Proin vitae malesuada nibh, vitae mollis ligula. Ut placerat odio nec auctor aliquam. Aenean commodo pulvinar massa, nec cursus lacus scelerisque nec. Proin scelerisque porta nibh. Suspendisse ultrices mauris arcu, eu eleifend velit rutrum vitae. Vivamus varius tincidunt neque eget pretium. Interdum et malesuada fames ac ante ipsum primis in faucibus. Vivamus et turpis quis tortor hendrerit rutrum ut id dolor. Curabitur fringilla nibh eu suscipit rhoncus. Integer porta, tellus id blandit vehicula, arcu ex posuere eros, in sodales tellus massa sit amet dolor. Vestibulum id felis gravida, fringilla enim quis, sodales nisi. Fusce iaculis, risus ut molestie consectetur, neque nisi consectetur velit, id tincidunt libero orci vitae sapien. Maecenas sodales odio ut porta ultrices. Donec eget sapien libero. Nunc ut nulla lorem. Vestibulum pulvinar magna tellus, sed molestie ligula efficitur id. In vehicula ante at sem pharetra, eget suscipit sapien ullamcorper. Mauris vel quam magna. Aliquam fringilla efficitur metus, non hendrerit arcu sodales commodo. Interdum et malesuada fames ac ante ipsum primis in faucibus. Morbi eget orci arcu. Nulla ullamcorper urna non odio ultrices scelerisque id quis dolor. In maximus tellus eget ultricies tempor. Sed eget massa eu augue accumsan euismod sit amet nec enim. Morbi ac fermentum odio." #longer than 1k chars
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised 
        message_sendlater(myToken, myChannelID, illegalMessage, datetime(4000, 1, 1, 1, 1)) #raise exception for exceeding 1k char message limit
        
def test_message_sendlater_6(): #valueerror for time in past
    reset()
    myToken = auth_register("valid@email.com", "securepassword", "user", "name")["token"] #generate token for valid user
    myChannelID = channels_create(myToken, "test", True) #create test channel
    channel_join(myToken, myChannelID) #join that channel
    with pytest.raises(ValueError, match=r".*"): #check ValueError raised 
        message_sendlater(myToken, myChannelID, "this is legal", datetime(2000, 1, 1, 1, 1).timestamp()) #raise exception for message scheduled for 1/1/2000 01:01AM
        
