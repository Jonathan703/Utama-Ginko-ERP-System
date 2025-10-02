from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Optional
from app.models.auth import UserLogin, User
from app.config.security import verify_password, create_access_token
from app.services.user_service import get_user_by_username

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def login_user(db: Session, user_data: UserLogin):
    """
    Authenticate and logs in a userm generating a JWT token.
    
    Raises:
    HTTPException: If authentication fails or the user is inactive.
    """
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNATHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    access_token_expires = timedelta(minutes=1440)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": str(user.id),
            "role_id": user.role.id if user.role else None,
            "role_name": user.role.name if user.role else "user"
        },
        expires_delta=access_token_expires
    )
    
    return{
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first.name,
            "last_name": user.last.name,
            "role_name": user.role.name if user.role else "user",
            "is_active": user.is_active
        }
    }
    
def get_current_user(db: Session, token: str):
    from app.config.security import verify_token
    
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate the credentials",
            headers={"WWW_Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate the credentials",
            headers={"WWW_Authenticate": "Bearer"},
        )
        
    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW_Authenticate": "Bearer"},
        )
        
    return user

def check_user_permission(user, required_role: str = None, required_permissions: list = None):
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    if user.role and user.role.name == "admin":
        return True
    
    if required_permissions and user.role:
        role_permissions = user.role.permissions if user.role.permissions else set()
            
        if not set(required_permissions).issubset(role_permissions):
            missing_permissions = set(required_permissions) - role_permissions
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access is denied. Missing permissions: {', '. join(missing_permissions)}"
            )
    return True
