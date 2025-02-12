from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

def validate_token(token):
    jwt_authentication = JWTAuthentication()
    try:
        if token.startswith("Bearer "):
            token = token.split(" ")[1]
        validated_token = jwt_authentication.get_validated_token(token)
        user = jwt_authentication.get_user(validated_token)
        return {"user_id": user.id, "is_authenticated": True}
    except (InvalidToken, TokenError):
        return {"is_authenticated": False}