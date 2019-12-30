from .auth_register import auth_register
from .channels_create import channels_create
from .message_send import message_send
from .search import search
from .channel_join import channel_join
import pytest
from .error import AccessError, ValueError
from appdata import reset

def test_successful_search():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create an account and generate token
    token = user['token']
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel therefore am admin
    message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    assert search(token, "Message")['messages'][0]['message'] == "Message"

def test_unsuccessful_search():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create an account and generate token
    token = user['token']
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel therefore am admin
    message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    assert search(token, "b")['messages'] == [] #Unsuccessful search

def test_prefix_search():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create an account and generate token
    token = user['token']
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel therefore am admin
    message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    assert search(token, "Me")['messages'][0]['message'] == "Message"

def test_middle_search():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create an account and generate token
    token = user['token']
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel therefore am admin
    message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    assert search(token, "ss")['messages'][0]['message'] == "Message"

def test_suffix_seach():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create an account and generate token
    token = user['token']
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel therefore am admin
    message_send(token, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    assert search(token, "ge")['messages'][0]['message'] == "Message"

def test_empty_search():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create an account and generate token
    token = user['token']
    channels_create(token, "Channel_name", False) #Create a new channel therefore am admin
    assert search(token, "ge")['messages'] == [] #Unsuccessful search as no messages

def test_search_messages_posted_others():
    reset()
    user1 = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create an account and generate token
    token1 = user1['token']
    token2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token1, "Channel_name", True) #Create a new channel therefore am admin
    channel_join(token2, channel_id)
    message_send(token1, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    assert search(token2, "Message")['messages'][0]['message'] == "Message"

def test_not_in_channel():
    reset()
    user1 = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create an account and generate token
    token1 = user1['token']
    token2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name")['token'] #Create an account and generate token
    channel_id = channels_create(token1, "Channel_name", False) #Create a new channel therefore am admin
    message_send(token1, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    assert search(token2, "Message")['messages'] == [] #Unsuccessful search

def test_invalid_token():
    with pytest.raises(AccessError, match="r.*"):
        search("hello", "Message")

def test_multiple_channels():
    reset()
    user1 = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create an account and generate token
    token1 = user1['token']
    channels_create(token1, "Channel_name", False) #Create a new channel therefore am admin
    channels_create(token1, "Channel_name2", False) #Create a new channel therefore am admin
    channels_create(token1, "Channel_name3", False) #Create a new channel therefore am admin
    channel_id = channels_create(token1, "Channel_name4", False) #Create a new channel therefore am admin
    message_send(token1, channel_id, "Message") #Send a message to that channel. The message will have message_id 0 as it is the most recent
    assert search(token1, "Message")['messages'][0]['message'] == "Message"
