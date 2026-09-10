from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()
SECRET_KEY = "your_secret_key"  # Read from environment variable or config file
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict[str, str], expires_delta: timedelta = timedelta(minutes=150)) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)