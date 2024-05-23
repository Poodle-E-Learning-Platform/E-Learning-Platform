from pydantic import BaseModel, constr
from datetime import datetime, date


class Section(BaseModel):
    section_id: int
    title: str = constr(pattern="^\w{1,100}$")
    content: str
    description: str | None = None
    external_resource: str | None = None
    course_id: int

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
    course_id: int
    title: str = constr(pattern="^\w{1,100}$")
    content: str
    description: str | None = None
    external_resource: str | None = None


class UpdateSection(BaseModel):
    title: str = constr(pattern="^\w{1,100}$")
    content: str
    description: str | None = None
    external_resource: str | None = None


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
    is_premium: bool


class UpdateCourse(BaseModel):
    title: str = constr(pattern="^\w{1,50}$")
    description: str
    objectives: str
    is_premium: bool


class CourseWithSections(BaseModel):
    course_id: int
    title: str = constr(pattern="^\w{1,50}$")
    description: str
    objectives: str
    owner_id: int
    is_premium: bool
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


class TeacherRegistration(BaseModel):
    email: str = constr(pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    first_name: str
    last_name: str
    password: str = constr(pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    phone_number: str | None = None
    linkedin_account: str | None = None


class Student(BaseModel):
    student_id: int
    users_user_id: int
    email: str = constr(pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    first_name: str
    last_name: str
    password: str = constr(pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")

    @classmethod
    def from_query_result(cls, student_id,
                          users_user_id,
                          email,
                          first_name,
                          last_name,
                          password):
        return cls(
            student_id=student_id,
            users_user_id=users_user_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )


class StudentRegistration(BaseModel):
    email: str = constr(pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    first_name: str
    last_name: str
    password: str = constr(pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")


class StudentReport(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    email: str
    course_id: int
    course_title: str

    @classmethod
    def from_query_result(cls, student_id, first_name, last_name, email, course_id, course_title):
        return cls(student_id=student_id,
                   first_name=first_name,
                   last_name=last_name,
                   email=email,
                   course_id=course_id,
                   course_title=course_title)


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


class Tag(BaseModel):
    tag_id: int
    tag_name: str


class CreateTagRequest(BaseModel):
    tag_name: str
