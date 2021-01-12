# Student Management System (still in development)
This is a Simple Student Management System E-Portal Project created for Educational Purpose using Python (Django).

Feel free to make changes. And if you love the project, do ADD a STAR ⭐️.

## Features of this Project

### A. Admin Users:
1. View Overall Summary Charts of Students Performance, Courses etc.
2. Manage Newsfeed (Add, Update and Delete)
3. Manage Staffs (Add, Update and Delete)
4. Manage Students (Add, Update and Delete)
5. Manage Course (Add, Update and Delete)
6. Manage Sessions/Semester (Add, Update and Delete)
7. Manage Library (Add, Update and Delete)

### B. Staff:
1. Take/Update Students Attendance
2. Add/Update Scoresheet
3. View Newsfeed etc.

### C. Students:
1. View Attendance
2. View Result
3. View Newsfeed
4. View Records
5. etc.


## Installation/Running

### Pre-Requisites:
1. Install Git Version Control
[ https://git-scm.com/ ]

2. Install Python Latest Version
[ https://www.python.org/downloads/ ]

3. Install Pip (Package Manager)
[ https://pip.pypa.io/en/stable/installing/ ]

*Homebrew can also be used as an alternative to pip*

### Installation
**1. Create a Virtual Environment and Activate**

Install Virtual Environment
```
$  pip install virtualenv
```

Create Virtual Environment

```
$  virtualenv venv
```

Activate Virtual Environment

For Windows
```
$  cd venv/scripts&&activate
```

For Mac/Linux
```
$  source venv/bin/activate
```

**2. Navigate to the project's base directory**

**3. Install Requirements from 'requirements.txt'**
```python
$  pip install -r requirements.txt
```


**4. Run Server**

```python
$ python manage.py runserver
```
Server will run on `http://127.0.0.1:8000/`

### Login Credentials

*For Superuser/Admin*

Create Super User `$  python manage.py createsuperuser`, enter username, gmail and password. 

To access the django admin panel, add a trailing url - `/administration/` i.e. `http://127.0.0.1:8000/administration/`

*To Login as a student/staff member*

* Navigate to "Add new user" tab and create a new user.
* Logout and Login with the user information you just created.

