# Job Board API

A REST API for a job board platform where companies can post job listings and job seekers can apply with resume uploads. Built with Django and Django REST Framework.

## Features

- User authentication with token-based login (job seekers and companies)
- Full CRUD for job listings, restricted to the company that posted them
- Job applications with resume upload (PDF/DOC/DOCX, max 5MB)
- Application status tracking (pending, reviewed, shortlisted, rejected)
- Search and filter job listings by location, job type, and keyword
- Pagination on all list endpoints

## Tech Stack

- Python 3
- Django
- Django REST Framework
- PostgreSQL
- Token Authentication

## Setup Instructions

1. Clone the repository

git clone https://github.com/fredrickmwendwa/job-board-api.git
cd job-board-api


2. Create and activate a virtual environment

python -m venv venv
venv\Scripts\activate


3. Install dependencies

pip install -r requirements.txt


4. Create a PostgreSQL database called `jobboard_db`

5. Create a `.env` file in the project root with the following variables

SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=jobboard_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1,localhost


6. Run migrations

python manage.py migrate


7. Create a superuser (optional, for admin access)

python manage.py createsuperuser


8. Run the server

python manage.py runserver


## API Endpoints

### Accounts
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/accounts/register/ | Register a new user |
| POST | /api/accounts/login/ | Log in and receive a token |
| POST | /api/accounts/logout/ | Log out (requires token) |
| GET/PUT | /api/accounts/profile/ | View or update your profile |

### Jobs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/jobs/ | List all active jobs (supports ?location=, ?job_type=, ?search=) |
| POST | /api/jobs/ | Create a job (company accounts only) |
| GET | /api/jobs/<id>/ | View a single job |
| PUT | /api/jobs/<id>/ | Update a job (owner only) |
| DELETE | /api/jobs/<id>/ | Delete a job (owner only) |
| GET | /api/jobs/my-jobs/ | View jobs you've posted (company only) |

### Applications
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/applications/apply/<job_id>/ | Apply to a job with a resume |
| GET | /api/applications/my-applications/ | View your submitted applications |
| GET | /api/applications/job/<job_id>/ | View applications for your job (company only) |
| GET | /api/applications/<id>/ | View a single application |
| DELETE | /api/applications/<id>/ | Withdraw an application (applicant only) |
| PUT | /api/applications/<id>/status/ | Update application status (company only) |

## Running Tests

python manage.py test

