import jwt
import threading
from appdata import data, valid_tokens, channels, index, decodeToken, getChannel, isUserChan
from server.error import ValueError, AccessError
from datetime import datetime, timezone

def message_sendlater(token, channel_id, message, time_sent):
    global data
    global channels
    global index

    try:
        u_id = decodeToken(token)
        channel = getChannel(channel_id)

        if isUserChan(u_id, channel):
            if len(message) > 1000:
                raise ValueError("Message can not be greather than 1000 character limit")
            elif len(message) == 0: #this appears to be handled by front end...
                raise ValueError("Message can not be empty")
            else:
                timeNow = datetime.now(timezone.utc).timestamp() #check timer is not in past
                if time_sent >= timeNow:
                    messageID = index
                    index += 1
                    timeDiff = (time_sent - timeNow)
                    timer = threading.Timer(timeDiff, sendNow, [channel, message, messageID, u_id]) #start a timer
                    timer.start()
                    return messageID
                raise ValueError("Time can not be in the past!")
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e


def sendNow(channel, message, messageID, u_id):
    timeStamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds() # generate timestamp
    newMessage = { "message_id" : messageID, "u_id" : u_id, "message" : message, "time_created" : timeStamp, "reacts" : [], "is_pinned" : False  }
    channel["messages"].append(newMessage)  #add the message
    return True #EiThEr AlL rEtUrN sTaTeMeNtS iN a FuNcTiOn ShOuLd ReTuRn An ExPrEsSiOn, Or NoNe Of ThEm ShOuLd. (InCoNsIsTeNt-ReTuRn-StAtEmEnTs)
