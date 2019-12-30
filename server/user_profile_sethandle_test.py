from .auth_register import auth_register
from .user_profile_sethandle import user_profile_sethandle
from .error import AccessError, ValueError
from appdata import reset, valid_tokens
from .user_profile import user_profile
import pytest
import jwt

def test_successful_handle_change():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    u_id = user['u_id'] #Get the user id and token
    token = user['token']
    user_profile_sethandle(token, "Handle") #Change handle
    assert user_profile(token, u_id)["handle_str"] == "Handle" #Successful handle change

def test_unsuccessful_handle_change():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    token = user['token']
    handle = "123456789012345678901234567890" #Handle is 30 characters > 20
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        user_profile_sethandle(token, handle) #Change handle fails as handle too long

def test_invalid_token():
    reset()
    with pytest.raises(AccessError, match=r".*"): #Check Value Error Raised
        user_profile_sethandle('ayylmao', 'abc123') #Change handle fails as handle too long

def test_handle_taken():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    user2 = auth_register("ema2l@email.com", "password", "First_Name", "Last_Name") #Create a new profile#
    user_profile_sethandle(user['token'], "Handle") #Change handle
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        user_profile_sethandle(user2['token'], "Handle") #Change handle

def test_user_invalid():
    reset()
    global valid_tokens
    token = jwt.encode({'u_id': '69'}, 'table_flip', algorithm='HS256').decode('utf-8')
    valid_tokens.append(token)
    with pytest.raises(ValueError, match=r".*"):
        user_profile_sethandle(token, "keepothump") 

def test_multiple_user():
    reset()
    auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    user2 = auth_register("ema2l@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    user_profile_sethandle(user2['token'], "Handle") #Change handle
    assert user_profile(user2['token'], user2['u_id'])["handle_str"] == "Handle" #Successful handle change
