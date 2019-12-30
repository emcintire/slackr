from .auth_register import auth_register
from .user_profile_setemail import user_profile_setemail
from .user_profile import user_profile
from .error import AccessError, ValueError
from appdata import reset, valid_tokens
import pytest
import jwt

def test_successful_email_change():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    u_id = user['u_id'] #Get the user id and token
    token = user['token']
    user_profile_setemail(token, "ema1l@email.com") #Change handle
    assert user_profile(token, u_id)["email"] == "ema1l@email.com" #Successful email change

def test_invalid_email():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    token = user['token']
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        user_profile_setemail(token, "email.com") #Change email fails as email is invalid

def test_invalid_email2():
    reset()
    user = auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    auth_register("ema1l@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    token = user['token']
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        user_profile_setemail(token, "ema1l@email.com") #Change email fails as email is already in use

def test_multiple_user():
    reset()
    auth_register("email@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    user2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name") #Create a new profile
    u_id = user2['u_id'] #Get the user id and token
    token = user2['token']
    user_profile_setemail(token, "emael@email.com") #Change handle
    assert user_profile(token, u_id)["email"] == "emael@email.com" #Successful email change

def test_invalid_token():
    reset()
    with pytest.raises(AccessError, match=r".*"):
        user_profile_setemail("Fnatic is garbage", "email@email.com")

def test_user_invalid():
    reset()
    global valid_tokens
    token = jwt.encode({'u_id': '69'}, 'table_flip', algorithm='HS256').decode('utf-8')
    valid_tokens.append(token)
    with pytest.raises(ValueError, match=r".*"):
        user_profile_setemail(token, "email@email.com") 
    

