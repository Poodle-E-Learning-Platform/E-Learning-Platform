# E-Learning Platform

## Project Description

E-learning platform designed for students to search for and enroll in online courses, and for teachers to publish and manage courses. Functionality: Students view and access courses. Teachers create, update, and manage courses, sections, and student enrollments.

## Functionality

### Entities

#### Users
- Users can be teachers, students, or admins.
- Each user must have an email, first name, last name, and a password.
- The email serves as a username for both students and teachers and cannot be changed.
- Teachers should also have a phone number and LinkedIn account.
- Students can view available courses and access their content based on whether the courses are public or premium and/or they are subscribed.
- Teachers can create and update courses, and manage sections within those courses.

#### Courses
- Each course must have a unique title, description, objectives, owner (teacher), tags, and sections.
- Courses must be either public or premium and can be augmented with sections later.
- Courses should have options for subscribing or unsubscribing.
- Courses can have ratings based on student feedback.

#### Sections
- Each section must have a title, content, and an optional description and external resource link.
- Sections within a course should be sortable by ID or name.

### Public Part

The public part of the platform is accessible without authentication.
- Anonymous users can view the title, description, and tags of available public courses but cannot access the content.
- Anonymous users can search for courses by tag and/or rating.
- Anonymous users can register and login.

### Endpoints for Registered Users

Accessible only if the user is authenticated. Authenticated teachers or admins can access all courses and sections they own or manage.

#### For Students
- Students must be able to login/logout.
- Students can view and edit their account information (except the email).
- Students can access all public courses and the premium courses they are enrolled in.
- Students can track their progress in each course based on the sections they have visited.
- Students can view and search through existing public and premium courses by name and tag.
- Students can unsubscribe from premium courses.
- Students can rate a course only if they are enrolled in it.
- Students can subscribe to a maximum of 5 premium courses at a time and an unlimited number of public courses.

#### For Teachers
- Teachers can view and edit their account information (except the e-mail).
- Teachers can access all courses and sections they own.
- Teachers can create, view, and update their courses.
- Teachers can deactivate/hide courses they own if no students are subscribed.
- Teachers can generate reports for past and current students enrolled in their courses.

## Technologies Used
- FastAPI
- Python
- REST
- JWT
- JSON
- Uvicorn
- MariaDB
- MySQL

## Prerequisites
1. Install Python:
   - Download and install Python from the [official website](https://www.python.org/downloads/).
   - If you already have Python installed, go directly to the second point.
2. Install pip:
   - Ensure pip (Python package installer) is installed with Python. You can check by running `pip --version` in your terminal.
3. Install a virtual environment tool (optional but recommended):
   - You can use `venv` which is included with Python: `python -m venv env`
   - Or install `virtualenv` using pip: `pip install virtualenv`
4. Install MariaDB Server:
   - Download and install MariaDB from the [official website](https://mariadb.org/download/).
   - Follow the instructions for your operating system to complete the installation.
5. Install MySQL Workbench:
   - Download and install MySQL Workbench from the [official website](https://www.mysql.com/products/workbench/).
   - Use MySQL Workbench to manage your MariaDB server. Configure the connection details such as localhost and port as needed.
6. Run the SQL script from the repo in MySQL Workbench:
   - Open MySQL Workbench and connect to your MariaDB server.
   - Open the SQL script file from the cloned repository in MySQL Workbench.
   - Execute the script to create the database schema and tables.
7. Set the created schema as the default one in the DBMS:
   - Once connected to your MariaDB server in MySQL Workbench, set the newly created schema (e.g., `learning_platform`) as the default schema.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/forum-post-system.git

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Usage

1. Start the server:
   ```bash
   uvicorn main:app --reload

Access the API endpoints at http://localhost:8000/docs.

## Credits

- **Project Creators:** Kaloyan Nikolov, Veselin Totev.


