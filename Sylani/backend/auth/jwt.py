from jose import jwt, JWTError
from datetime import datetime, timedelta
from config import ACCESS_EXPIRE_MINUTES, ACCESS_SECRET_KEY, ALGORITHM, RESET_EXPIRE_MINUTES, RESET_SECRET_KEY



def create_access_token(email):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    return jwt.encode({"sub": email, "exp": expire}, ACCESS_SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token):
    try:
        payload = jwt.decode(token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


def create_reset_token(email):
    expire = datetime.utcnow() + timedelta(minutes=RESET_EXPIRE_MINUTES)
    return jwt.encode({"sub": email, "exp": expire}, RESET_SECRET_KEY, algorithm=ALGORITHM)

def verify_reset_token(token):
    try:
        payload = jwt.decode(token, RESET_SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None