from .auth_register import auth_register
from .standup_start import standup_start
from .channels_create import channels_create
from .standup_active import standup_active
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
    assert standup_active(token, channel_id)['is_active']

def test_invalid_channel():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel
    standup_start(token, str(channel_id), 900) #Successful standup start
    with pytest.raises(ValueError, match=r".*"):
        standup_active(token, 69)

def test_standup_inactive():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    channel_id = channels_create(token, "Channel_name", False) #Create a new channel
    assert not standup_active(token, channel_id)['is_active']

def test_multiple_channels():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    channels_create(token, "Channel_name1", False) #Create a new channel that user1 is part of and private
    channel_id = channels_create(token, "Channel_name2", False) #Create a new channel that user1 is part of and private
    standup_start(token, str(channel_id), 900) #Successful standup start
    assert standup_active(token, channel_id)['is_active']

def test_invalid_token():
    reset()
    with pytest.raises(AccessError, match=r".*"):
        standup_active("GEESE HOWARD", "0")
