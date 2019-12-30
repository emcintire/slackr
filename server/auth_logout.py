from appdata import removeToken

def auth_logout(token):
    
    # Check if token is currently authenticated
    return {"is_success": removeToken(token)}
