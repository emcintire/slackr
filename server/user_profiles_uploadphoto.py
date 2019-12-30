from server.error import ValueError, AccessError
from appdata import channels, data, valid_tokens, getHostName, decodeToken
import re
from PIL import Image
import requests
import jwt
import urllib.request

def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    global data
    global channels
    try:
        host_name = 'http://' + getHostName() + '/'
        u_id = decodeToken(token)
        # validate file format
        if ".jpg" not in img_url:
            raise ValueError('Not a JPG')
        # set path
        path = "static/" + str(u_id) + "_profile_image" + ".jpg"
        # open the image
        try:
            urllib.request.urlretrieve(img_url, path)
            image = Image.open(path)
        except:
            raise ValueError('Invalid url')
        #cropping setup
        width, height = image.size

        border = (x_start, y_start, x_end, y_end)  
        if x_start < 0 or x_start > width:
            raise ValueError('Dimensions incorrect')
        if y_start < 0 or y_start > height:
            raise ValueError('Dimensions incorrect')
        if x_end < 0 or x_end > width:
            raise ValueError('Dimensions incorrect')
        if y_end < 0 or y_end > height:
            raise ValueError('Dimensions incorrect')
        # crop and serve
        (image.crop(border)).save(path, "JPEG")
        data[u_id]['profile_img_url'] = host_name + path
        for channel in channels:
            for user in channel['all_members']:
                if user['u_id'] == u_id:
                    user['profile_img_url'] = host_name + path
            for user in channel['owner_members']:
                if user['u_id'] == u_id:
                    user['profile_img_url'] = host_name + path
        return {}
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e



