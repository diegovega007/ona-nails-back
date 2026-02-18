from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..services.auth_service import AuthService
from typing import Annotated
security = HTTPBearer()

def authorization_header(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> dict:
    try:
        auth_service = AuthService()
        username = auth_service.decode_token(credentials.credentials)
        return {"username": username}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )