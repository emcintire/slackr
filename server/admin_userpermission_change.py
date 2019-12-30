import jwt
from appdata import data, channels, decodeToken, getUser, setPermission
from server.error import ValueError, AccessError

def admin_userpermission_change(token, u_id, permission_id):
    
    try:
        # Check if user is authenticated and get the requesting user ID from token
        granterID = decodeToken(token)

        # Check if the target uID format is valid
        if not u_id.isdigit():
            raise ValueError("Invalid user ID!")

        # Check if the target permission ID is valid
        if int(permission_id) > 3 or int(permission_id) < 1:
            raise ValueError("Invalid permission id")

        # Find the requesting user
        permissions = getUser(granterID)['permission_id']

        # Check if requesting user has permissions for the action
        if permissions < 3:
            setPermission(u_id, permission_id)
            return {}
        raise AccessError("Granter is not an admin or owner")     
        
    except ValueError as e:
        raise e
    except AccessError as e:
        raise e 
