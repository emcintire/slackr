from .auth_register import auth_register
from .admin_userpermission_change import admin_userpermission_change
from server.error import AccessError, ValueError
from appdata import reset
import pytest

def test_successful_permissions_change():
    reset()
    token1 = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile which is an admin
    u_id2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name")['u_id'] #Create a new profile which is an user
    assert admin_userpermission_change(token1, str(u_id2), "2") == {} #Set user2 to admin

def test_successful_demote():
    reset()
    token1 = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile which is an admin
    u_id2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name")['u_id'] #Create a new profile which is an user
    admin_userpermission_change(token1, str(u_id2), "2") #Set user2 to admin
    assert admin_userpermission_change(token1, str(u_id2), "3") == {} #Set user2 to dirt covered peasant scum

def test_not_admin():
    reset()
    u_id1 = auth_register("email@email.com", "password", "First_Name", "Last_Name")['u_id'] #Create a new profile which is an admin
    token2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile which is an user
    with pytest.raises(AccessError, match=r".*"): #Check Access Error Raised
        admin_userpermission_change(token2, str(u_id1), "3") #Unsuccessful demotion as user2 is not an admin

def test_invalid_userid():
    reset()
    token1 = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile which is an admin
    user_id = -1 #invalid userid
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        admin_userpermission_change(token1, str(user_id), "2") #Unsuccessful as user_id is invalid

def test_invalid_userid2():
    reset()
    token1 = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile which is an admin
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        admin_userpermission_change(token1, "420", "2") #Unsuccessful as user_id is invalid

def test_invalid_token():
    reset()
    with pytest.raises(AccessError, match=r".*"): #Check Value Error Raised
        admin_userpermission_change("bleugh", str(0), "2") #Unsuccessful as user_id is invalid

def test_permission_id_invalid():
    reset()
    token1 = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile which is an admin
    u_id2 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name")['u_id'] #Create a new profile which is an user
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        admin_userpermission_change(token1, str(u_id2), "420") #Permission_id invalid so unsuccessful
    
