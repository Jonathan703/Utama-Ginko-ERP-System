import os
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import UTC

load_dotenv()

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is not set. This is a critical security risk")

class SecurityConfig:
    JWT_SECRET_KEY = JWT_SECRET_KEY
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 1440))
    BCRYPT_LOG_ROUNDS = int(os.environ.get('BCRYPT_LOG_ROUNDS', 12))
    
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000'). split(',')
    
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    rounds=SecurityConfig.BCRYPT_LOG_ROUNDS
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Args:
    data (Dict): The payload data to encode in the token.
    expires_delta (Optional[timedelta]): The expiration time. If None,
    the default from Security Config is being used.
    
    Returns:
        str: The encoded JWT token
    """
    
    to_encode = data.copy()
    
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=SecurityConfig.JWT_ACCESS_TOKEN_EXPIRES))
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        SecurityConfig.JWT_SECRET_KEY,
        algorithm=SecurityConfig.JWT_ALGORITHM
    )
    
    return encoded_jwt
    
def verify_token(token: str) -> Optional[Dict]:
    try: 
        payload = jwt.decode(
            token,
            SecurityConfig.JWT_SECRET_KEY,
            algorithms=[SecurityConfig.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None