from .auth_register import auth_register
from .user_profile import user_profile
from .error import AccessError, ValueError
import pytest
from appdata import reset

def test_successful_profile():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    u_id = user['u_id'] #Get the user id and token
    token = user['token']
    assert user_profile(token, u_id)["email"] == "email@email.com" #Check emails are the same
    assert user_profile(token, u_id)["name_first"] == "First_Name" #Check names are the same
    assert user_profile(token, u_id)["name_last"] == "Last_Name"
    assert user_profile(token, u_id)["handle_str"] == "first_namelast_name" #Handle is undefined, can be empty or None

def test_invalid_token():
    reset()
    auth_register("email@email.com", "password", "First_Name", "Last_Name") #Register a new profile
    u_id = -1 #Assume -1 is invalid u_id and token
    token = -1
    with pytest.raises(AccessError, match=r".*"): #Check Value Error Raised
        user_profile(token, u_id) #Fails as user id and token is invalid

def test_invalid_profile():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Register a new profile
    u_id = -1 #Assume -1 is invalid u_id and token
    token = user['token']
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        user_profile(token, u_id) #Fails as user id and token is invalid

def test_multiple_profile():
    reset()
    auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    user2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    u_id = user2['u_id'] #Get the user id and token
    token = user2['token']
    assert user_profile(token, u_id)["email"] == "ema1l@email.com" #Check emails are the same
    assert user_profile(token, u_id)["name_first"] == "First_Name" #Check names are the same
    assert user_profile(token, u_id)["name_last"] == "Last_Name"
    assert user_profile(token, u_id)["handle_str"] == "first_namelast_name1" #Handle is undefined, can be empty or None
