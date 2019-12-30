import pytest
from .auth_login import auth_login
from .auth_register import auth_register
from appdata import reset
from server.error import AccessError, ValueError
  
def test_bad_email(): #try to login with bademail
    reset()
    auth_register("validemail@gmail.com", "validpassword1", "validname", "validname")
    badEmail = "lolz"
    with pytest.raises(ValueError, match=r".*"):
        auth_login(badEmail,"validpassword1")
 
def test_bad_email2(): #try to test none email
    reset()
    auth_register("validemail@gmail.com", "validpassword1", "validname", "validname")
    with pytest.raises(ValueError, match=r".*"):
        auth_login(None,"validpassword1")

def test_invalid_password(): #test invalid email/pass combination
    reset()
    auth_register("validemail@gmail.com", "invalidpassword", "validname", "validname")
    auth_register("validemail1@gmail.com", "validpassword1", "validname", "validname")
    with pytest.raises(ValueError, match=r".*"):
        auth_login("validemail@gmail.com","validpassword1")

def test_not_registered():
    reset()
    with pytest.raises(ValueError, match=r".*"):
        auth_login("validemail@gmail.com","validpassword1")
      
def test_success(): #valid case which should work
    reset()
    user = auth_register("validemail@gmail.com", "validpassword1", "validname", "validname")
    u_id = user["u_id"]
    assert auth_login("validemail@gmail.com","validpassword1")["u_id"] == u_id #check that uID is the same for the new session
    #assert auth_login("validemail@gmail.com","validpassword1")["token"] != token #check that the token is unique and not the same for the new session

def test_multiple(): #valid case which should work
    reset()
    auth_register("validemail@gmail.com", "validpassword1", "validname", "validname")
    user2 = auth_register("validemail1@gmail.com", "validpassword1", "validname", "validname")
    assert auth_login("validemail1@gmail.com","validpassword1")["u_id"] == user2['u_id'] #check that uID is the same for the new session
 
