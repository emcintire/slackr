import pytest
from .auth_register import auth_register
from .auth_login import auth_login
from .auth_logout import auth_logout
from appdata import reset
def test_valid_token(): #log out with valid token
    reset()
    user1 = auth_register("validemail@gmail.com", "validpassword1", "validname", "validname")
    token = user1['token']
    assert auth_logout(token)['is_success'] #this return assumes it succeeded
 
def test_invalid_token(): #log out with invalid token
    reset()
    auth_register("validemail@gmail.com", "validpassword1", "validname", "validname")
    invalidToken = "memes"
    assert not auth_logout(invalidToken)['is_success'] #this ASSUMES N/A assumption case will return None if not succeeded

