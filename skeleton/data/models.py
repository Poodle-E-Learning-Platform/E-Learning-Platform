from pydantic import BaseModel, constr
from datetime import datetime, date


class Section(BaseModel):
    section_id: int
    title: str = constr(pattern="^\w{1,100}$")
    content: str
    description: str | None = None
    external_resource: str | None = None
    course_id = int

    @classmethod
    def from_query_result(cls, section_id, title, content, description, external_resource, course_id):
        return cls(
            section_id=section_id,
            title=title,
            content=content,
            description=description,
            external_resource=external_resource,
            course_id=course_id
        )


class CreateSection(BaseModel):
    title: str
    content: str
    course_id: int


class Course(BaseModel):
    course_id: int
    title: str = constr(pattern="^\w{1,50}$")
    description: str
    objectives: str
    owner_id: int
    is_premium: bool = False
    rating: float = 0.00

    @classmethod
    def from_query_result(cls, course_id, title, description, objectives, owner_id, is_premium, rating):
        return cls(
            course_id=course_id,
            title=title,
            description=description,
            objectives=objectives,
            owner_id=owner_id,
            is_premium=is_premium,
            rating=rating
        )


class CreateCourse(BaseModel):
    title: str = constr(pattern="^\w{1,50}$")
    description: str
    objectives: str
    owner_id: int


class CourseWithSections(BaseModel):
    course_id: int
    title: str = constr(pattern="^\w{1,50}$")
    description: str
    objectives: str
    sections: list[Section | None]


class User(BaseModel):
    user_id: int
    email: str = constr(pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = constr(pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    is_admin: bool = False

    @classmethod
    def from_query_result(cls, user_id, email, password, is_admin=False):
        return cls(
            user_id=user_id,
            email=email,
            password=password,
            is_admin=is_admin
        )


class Teacher(BaseModel):
    teacher_id: int
    email: str = constr(pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    first_name: str
    last_name: str
    password: str = constr(pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    phone_number: str | None = None
    linkedin_account: str | None = None
    users_user_id: int

    @classmethod
    def from_query_result(cls, teacher_id,
                          email,
                          first_name,
                          last_name,
                          password,
                          phone_number,
                          linkedin_account,
                          users_user_id):
        return cls(
            teacher_id=teacher_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            phone_number=phone_number,
            linkedin_account=linkedin_account,
            users_user_id=users_user_id
        )


class Student(BaseModel):
    student_id: int
    users_user_id: int
    email: str = constr(pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    first_name: str
    last_name: str
    password: str = constr(pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")

    @classmethod
    def from_query_result(cls, student_id,
                          email,
                          first_name,
                          last_name,
                          password,
                          users_user_id):
        return cls(
            student_id=student_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            users_user_id=users_user_id
        )


class GetUser(BaseModel):
    user_id: int
    email: str = constr(pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    @classmethod
    def from_query_result(cls, user_id, email):
        return cls(
            user_id=user_id,
            email=email
        )


class LoginInformation(BaseModel):
    email: str
    password: str


# class RegistrationInformation(BaseModel): -> May be we need different registration forms for Teacher/Student/Admin
#     email: str
#     password: str


# class UserCategoryAccess(BaseModel):
#     user_id: int
#     username: str
#     access_level: str
#
#     @classmethod
#     def from_query_result(cls, user_id, username, access_level):
#         return cls(user_id=user_id,
#                    username=username,
#                    access_level=access_level
#                    )


# ===============================================================================================================

# class Reply(BaseModel):
#     id: int
#     text: str
#     topic_id: int
#     user_id: int
#     creation_date: datetime
#
#     @classmethod
#     def from_query_result(cls, reply_id, text, topic_id, user_id, creation_date):
#         return cls(
#             id=reply_id,
#             text=text,
#             topic_id=topic_id,
#             user_id=user_id,
#             creation_date=creation_date
#         )
#
#
# class CreateReply(BaseModel):
#     text: str
#
#
# class ChooseBestReply(BaseModel):
#     reply_id: int
#
#
# class ReplyWithVotes(BaseModel):
#     id: int
#     text: str
#     topic_id: int
#     user_id: int
#     creation_date: datetime
#     vote_type: int
#
#
# class TopicWithReplies(BaseModel):
#     category_id: int
#     title: str
#     user_id: int
#     best_reply: int | None
#     is_locked: bool
#     replies: list[Reply | None]
#
#
# class Vote(BaseModel):
#     id: int
#     reply_id: int
#     user_id: int
#     vote_type: bool | None
#
#
# class Message(BaseModel):
#     id: int
#     text: str
#     sender_id: int
#     receiver_id: int
#     creation_date: datetime
#
#     @classmethod
#     def from_query_result(cls, message_id, text, sender_id, receiver_id, creation_date):
#         return cls(
#             id=message_id,
#             text=text,
#             sender_id=sender_id,
#             receiver_id=receiver_id,
#             creation_date=creation_date
#         )
#
#
# class CreateMessage(BaseModel):
#     text: str
