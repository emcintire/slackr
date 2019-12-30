import jwt
from appdata import data, valid_tokens, channels, decodeToken, getMessage, getMessageChannel, isUserChan
from server.error import ValueError, AccessError

def message_react(token, message_id, react_id):
    global data
    global valid_tokens
    global channels
    try:
        u_id = decodeToken(token)
        #check if react_id is valid at the start
        if react_id != 1:
            raise ValueError("Invalid react ID!")

        message = getMessage(message_id)
        channel = getMessageChannel(message_id)
        isUserChan(u_id, channel)
        for react in message["reacts"]: 
            for react_users in react["u_ids"]: #check that the user hasn't already reacted
                if react_users == u_id:
                    raise ValueError("User already has an active react for this message!")
        for react in message["reacts"]:
            if react["react_id"] == react_id:
                react["u_ids"].append(u_id) #add the reaction   
                return {}           
        message["reacts"].append({"react_id" : react_id, "u_ids" :[u_id]}) # genereate the react and ass
        return {}  

    except ValueError as e:
        raise e
    except AccessError as e:
        raise e
