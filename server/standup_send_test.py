from .auth_register import auth_register
from .standup_start import standup_start
from .channels_create import channels_create
from .channel_join import channel_join
from .standup_send import standup_send
from .error import AccessError, ValueError
from appdata import reset
import pytest
import time

def test_successful_standup_send():
    reset()
    token1 = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    token2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    channel_id = channels_create(token1, "Channel_name", True) #Create a new channel
    channel_join(token2, channel_id)
    standup_start(token1, channel_id, 900)
    assert standup_send(token2, channel_id, "message") == {} #Successful standup message send

def test_not_in_channel():
    reset()
    token1 = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    token2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    channel_id = channels_create(token1, "Channel_name", False) #Create a new channel
    standup_start(token1, channel_id, 900)
    with pytest.raises(AccessError, match=r".*"): #Check Access Error Raised
        standup_send(token2, channel_id, "message") #Unsuccessful standup message send as token2 not part of channel

def test_message_too_long():
    reset()
    token1 = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    token2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    channel_id = channels_create(token1, "Channel_name", True) #Create a new channel
    channel_join(token2, channel_id)
    standup_start(token1, channel_id, 900)
    i = 0
    message = ''
    while i < 2000:
        message += '1'
        i+=1
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        standup_send(token2, channel_id, message) #Unsuccessful standup message send as message too long

def test_channel_doesnt_exist():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    channel_id = channels_create(token, "Channel_name", True) #Create a new channel
    standup_start(token, channel_id, 900) #Would technically break here
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        standup_send(token, -1, "message") #Unsuccessful standup message send as channel_id invalid

def test_standup_not_active():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    channel_id = channels_create(token, "Channel_name", True) #Create a new channel
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        standup_send(token, channel_id, "message") #Unsuccessful standup message send as standup not active

def test_invalid_token():
    reset()
    with pytest.raises(AccessError, match=r".*"): #Check Value Error Raised
        standup_send('hello', 0, "message") #Unsuccessful standup message send as standup not active   
