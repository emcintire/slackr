from .auth_register import auth_register
from .user_profile_setname import user_profile_setname
from .user_profile import user_profile
from .channel_join import channel_join
from .channels_create import channels_create
from .error import AccessError, ValueError
from appdata import reset, valid_tokens
import jwt
import pytest

def test_successful_name_change():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    u_id = user['u_id'] #Get the user id and token
    token = user['token']
    user_profile_setname(token, "Name_First", "Name_Last") #Change name
    assert user_profile(token, u_id)["name_first"] == "Name_First" #Check name is the same
    assert user_profile(token, u_id)["name_last"] == "Name_Last"

def test_channels():
    reset()
    token1 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    user2 = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    u_id2 = user2['u_id'] #Get the user id and token
    token2 = user2['token']
    channels_create(token1, 'hello', True)
    channel_id = channels_create(token2, 'hello2', True)
    channel_join(token2, channel_id)
    user_profile_setname(token2, "Name_First", "Name_Last") #Change name
    assert user_profile(token2, u_id2)["name_first"] == "Name_First" #Check name is the same
    assert user_profile(token2, u_id2)["name_last"] == "Name_Last"

def test_first_name_too_long():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    token = user['token']
    name = "123456789012345678901234567890123456789012345678901234567890" #60 character long name
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        user_profile_setname(token, name, "Name_Last") #Unsuccessful name change as first name too long

def test_last_name_too_long():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    token = user['token']
    name = "123456789012345678901234567890123456789012345678901234567890" #60 character long name
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        user_profile_setname(token, "Name_First", name) #Unsuccessful name change as last name too long

def test_invalid_token():
    reset()
    with pytest.raises(AccessError, match=r".*"):
        user_profile_setname("kappa", "lmao", 'lmao2')

def test_user_invalid():
    reset()
    global valid_tokens
    token = jwt.encode({'u_id': '69'}, 'table_flip', algorithm='HS256').decode('utf-8')
    valid_tokens.append(token)
    with pytest.raises(ValueError, match=r".*"):
        user_profile_setname(token, "lmao", 'lmao2') 

def test_multiple_user():
    reset()
    auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    user2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    u_id = user2['u_id'] #Get the user id and token
    token = user2['token']
    user_profile_setname(token, "lmao", 'lmao2') #Change handle
    assert user_profile(token, u_id)["name_first"] == "lmao"
    assert user_profile(token, u_id)["name_last"] == "lmao2"
