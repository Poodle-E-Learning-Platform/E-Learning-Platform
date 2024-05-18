from data.database import insert_query, read_query
from data.models import User, Teacher, Student, TeacherRegistration, StudentRegistration
from mariadb import IntegrityError
from jose import jwt, JWTError
from datetime import datetime, timedelta
import secrets
import bcrypt


SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"

TOKEN_EXPIRATION_MINUTES = 30

blacklisted_tokens = {}


def create_teacher(data: TeacherRegistration) -> Teacher | None:
    hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())
    try:
        user_id = insert_query(
            """insert into users (email, password, is_admin) values (?, ?, ?)""",
            (data.email, data.password, 0))
        if user_id:
            teacher_id = insert_query(
                """insert into teachers (email, first_name, last_name, password, phone_number,
                 linkedin_account, users_user_id) values (?, ?, ?, ?, ?, ?, ?)""",
                (data.email, data.first_name, data.last_name, data.password,
                 data.phone_number, data.linkedin_account, user_id))
            if teacher_id:
                return Teacher(teacher_id=teacher_id, email=data.email, first_name=data.first_name,
                               last_name=data.last_name, password=hashed_password, phone_number=data.phone_number,
                               linkedin_account=data.linkedin_account, users_user_id=user_id)
        return None
    except IntegrityError:
        return None


def create_student(data: StudentRegistration) -> Student | None:
    hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())
    try:
        user_id = insert_query(
            """insert into users (email, password, is_admin) values (?, ?, ?)""",
            (data.email, data.password, 0))
        if user_id:
            student_id = insert_query(
                """insert into students (users_user_id, email, first_name, last_name, password) 
                   values (?, ?, ?, ?, ?)""",
                (user_id, data.email, data.first_name, data.last_name, data.password))
            if student_id:
                return Student(student_id=student_id, users_user_id=user_id, email=data.email,
                               first_name=data.first_name, last_name=data.last_name, password=hashed_password)
        return None
    except IntegrityError:
        return None


def find_by_email(email: str) -> User | None:
    data = read_query(
        """select * from users where email = ?""",
        (email,))
    return next((User.from_query_result(*row) for row in data), None)


def get_by_id(user_id: int) -> User | None:
    data = read_query("""select * from users where user_id = ?""", (user_id,))
    return next((User.from_query_result(*row) for row in data), None)


def try_login(email: str, password: str) -> User | None:
    user = find_by_email(email)
    if user and user.password == password:
        return user
    return None


def add_token_to_blacklist(token: str):
    if token not in blacklisted_tokens:
        blacklisted_tokens[token] = True


def is_token_blacklisted(token: str) -> bool:
    return token in blacklisted_tokens


def create_jwt_token(user_id: int, email: str) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
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
        return find_by_email(payload.get("email"))
    return None
