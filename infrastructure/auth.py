from jose import JWTError, jwt
import bcrypt
#from passlib.context import CryptContext
from datetime import datetime, timedelta
from config import Config
import copy
import pytz
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_pin(plain_pin: str, hashed_pin: bytes) -> bool:
    # Convert plain pin to bytes before checking
    plain_pin_bytes = plain_pin.encode('utf-8')
    return bcrypt.checkpw(plain_pin_bytes, hashed_pin)

def get_pin_hash(pin: str) -> bytes:
    # Convert pin to bytes before hashing
    pin_bytes = pin.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pin_bytes, salt)
    return hashed_password


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = copy.deepcopy(data)
    if expires_delta:
        expire = datetime.now(pytz.UTC) + expires_delta
    else:
        expire = datetime.now(pytz.UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        phone: str = payload.get("sub")
        if phone is None:
            return None
        return phone
    except JWTError:
        return None
