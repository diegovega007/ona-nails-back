import hashlib
from jose import jwt
from datetime import datetime, timezone, timedelta
import os
from ..exeptions.auth_exeption import TokenExpiredException
import bcrypt

class AuthService:
    SECRET_KEY = os.getenv("SECRET_KEY")

    def hash_password(self, password: str) -> str:
        pre_hash = hashlib.sha256(password.encode()).hexdigest()
        password_bytes = pre_hash.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pre_hash = hashlib.sha256(plain_password.encode()).hexdigest()
        password_bytes = pre_hash.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    def encode_token(self, username: str, password: str, expires_in: timedelta) -> str:
        token = jwt.encode(
            {
                "sub": username,
                "password": password,
                "exp": datetime.now(timezone.utc) + expires_in
            },
            self.SECRET_KEY,
            algorithm="HS256"
        )
        return token

    def decode_token(self, token: str) -> dict:
        token = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
        if token["exp"] < datetime.now(timezone.utc).timestamp():
            raise TokenExpiredException()
        return token.get("sub")