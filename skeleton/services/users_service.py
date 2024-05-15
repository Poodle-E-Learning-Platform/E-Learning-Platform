from data.database import insert_query, read_query
from data.models import User
from mariadb import IntegrityError
from jose import jwt, JWTError
from datetime import datetime, timedelta
from common.responses import Conflict
import secrets
import bcrypt


SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"

TOKEN_EXPIRATION_MINUTES = 30

blacklisted_tokens = {}


def create(username: str, password: str, email: str, name: str) -> User | None:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        generated_id = insert_query(
            """insert into users(username, password, email, name) values (?,?,?,?)""",
            (username, hashed_password.decode('utf-8'), email, name))
        return User(id=generated_id, username=username, password=hashed_password.decode('utf-8'), email=email, name=name, is_admin=False)
    except IntegrityError:
        return None


def find_by_username(username: str) -> User | None:
    data = read_query(
        """select * from users where username = ?""",
        (username,))
    return next((User.from_query_result(*row) for row in data), None)


def get_by_id(user_id: int) -> User | None:
    data = read_query("""select * from users where user_id = ?""", (user_id,))
    return next((User.from_query_result(*row) for row in data), None)


def try_login(username: str, password: str) -> User | None:
    user = find_by_username(username)
    if user and user.password == password:
        return user
    return None


def add_token_to_blacklist(token: str):
    if token not in blacklisted_tokens:
        blacklisted_tokens[token] = True


def is_token_blacklisted(token: str) -> bool:
    return token in blacklisted_tokens


def create_jwt_token(user_id: int, username: str) -> str:
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError as e:
        raise JWTError("Token verification failed") from e


def create_token(user: User) -> str:
    return create_jwt_token(user.id, user.username)


def is_authenticated(token: str) -> bool:
    payload = verify_jwt_token(token)
    return payload is not None


def from_token(token: str) -> User | None:
    payload = verify_jwt_token(token)
    if payload:
        return find_by_username(payload.get("username"))
    return None
