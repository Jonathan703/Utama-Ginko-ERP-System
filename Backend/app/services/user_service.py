from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime, UTC
from getpass import get_user
from app.models.user import User, Role
from app.models.auth import UserCreate, UserUpdate
from app.config.security import get_password_hash, verify_password

def check_last_admin(db: Session, user_id: int) -> None:
    user = get_user(db, user_id)
    if user and user.role and user.role.name == "admin":
        admin_count = db.query(User).join(Role).filter(
            Role.name == "admin",
            User.is_active == True,
            User.id != user_id
        ).count()
        if admin_count == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Operation denied: Cannot Modify or remove the last active administrator."
            )

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip : int = 0, limit: int = 100) -> List[User]:
    return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()

def get_users_by_role(db: Session, role_id: int, skip:int = 0, limit: int = 100) -> List[User]:
    return db.query (User).filter(User.role_id == role_id).offset(skip).limit(limit).all()

def create_user(db: Session, user_data: UserCreate) -> User:
    try:
        role = db.query(Role).filter(Role.id == user_data.role.id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role ID"
            )

        if get_user_by_username(db, user_data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
        if get_user_by_email(db, user_data.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            **user_data.model_dump(exclude={'password'}),
            password_hash=hashed_password,
            is_active=True,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    except IntegrityError as e:
        db.rillback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User creation failed due to unique violation."
        )
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
        
def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    check_last_admin(db, user_id)
    
    try:
        update_data = user_data.model_dump(exlude_unset=True)
        
        if 'password' in update_data and update_data['password']:
            db_user.password_hash = get_password_hash(update_data.pop('password'))
            
            for field, value in update_data.items():
                setattr(db_user, field, value)
                
            db_user.update_at = datetime.now(UTC)
            db.commit()
            db.refresh(db_user)
            
            return db_user
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists."
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal server error during user update."
        )

def update_user_password(db:)