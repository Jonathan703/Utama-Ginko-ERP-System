from fastapi import Request, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.services.auth_service import get_current_user, check_user_permission

def get_token_from_header(request: Request) -> Optional[str]:
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        return None

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
        return token
    except ValueError:
        return None

async def get_current_active_user(
    db: Session = Depends(get_db),
    token: str = Depends(get_token_from_header)
):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Autheticate": "Bearer"},
        )
        
    user = get_current_user(db, token)
    if not user:
        user = get_current_user(db, token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

def require_role(required_role: str):
    def role_checker(
        user = Depends(get_current_active_user)
    ):
        check_user_permission(user, required_role=required_role)
        return user
    return role_checker

def require_permission(required_permissions: list):
    def permission_checker(
        user = Depends(get_current_active_user)
    ):
        check_user_permission(user, required_permissions=required_permissions)
        return user
    return permission_checker