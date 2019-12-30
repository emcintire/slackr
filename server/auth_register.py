import re
import jwt
from datetime import datetime
from server.error import ValueError, AccessError
from appdata import data, getUserByEmail, createUser

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    
def auth_register(email,password,name_first,name_last):

    #check email is valid
    if not re.search(regex,email):  
        raise ValueError("Invalid Email")

    #check password is not less than 6 chars
    if len(password) < 5:
        raise ValueError("Password too short")

    #check email isn't already registered
    for user in data:
        if user['email'] == email:
            raise ValueError("Email already in use")

    #check first name is between 1 and 50 chars
    if len(name_first) > 50:
        raise ValueError("First name has to be 50 characters or less")
    elif len(name_first) == 0:                                            #Assumed that first name has to be at least 1 char
        raise ValueError("Name has to be at least one character")
    
    #check first name is between 1 and 50 chars
    if len(name_last) > 50:
        raise ValueError("Last name has to be 50 characters or less")
    elif len(name_last) == 0:                                             #Assumed that last name has to be at least 1 char
        raise ValueError("Last name has to be at least one character")

    #count how many people have same first name and last name
    count = 0
    for user in data:
        if (user.get('name_first')).lower() == name_first.lower() and (user.get('name_last')).lower() == name_last.lower():
            count += 1

    #If the handle would be greater than 20 digits,
    if len(name_first + name_last) < 20:
        if count == 0:
            handle = name_first.lower() + name_last.lower()
        else:
            handle = name_first.lower() + name_last.lower() + str(count)
    else:
        if count == 0:
            handle = (name_first.lower() + name_last.lower())[0:20]
        else:
            handle = (name_first.lower() + name_last.lower())[0:19] + str(count)             
    
    return createUser(email,password,name_first,name_last, handle)




