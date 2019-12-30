from .auth_register import auth_register
from .standup_start import standup_start
from .channels_create import channels_create
from .error import AccessError, ValueError
from appdata import reset
import pytest
import time
from datetime import datetime, timezone

def test_successful_standup():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel
    standup_start(token, str(channel_id), 900) #Successful standup start

def test_invalid_channel():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    channel_id = -1 #invalid channel id
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        standup_start(token, str(channel_id), 900) #Unsuccessful standup start as channel id is invalid

def test_not_member():
    reset()
    token1 = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    token2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    channel_id = channels_create(token1, "Channel_name", True) #Create a new channel that user1 is part of and private
    with pytest.raises(AccessError, match=r".*"): #Value Error is placeholder for Access Error
        standup_start(token2, str(channel_id), 900) #Unsuccessful standup start as user 2 is not part of the channel

def test_multiple_standups():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel that user1 is part of and private
    standup_start(token, str(channel_id), 900) #Successful standup start
    #time.sleep(300) #Wait 5 minutes COMMENTED OUT TEMPORARILY FOR DEBUG PURPOSES ONLY
    with pytest.raises(ValueError, match=r".*"): #Value Error is placeholder for Access Error
        standup_start(token, str(channel_id), 900) #Dependent on assumption

def test_multiple_channels():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    channels_create(token, "Channel_name1", False) #Create a new channel that user1 is part of and private
    channel_id = channels_create(token, "Channel_name2", False) #Create a new channel that user1 is part of and private
    standup_start(token, str(channel_id), 900) #Successful standup start

def test_invalid_token():
    reset()
    with pytest.raises(AccessError, match=r".*"):
        standup_start("GEESE HOWARD", "0", 900)
