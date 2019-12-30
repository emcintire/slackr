import pytest
from .auth_passwordreset_request import auth_passwordreset_request
from .auth_register import auth_register
from appdata import reset
from server.error import AccessError, ValueError


def test_valid_email():
    reset()
    auth_register("validemail@gmail.com", "validpassword", "validname", "validname")
    assert auth_passwordreset_request("validemail@gmail.com") == {} #attempt to reset, cant’t check return value

def test_multiple_email():
    reset()
    auth_register("validemail@gmail.com", "validpassword", "validname", "validname")
    auth_register("validemail1@gmail.com", "validpassword", "validname", "validname")
    assert auth_passwordreset_request("validemail1@gmail.com") == {} #attempt to reset, cant’t check return value

def test_invalid_email():
    reset()
    auth_register("invalidemail@gmail.com", "validpassword", "validname", "validname")
    with pytest.raises(ValueError, match=r".*"): #assumes this will raise exception NOT IN SPEC
        auth_passwordreset_request("invalidemail")

def test_not_registered():
    reset()
    with pytest.raises(ValueError, match=r".*"): #assumes this will raise exception NOT IN SPEC
        auth_passwordreset_request("validemail@email.com")

def test_bad_email():
    reset()
    with pytest.raises(ValueError, match=r".*"): #non-existant email
        auth_passwordreset_request("bademail")

def test_bad_email2():
    reset()
    with pytest.raises(ValueError, match=r".*"): #input is None
        auth_passwordreset_request(None)
