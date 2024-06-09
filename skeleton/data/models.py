from pydantic import BaseModel, constr, Field, EmailStr
from typing import Optional, List, Dict


class Section(BaseModel):
    section_id: int
    title: str = Field(..., pattern="^\w{1,100}$", title="Section Title", example="Present Simple Tense")
    content: str = Field(..., title="Section Content",
                         example="The simple present is a verb tense with two main uses...")
    description: Optional[str] = Field(None, title="Section Description",
                                       example="Introduction to Present Simple Tense.")
    external_resource: Optional[str] = Field(None, title="External Resource URL",
                                             example="http://grammerly.com/resource")
    course_id: int = Field(..., title="Course ID", example=1)

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
    course_id: int = Field(..., title="Course ID", example=1)
    title: str = Field(..., pattern="^\w{1,100}$", title="Section Title", example="Past Simple Tense")
    content: str = Field(..., title="Section Content",
                         example="The simple past is a verb tense that is used to talk about things that happened or existed before now...")
    description: Optional[str] = Field(None, title="Section Description", example="Introduction to Past Simple Tense.")
    external_resource: Optional[str] = Field(None, title="External Resource URL",
                                             example="http://grammerly.com/resource")


class UpdateSection(BaseModel):
    title: str = Field(..., pattern="^\w{1,100}$", title="Section Title", example="Past Simple Tense")
    content: str = Field(..., title="Section Content",
                         example="Here are the most common irregular verbs in English, with their past tense forms...")
    description: Optional[str] = Field(None, title="Section Description",
                                       example="Past Simple Tense - Advanced concepts")
    external_resource: Optional[str] = Field(None, title="External Resource URL",
                                             example="http://learnenglish.britishcouncil.org/grammar/resource")


class Course(BaseModel):
    course_id: int
    title: str = Field(..., pattern="^\w{1,50}$", title="Course Title", example="English A1")
    description: str = Field(..., title="Course Description",
                             example="Introductory course covering the alphabet, common grammar points and basic words")
    objectives: str = Field(..., title="Course Objectives",
                            example="Learn how to introduce yourself and have a small talk on various common subjects.")
    owner_id: int = Field(..., title="Owner ID", example=1)
    is_premium: bool = Field(False, title="Is Premium", example=False)
    rating: float = Field(0.00, title="Course Rating (1-5)", example=4.5)

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
    title: str = Field(..., pattern="^\w{1,50}$", title="Course Title", example="B2 - English")
    description: str = Field(..., title="Course Description",
                             example="A course for students with a good grasp of the basic concepts and applies them on practice.")
    objectives: str = Field(..., title="Course Objectives",
                            example="After the course students should be able to write about and describe experiences, events, wishes and aspirations, and explain opinions and plans.")
    is_premium: bool = Field(..., title="Is Premium", example=False)


class UpdateCourse(BaseModel):
    title: str = Field(..., pattern="^\w{1,50}$", title="Course Title", example="A1 - English")
    description: str = Field(..., title="Course Description",
                             example="Introductory course covering the alphabet, common grammar points and basic words")
    objectives: str = Field(..., title="Course Objectives",
                            example="Learn to understand and use very common everyday expressions and simple phrases for immediate needs.")
    is_premium: bool = Field(..., title="Is Premium", example=False)


class CourseWithSections(BaseModel):
    course_id: int
    title: str = Field(..., pattern="^\w{1,50}$", title="Course Title", example="A1 - English")
    description: str = Field(..., title="Course Description",
                             example="Introductory course covering the alphabet, common grammar points and basic words")
    objectives: str = Field(..., title="Course Objectives",
                            example="Learn to understand and use very common everyday expressions and simple phrases for immediate needs.")
    owner_id: int = Field(..., title="Owner ID", example=1)
    is_premium: bool = Field(False, title="Is Premium", example=False)
    sections: List[Optional[Section]] = Field(..., title="Course Sections")


class User(BaseModel):
    user_id: int
    email: EmailStr = Field(..., title="Email Address", example="georgi.todorov@gmail.com")
    password: str = Field(..., title="Password", example="123qwe456")
    is_admin: bool = Field(False, title="Is Admin", example=False)

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
    email: EmailStr = Field(..., title="Email Address", example="petar.stoianov@gmail.com")
    first_name: str = Field(..., title="First Name", example="Petar")
    last_name: str = Field(..., title="Last Name", example="Stoianov")
    password: str = Field(..., title="Password", example="123qweasd")
    phone_number: Optional[str] = Field(None, title="Phone Number", example="+359888111222")
    linkedin_account: Optional[str] = Field(None, title="LinkedIn Account",
                                            example="https://linkedin.com/in/petarstoianov")
    users_user_id: int = Field(..., title="User ID", example=1)

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
    email: EmailStr = Field(..., title="Email Address", example="snejana.todorova@gmail.com")
    first_name: str = Field(..., title="First Name", example="Snejana")
    last_name: str = Field(..., title="Last Name", example="Todorova")
    password: str = Field(..., title="Password", example="qwe123asd")
    phone_number: Optional[str] = Field(None, title="Phone Number", example="+359888777999")
    linkedin_account: Optional[str] = Field(None, title="LinkedIn Account", example="https://linkedin.com/in/snejana")


class Student(BaseModel):
    student_id: int
    users_user_id: int
    email: EmailStr = Field(..., title="Email Address", example="a.aleksandrov@gmail.com")
    first_name: str = Field(..., title="First Name", example="Aleksandar")
    last_name: str = Field(..., title="Last Name", example="Aleksandrov")
    password: str = Field(..., title="Password", example="asd456qwe")

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
    email: EmailStr = Field(..., title="Email Address", example="p.ivanov@gmail.com")
    first_name: str = Field(..., title="First Name", example="Pavel")
    last_name: str = Field(..., title="Last Name", example="Ivanov")
    password: str = Field(..., title="Password", example="456asd123")


class StudentReport(BaseModel):
    student_id: int
    first_name: str = Field(..., title="First Name", example="Pavel")
    last_name: str = Field(..., title="Last Name", example="Ivanov")
    email: EmailStr = Field(..., title="Email Address", example="p.ivanov@gmail.com")
    course_id: int
    course_title: str = Field(..., title="Course Title", example="Beginner Level - English")

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
    email: EmailStr = Field(..., title="Email Address", example="georgi.todorov@gmail.com")

    @classmethod
    def from_query_result(cls, user_id, email):
        return cls(
            user_id=user_id,
            email=email
        )


class LoginInformation(BaseModel):
    email: EmailStr = Field(..., title="Email Address", example="a.aleksandrov@gmail.com")
    password: str = Field(..., title="Password", example="asd456qwe")


class Tag(BaseModel):
    tag_id: int
    tag_name: str = Field(..., title="Tag Name", example="Intermediate")


class CreateTagRequest(BaseModel):
    tag_name: str = Field(..., title="Tag Name", example="Beginner")
