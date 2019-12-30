import pytest 
import httplib2
from urllib.parse import urlencode
import ast
import time

def test_http_server(): #valid case
    port = '6901'
    h = httplib2.Http()

    # Auth_register
    em = 'kappa0@gmail.com'
    nf = 'Kappa'
    nl = 'Johnson'
    pw = 'abc123'
    data = {'email':em, 'password':pw, 'name_first':nf, 'name_last':nl}
    resp, cont = h.request('http://127.0.0.1:'+port+'/auth/register', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    cont_dict = ast.literal_eval(cont.decode())
    assert cont_dict['u_id'] == 0    

    # Auth_logout
    token = cont_dict['token']
    data = {'token':token}
    resp, cont = h.request('http://127.0.0.1:'+port+'/auth/logout', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{"is_success": true}'

    # Auth_login
    em = 'kappa0@gmail.com'
    pw = 'abc123'
    data = {'email':em, 'password':pw}
    resp, cont = h.request('http://127.0.0.1:'+port+'/auth/login', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    cont_dict = ast.literal_eval(cont.decode())
    assert cont_dict['u_id'] == 0

    # Channels_create
    token = cont_dict['token']
    nm = 'abc123'
    ip = True
    data = {'token':token, 'name':nm, 'is_public':ip}
    resp, cont = h.request('http://127.0.0.1:'+port+'/channels/create', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{"channel_id": 0}'

    # Channels_list
    resp, cont = h.request('http://127.0.0.1:'+port+'/channels/list?token='+str(token), method='GET')
    assert resp['status'] == '200'
    assert cont.decode() == '{"channels": [{"channel_id": 0, "name": "abc123"}]}'

    # Channels_listall
    resp, cont = h.request('http://127.0.0.1:'+port+'/channels/listall?token='+str(token), method='GET')
    assert resp['status'] == '200'
    assert cont.decode() == '{"channels": [{"channel_id": 0, "name": "abc123"}]}'

    # User_profile
    resp, cont = h.request('http://127.0.0.1:'+port+'/user/profile?token='+str(token)+'&'+'u_id=0', method='GET')
    assert resp['status'] == '200'
    assert cont.decode() == '{"email": "kappa0@gmail.com", "name_first": "Kappa", "name_last": "Johnson", "handle_str": "kappajohnson", "profile_img_url": null}'

    # User_profile_setname
    data = {'token':token, 'name_first':'hello', 'name_last':'there'}
    resp, cont = h.request('http://127.0.0.1:'+port+'/user/profile/setname', method='PUT', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # User_profile_setemail
    data = {'token':token, 'email':'hello@gmail.com'}
    resp, cont = h.request('http://127.0.0.1:'+port+'/user/profile/setemail', method='PUT', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # User_profile_sethandle
    data = {'token':token, 'handle_str':'ayylmao'}
    resp, cont = h.request('http://127.0.0.1:'+port+'/user/profile/sethandle', method='PUT', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # User_profile_uploadphoto
    data = {'token':token, 'img_url':'https://i.imgur.com/z9QKgcq.jpg', 'x_start':0, 'y_start':0, 'x_end':500, 'y_end':500}
    resp, cont = h.request('http://127.0.0.1:'+port+'/user/profiles/uploadphoto', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # User_profile
    resp, cont = h.request('http://127.0.0.1:'+port+'/user/profile?token='+str(token)+'&'+'u_id=0', method='GET')
    assert resp['status'] == '200'
    assert cont.decode() == '{"email": "hello@gmail.com", "name_first": "hello", "name_last": "there", "handle_str": "ayylmao", "profile_img_url": "http://127.0.0.1:'+port+'/static/0_profile_image.jpg"}'

    # Auth_register2
    em = 'kappa1@gmail.com'
    nf = 'Kappa'
    nl = 'Johnson'
    pw = 'abc123'
    data = {'email':em, 'password':pw, 'name_first':nf, 'name_last':nl}
    resp, cont = h.request('http://127.0.0.1:'+port+'/auth/register', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    user2 = ast.literal_eval(cont.decode())
    assert user2['u_id'] == 1
    token2 = user2['token']

    # Users_all
    resp, cont = h.request('http://127.0.0.1:'+port+'/users/all?token='+str(token)+'&'+'u_id=0', method='GET')
    assert resp['status'] == '200'
    assert cont.decode() == '{"users": [{"u_id": 0, "email": "hello@gmail.com", "name_first": "hello", "name_last": "there", "handle_str": "ayylmao", "profile_img_url": "http://127.0.0.1:'+port+'/static/0_profile_image.jpg"}, {"u_id": 1, "email": "kappa1@gmail.com", "name_first": "Kappa", "name_last": "Johnson", "handle_str": "kappajohnson", "profile_img_url": null}]}'

    # Channel_details
    data = {'token':token, 'channel_id':0}
    resp, cont = h.request('http://127.0.0.1:'+port+'/channel/details?token='+str(token)+'&channel_id=0', method='GET')
    assert resp['status'] == '200'
    assert cont.decode() == '{"name": "abc123", "owner_members": [{"u_id": 0, "name_first": "hello", "name_last": "there", "profile_img_url": "http://127.0.0.1:'+port+'/static/0_profile_image.jpg"}], "all_members": [{"u_id": 0, "name_first": "hello", "name_last": "there", "profile_img_url": "http://127.0.0.1:'+port+'/static/0_profile_image.jpg"}]}'

    # Channel_invite
    data = {'token':token, 'channel_id':0, 'u_id':1}
    resp, cont = h.request('http://127.0.0.1:'+port+'/channel/invite', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # Channel_details
    data = {'token':token, 'channel_id':0}
    resp, cont = h.request('http://127.0.0.1:'+port+'/channel/details?token='+str(token)+'&channel_id=0', method='GET')
    assert resp['status'] == '200'
    assert cont.decode() == '{"name": "abc123", "owner_members": [{"u_id": 0, "name_first": "hello", "name_last": "there", "profile_img_url": "http://127.0.0.1:'+port+'/static/0_profile_image.jpg"}], "all_members": [{"u_id": 0, "name_first": "hello", "name_last": "there", "profile_img_url": "http://127.0.0.1:'+port+'/static/0_profile_image.jpg"}, {"u_id": 1, "name_first": "Kappa", "name_last": "Johnson", "profile_img_url": null}]}'

    # Channel_leave
    data = {'token':token2, 'channel_id':0}
    resp, cont = h.request('http://127.0.0.1:'+port+'/channel/leave', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # Channel_join
    data = {'token':token2, 'channel_id':0}
    resp, cont = h.request('http://127.0.0.1:'+port+'/channel/join', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # Channel_addowner
    data = {'token':token, 'channel_id':0, 'u_id':1}
    resp, cont = h.request('http://127.0.0.1:'+port+'/channel/addowner', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # Channel_removeowner
    data = {'token':token, 'channel_id':0, 'u_id':1}
    resp, cont = h.request('http://127.0.0.1:'+port+'/channel/removeowner', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # Message_send
    data = {'token':token, 'channel_id': 0, 'message':'hello'}
    resp, cont = h.request('http://127.0.0.1:'+port+'/message/send', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{"message_id": 0}'

    # Message_edit
    data = {'token':token, 'message_id':0, 'message':'hello there'}
    resp, cont = h.request('http://127.0.0.1:'+port+'/message/edit', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # Message_react
    data = {'token':token, 'message_id':0, 'react_id':1}
    resp, cont = h.request('http://127.0.0.1:'+port+'/message/react', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # Message_react
    data = {'token':token, 'message_id':0, 'react_id':1}
    resp, cont = h.request('http://127.0.0.1:'+port+'/message/unreact', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # Message_pin
    data = {'token':token, 'message_id':0, 'react_id':1}
    resp, cont = h.request('http://127.0.0.1:'+port+'/message/pin', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # Message_unpin
    data = {'token':token, 'message_id':0, 'react_id':1}
    resp, cont = h.request('http://127.0.0.1:'+port+'/message/unpin', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # Channel_messages
    resp, cont = h.request('http://127.0.0.1:'+port+'/channel/messages?token='+str(token)+'&channel_id=0&start=0', method='GET')
    assert resp['status'] == '200'
  
    assert '"message_id": 0' in cont.decode()
    assert '"u_id": 0' in cont.decode()
    assert '"message": "hello there"' in cont.decode()
    assert '"reacts": [{"react_id": 1, "u_ids": [], "is_this_user_reacted": false}]' in cont.decode()
    assert '"is_pinned": false' in cont.decode()
    

    # Search
    resp, cont = h.request('http://127.0.0.1:'+port+'/search?token='+token+'&query_str=there', method='GET')
    assert resp['status'] == '200'
    assert '"message_id": 0' in cont.decode()
    assert '"u_id": 0' in cont.decode()
    assert '"message": "hello there"' in cont.decode()
    assert '"reacts": [{"react_id": 1, "u_ids": [], "is_this_user_reacted": false}]' in cont.decode()
    assert '"is_pinned": false' in cont.decode()

    # Message_remove
    data = {'token': token, 'message_id':0}
    resp, cont = h.request('http://127.0.0.1:'+port+'/message/remove', method='DELETE', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # Admin_userpermission_change
    data = {'token':token, 'u_id':1, 'permission_id':1}
    resp, cont = h.request('http://127.0.0.1:'+port+'/admin/userpermission/change', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # Standup_start
    data = {'token':token, 'channel_id':0, 'length':2}
    resp, cont = h.request('http://127.0.0.1:'+port+'/standup/start', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert '{"time_finish": ' in cont.decode()

    # Standup_active
    data = {'token':token, 'channel_id':0}
    resp, cont = h.request('http://127.0.0.1:'+port+'/standup/active?token='+token+'&channel_id=0', method='GET')
    assert resp['status'] == '200'
    assert '{"is_active": true, "time_finish": ' in cont.decode()

    # Standup_send
    data = {'token':token, 'channel_id':0, 'message':'greetings traveller'}
    resp, cont = h.request('http://127.0.0.1:'+port+'/standup/send', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    time.sleep(2)
    # Channel_messages
    resp, cont = h.request('http://127.0.0.1:'+port+'/channel/messages?token='+str(token)+'&channel_id=0&start=0', method='GET')
    assert resp['status'] == '200'
    assert '"message_id": 0' in cont.decode()
    assert '"u_id": 0' in cont.decode()
    assert '"message": "hello: greetings traveller "' in cont.decode()
    assert '"reacts": []' in cont.decode()    

    # Auth_passwordreset_request
    data = {'email':em}
    resp, cont = h.request('http://127.0.0.1:'+port+'/auth/passwordreset/request', method='POST', headers={'Content-type': 'application/x-www-form-urlencoded'}, body=urlencode(data))
    assert resp['status'] == '200'
    assert cont.decode() == '{}'

    # Auth_passwordreset_reset
    # untestable
