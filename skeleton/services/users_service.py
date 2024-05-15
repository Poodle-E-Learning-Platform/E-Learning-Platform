from data.database import insert_query, read_query
from data.models import User
from mariadb import IntegrityError


_SEPARATOR = ';'

# passwords should be secured as hashstrings in DB
# def _hash_password(password: str):
#     from hashlib import sha256
#     return sha256(password.encode('utf-8')).hexdigest()


def find_by_username(username: str) -> User | None:
    data = read_query(
        """select user_id, username, password, email, name, is_admin from users where username = ?""",
        (username,))

    return next((User.from_query_result(*row) for row in data), None)


def get_by_id(user_id: int) -> User | None:
    data = read_query("""select * from users where user_id = ?""",
        (user_id,))

    return next((User.from_query_result(*row) for row in data), None)


def try_login(username: str, password: str) -> User | None:
    user = find_by_username(username)

    # password = _hash_password(password)
    return user if user and user.password == password else None


def create(username: str, password: str, email: str, name: str) -> User | None:
    # password = _hash_password(password)
    try:
        generated_id = insert_query(
            """insert into users(username, password, email, name) values (?,?,?,?)""",
            (username, password, email, name))

        return User(id=generated_id, username=username, password='', email=email, name=name, is_admin=False)

    except IntegrityError:
        return None


def create_token(user: User) -> str:
    return f'{user.id}{_SEPARATOR}{user.username}'


def is_authenticated(token: str) -> bool:
    return any(read_query(
        """select 1 from users where user_id = ? and username = ?""",
        token.split(_SEPARATOR)))


def from_token(token: str) -> User | None:
    _, username = token.split(_SEPARATOR)

    return find_by_username(username)
