from .auth_register import auth_register
from .users_all import users_all
from .error import AccessError, ValueError
import pytest
from appdata import reset, valid_tokens
from datetime import datetime
import jwt

def test_successful():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    users = users_all(token)['users']
    assert users[0]['email'] == "email@email.com"
    assert users[0]['name_first'] == "First_Name"
    assert users[0]['name_last'] == "Last_Name"
    assert users[0]['handle_str'] == "first_namelast_name"


def test_invalid_token():
    reset()
    auth_register("email@email.com", "password", "First_Name", "Last_Name") #Register a new profile
    token = -1
    with pytest.raises(AccessError, match=r".*"): #Check Value Error Raised
        users_all(token) #Fails as user id and token is invalid


def test_no_profiles():
    reset()
    global valid_tokens
    token = jwt.encode({"u_id": 1, "login_time": str(datetime.now())}, "table_flip", algorithm='HS256').decode('utf-8')
    valid_tokens.append(token)
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        users_all(token) #Fails as user id and token is invalid

def test_multiple_profile():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    auth_register("ema1l@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    users = users_all(user['token'])['users']
    assert users[0]['email'] == "email@email.com"
    assert users[0]['name_first'] == "First_Name"
    assert users[0]['name_last'] == "Last_Name"
    assert users[0]['handle_str'] == "first_namelast_name"
    assert users[1]['email'] == "ema1l@email.com"
    assert users[1]['name_first'] == "First_Name"
    assert users[1]['name_last'] == "Last_Name"
    assert users[1]['handle_str'] == "first_namelast_name1"

