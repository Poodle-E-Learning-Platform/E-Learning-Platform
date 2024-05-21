from data.database import insert_query, read_query, update_query, delete_query
from data.models import Course, CreateCourse, CourseWithSections, Section, UpdateCourse
from mariadb import IntegrityError
from services import users_service
from common.responses import NotFound, Forbidden


def get_all_teacher_courses(user_id: int) -> list[CourseWithSections] | NotFound | None:
    teacher = users_service.get_teacher_by_user_id(user_id)
    if not teacher:
        return NotFound(content="Teacher not found!")

    owner_id = teacher.teacher_id

    course_query = """select * from courses where owner_id = ?"""
    course_params = (owner_id,)
    course_data = read_query(course_query, course_params)

    if not course_data:
        return None

    courses_with_sections = []

    for course_row in course_data:
        course_id = course_row[0]
        section_query = """select * from sections where course_id = ?"""
        section_params = (course_id,)
        section_data = read_query(section_query, section_params)

        if not section_data:
            sections = []
        else:
            sections = [Section.from_query_result(*row) for row in section_data]

        course_with_sections = CourseWithSections(
            course_id=course_row[0],
            title=course_row[1],
            description=course_row[2],
            objectives=course_row[3],
            owner_id=course_row[-3],
            is_premium=bool(course_row[-2]),
            sections=sections
        )

        courses_with_sections.append(course_with_sections)

    return courses_with_sections


def get_teacher_course_by_id(user_id: int, course_id: int, order: str = "asc", title: str = None) -> CourseWithSections | NotFound:
    teacher = users_service.get_teacher_by_user_id(user_id)

    if not teacher:
        return NotFound(content="Teacher not found!")

    owner_id = teacher.teacher_id

    course_query = """SELECT * FROM courses WHERE owner_id = ? AND course_id = ?"""
    course_params = (owner_id, course_id)
    course_data = read_query(course_query, course_params)

    if not course_data:
        return NotFound(content=f"Course with ID {course_id} not found!")

    course_row = course_data[0]
    sections = []

    section_query = """SELECT * FROM sections WHERE course_id = ?"""

    if title:
        section_query += """ AND title LIKE ?"""
        section_params = (course_id, f"%{title}%")
    else:
        section_params = (course_id,)

    section_query += """ ORDER BY section_id"""
    if order.lower() == "desc":
        section_query += """ DESC"""

    section_data = read_query(section_query, section_params)

    if section_data:
        sections = [Section.from_query_result(*row) for row in section_data]

    course_with_sections = CourseWithSections(
        course_id=course_row[0],
        title=course_row[1],
        description=course_row[2],
        objectives=course_row[3],
        owner_id=course_row[-3],
        is_premium=bool(course_row[-2]),
        sections=sections
    )

    return course_with_sections


def get_student_course_by_id(student_id: int, course_id: int, order: str = "asc", title: str = None) ->\
        CourseWithSections | NotFound:
    course_query = """select * from courses where course_id = ?"""
    course_params = (course_id,)
    course_data = read_query(course_query, course_params)

    if not course_data:
        return NotFound(content=f"Course with ID {course_id} not found!")

    course_row = course_data[0]
    is_premium = bool(course_row[-2])

    if is_premium:
        enrollment_query = """select * from enrollments where courses_course_id = ? and students_student_id = ?"""
        enrollment_params = (course_id, student_id)
        enrollment_data = read_query(enrollment_query, enrollment_params)

        if not enrollment_data:
            return NotFound(content="Access denied. This is a premium course and the student is not enrolled.")

    section_query = """select * from sections where course_id = ?"""

    if title:
        section_query += """ and title like ?"""
        section_params = (course_id, f"%{title}%")
    else:
        section_params = (course_id,)

    section_query += """ order by section_id"""
    if order.lower() == "desc":
        section_query += """ desc"""

    section_data = read_query(section_query, section_params)

    sections = [Section.from_query_result(*row) for row in section_data] if section_data else []

    course_with_sections = CourseWithSections(
        course_id=course_row[0],
        title=course_row[1],
        description=course_row[2],
        objectives=course_row[3],
        owner_id=course_row[-3],
        is_premium=is_premium,
        sections=sections
    )

    return course_with_sections


def get_course_by_id_simpler(course_id) -> Course | NotFound:
    course_query = """select * from courses where course_id = ?"""
    course_params = (course_id,)
    course_data = read_query(course_query, course_params)

    if not course_data:
        return NotFound(content=f"Course with ID {course_id} not found!")

    course_row = course_data[0]

    return Course(course_id=course_row[0],
                  title=course_row[1],
                  description=course_row[2],
                  objectives=course_row[3],
                  owner_id=course_row[-3],
                  is_premium=bool(course_row[-2]),
                  rating=course_row[-1]
                  )


def get_all_student_courses(student_id: int) -> list[Course] | NotFound | None:
    enrolled_query = """
    select c.course_id, c.title, c.description, c.objectives, c.owner_id, c.is_premium, c.rating
    from courses c
    join enrollments e on c.course_id = e.courses_course_id
    where e.students_student_id = ?
    """
    enrolled_params = (student_id,)
    enrolled_data = read_query(enrolled_query, enrolled_params)

    non_premium_query = """
    select c.course_id, c.title, c.description, c.objectives, c.owner_id, c.is_premium, c.rating
    from courses c
    where c.is_premium = 0
    and not exists (
        select 1
        from enrollments e
        where e.courses_course_id = c.course_id
        and e.students_student_id = ?
    )
    """
    non_premium_params = (student_id,)
    non_premium_data = read_query(non_premium_query, non_premium_params)

    courses = []

    if enrolled_data:
        courses.extend([Course.from_query_result(*row) for row in enrolled_data])

    if non_premium_data:
        courses.extend([Course.from_query_result(*row) for row in non_premium_data])

    if not courses:
        return NotFound(content="Student is not enrolled in any courses yet!")

    return courses


def get_non_premium_courses() -> list[CourseWithSections] | NotFound:
    query = """
    SELECT c.course_id, c.title, c.description, c.objectives, c.owner_id, c.is_premium,
           s.section_id, s.title, s.content, s.description, s.external_resource
    FROM courses c
    JOIN sections s ON c.course_id = s.course_id
    WHERE c.is_premium = 0
    """
    data = read_query(query)

    if not data:
        return NotFound(content="No courses and sections found!")

    courses_with_sections = []
    for row in data:
        # Check if this is a new course
        if not courses_with_sections or courses_with_sections[-1].course_id != row[0]:
            # Create a new course
            current_course = CourseWithSections(
                course_id=row[0],
                title=row[1],
                description=row[2],
                objectives=row[3],
                owner_id=row[4],
                is_premium=bool(row[5]),
                sections=[]
            )
            courses_with_sections.append(current_course)

        # Add section to the current course
        section = Section(
            section_id=row[6],
            title=row[7],
            content=row[8],
            description=row[9],
            external_resource=row[10]
        )
        current_course.sections.append(section)

    return courses_with_sections


def create_course(user_id: int, data: CreateCourse) -> Course | None | NotFound:
    teacher = users_service.get_teacher_by_user_id(user_id)
    if not teacher:
        return NotFound(content="Teacher not found!")

    owner_id = teacher.teacher_id

    try:
        course_id = insert_query(
            """insert into courses (title, description, objectives, owner_id, is_premium) values (?, ?, ?, ?, ?)""",
            (data.title, data.description, data.objectives, owner_id, data.is_premium)
        )
        if course_id:
            return Course(course_id=course_id, title=data.title, description=data.description,
                          objectives=data.objectives, owner_id=owner_id, is_premium=data.is_premium)
        return None
    except IntegrityError:
        return None


def update_course(course_id: int, data: UpdateCourse, user_id: int) -> Course | NotFound | None:
    teacher = users_service.get_teacher_by_user_id(user_id)
    if not teacher:
        return NotFound(content="Teacher not found!")

    course = get_teacher_course_by_id(teacher.users_user_id, course_id)

    if not course:
        return NotFound(content=f"Course with ID {course_id} not found.")

    try:
        update_query(
            """UPDATE courses SET title = ?, description = ?, objectives = ?, is_premium = ?
             WHERE course_id = ? AND owner_id = ?""",
            (data.title, data.description, data.objectives, data.is_premium, course_id, teacher.teacher_id)
        )

        updated_course = get_teacher_course_by_id(user_id, course_id)
        return updated_course
    except IntegrityError:
        return None


def delete_course_if_no_enrollments(teacher_id: int, course_id: int) -> dict | NotFound | Forbidden:
    course_query = """select * from courses where course_id = ? and owner_id = ?"""
    course_params = (course_id, teacher_id)
    course_data = read_query(course_query, course_params)

    if not course_data:
        return NotFound(content=f"Course with ID {course_id} not found or you do not own this course!")

    enrollments_query = """select * from enrollments where courses_course_id = ?"""
    enrollments_params = (course_id,)
    enrollments_data = read_query(enrollments_query, enrollments_params)

    if enrollments_data:
        return Forbidden(content=f"Cannot delete course with ID {course_id} because students are enrolled in it!")

    delete_course_query = """delete from courses where course_id = ?"""
    delete_course_params = (course_id,)
    delete_query(delete_course_query, delete_course_params)

    return {"message": "Course deleted successfully"}


def is_course_deleted(course_id: int) -> bool:
    course_query = """select * from courses where course_id = ?"""
    course_params = (course_id,)
    course_data = read_query(course_query, course_params)

    return not course_data
