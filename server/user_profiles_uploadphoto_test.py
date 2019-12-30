from .auth_register import auth_register
from .user_profiles_uploadphoto import user_profiles_uploadphoto
from .channels_create import channels_create
from .channel_join import channel_join
from .error import AccessError, ValueError
from appdata import reset
import pytest

def test_successful_upload():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    channels_create(token, 'hello', True)   
    image_url = "https://i.imgur.com/z9QKgcq.jpg"
    assert user_profiles_uploadphoto(token, image_url, 0, 0, 100, 100) == {} #Successful image upload

def test_channel():
    reset()
    token1 = auth_register("ema1l@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    token2 = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    channel_id = channels_create(token1, 'hello', True)  
    channel_join(token1, channel_id)
    image_url = "https://i.imgur.com/z9QKgcq.jpg"
    assert user_profiles_uploadphoto(token2, image_url, 0, 0, 100, 100) == {} #Successful image upload

def test_invalid_url():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    image_url = "https://i.imgur.com/fdasfdasfasdfasd.jpg"
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        user_profiles_uploadphoto(token, image_url, 0, 0, 500, 500) #Unsuccessful image upload as url does not link to image

def test_not_jpg():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    image_url = "https://i.imgur.com/fdasfdasfasdfasd"
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        user_profiles_uploadphoto(token, image_url, 0, 0, 500, 500) #Unsuccessful image upload as url does not link to image

def test_incorrect_dimensions():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    image_url = "https://i.imgur.com/z9QKgcq.jpg"
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        user_profiles_uploadphoto(token, image_url, 0, 0, 1000, 500) #Unsuccessful image upload as dimensions are outside the image

def test_incorrect_dimensions2():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    image_url = "https://i.imgur.com/z9QKgcq.jpg"
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        user_profiles_uploadphoto(token, image_url, -1, 0, 500, 500)#Unsuccessful image upload as dimensions are outside the image

def test_incorrect_dimensions3():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    image_url = "https://i.imgur.com/z9QKgcq.jpg"
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        user_profiles_uploadphoto(token, image_url, 0, -1, 500, 500) #Unsuccessful image upload as dimensions are outside the image

def test_incorrect_dimensions4():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    image_url = "https://i.imgur.com/z9QKgcq.jpg"
    with pytest.raises(ValueError, match=r".*"): #Check Value Error Raised
        user_profiles_uploadphoto(token, image_url, 0, 0, 500, 1000) #Unsuccessful image upload as dimensions are outside the image

def test_overwrite_image():
    reset()
    token = auth_register("email@email.com", "password", "First_Name", "Last_Name")['token'] #Create a new profile
    image_url1 = "https://i.imgur.com/z9QKgcq.jpg"
    image_url2 = "https://i.imgur.com/z9QKgcq.jpg"
    user_profiles_uploadphoto(token, image_url1, 0, 0, 200, 200)
    assert user_profiles_uploadphoto(token, image_url2, 0, 0, 300, 300) == {} #Succesfully overwrite first image

def test_invalid_token():
    reset()
    with pytest.raises(AccessError, match=r".*"): #Check Value Error Raised
        user_profiles_uploadphoto('lmao', 'ayy', 0, 0, 1000, 1000) #Unsuccessful image upload as dimensions are outside the image
