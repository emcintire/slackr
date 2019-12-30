import pytest 
from .auth_register import auth_register
from appdata import reset
from server.error import ValueError, AccessError

def test_valid(): #valid case
    reset()
    user = auth_register("testing@unsw.edu.au", "SecurePassword1234", "Mike", "Hunt")
    assert user["u_id"] == 0 #assumes this starts from 0. check user was generate

def test_bad_email(): #test invalid email
    reset()
    with pytest.raises(ValueError, match=r".*"):
        auth_register("invalidemail", "validpassword1", "validname", "validname")

def test_invalid_email(): #test registration with duplicate email
    reset()
    auth_register("validemail1@gmail.com", "validpassword1", "validname", "validname")
    with pytest.raises(ValueError, match=r".*"):
        auth_register("validemail1@gmail.com", "validpassword1", "validname", "validname")

def test_invalid_password(): #test with too short password
    reset()
    with pytest.raises(ValueError, match=r".*"):
        auth_register("validemail1@gmail.com", "1234", "validname", "validname")
  
def test_invalid_first_name(): #test name too long 100):
    reset()
    with pytest.raises(ValueError, match=r".*"):
        auth_register("validemail1@gmail.com", "validpassword1", "invalidname111111111111111111111111111111111111111111111", "validname")

def test_invalid_first_name2(): #tests 0 character first name
    reset()
    with pytest.raises(ValueError, match=r".*"):
        auth_register("validemail1@gmail.com", "validpassword1", "", "validname")

def test_invalid_last_name(): #test surname too long
    reset()
    with pytest.raises(ValueError, match=r".*"):
        auth_register("validemail1@gmail.com", "validpassword1", "validname","invalidname111111111111111111111111111111111111111111111")

def test_invalid_last_name2(): #test 0 character surname
    reset()
    with pytest.raises(ValueError, match=r".*"):
        auth_register("validemail1@gmail.com", "validpassword1", "validname","")

def test_same_name():
    reset()
    auth_register("validemail1@gmail.com", "validpassword1", "validname","last_name")
    auth_register("validemail2@gmail.com", "validpassword1", "validname","last_name")

def test_long_name():
    reset()
    auth_register("validemail1@gmail.com", "validpassword1", "abcdefghij","abcdefghij")
    auth_register("validemail2@gmail.com", "validpassword1", "abcdefghij","abcdefghij")
