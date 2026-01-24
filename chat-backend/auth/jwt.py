from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "secret-key-1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES= 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])