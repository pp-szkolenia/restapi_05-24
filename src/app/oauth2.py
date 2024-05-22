from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status
from datetime import datetime, timedelta
from app.models import TokenData
import os
from dotenv import load_dotenv


load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception: HTTPException):
    try:
        print("!!!", token, SECRET_KEY, ALGORITHM)
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)

        id_ = payload.get("user_id")

        if id_ is None:
            print("123")
            raise credentials_exception
        print("4")
        is_admin = payload.get("is_admin")
        print("5")
        token_data = TokenData(user_id=id_, is_admin=is_admin)
        return token_data
    except JWTError:
        print("456")
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                          detail="Could not validate credentials",
                                          headers={"www-authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
