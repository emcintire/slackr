import pytest
from .auth_passwordreset_reset import auth_passwordreset_reset
from .auth_passwordreset_request import auth_passwordreset_request
from .auth_register import auth_register
from appdata import reset, reset_codes
from server.error import AccessError, ValueError

#ASSUMES ARBITRARY CODES AS ACTUAL CODES CAN NOT BE OBTAINED VIA FUNCTION
invalidCode = "69"
validCode = "123456"
 
def test_invalid_code(): #reset with invalid code
    reset()
    auth_register("validemail@gmail.com", "validpassword", "validname", "validname")
    auth_passwordreset_request("validemail@gmail.com")
    with pytest.raises(ValueError, match=r".*"):
        auth_passwordreset_reset(invalidCode, '123456')
 
 
def test_invalid_password(): #too short password
    reset()
    auth_register("validemail@gmail.com", "validpassword1", "validname", "validname")
    auth_passwordreset_request("validemail@gmail.com")
    with pytest.raises(ValueError, match=r".*"):
        auth_passwordreset_reset(validCode, '1234')
      
def test_invalid_password2(): #reset with NONE password
    reset()
    auth_register("validemail@gmail.com", "validpassword", "validname", "validname")
    auth_passwordreset_request("validemail@gmail.com")
    with pytest.raises(ValueError, match=r".*"):
        auth_passwordreset_reset(validCode, None)
    
def test_success(): #valid case
    reset()
    global reset_codes
    user = auth_register("validemail@gmail.com", "validpassword", "validname", "validname")
    reset_codes.append({'u_id':user['u_id'], 'reset_code':123456})
    auth_passwordreset_request("validemail@gmail.com")
    assert auth_passwordreset_reset(validCode, '123456') == {}

 
