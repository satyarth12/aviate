# ATS (Applicant Tracking System)
A Django REST Framework application that helps recruiters track job applications.

## Project Overview
This Applicant Tracking System (ATS) allows recruiters to manage candidate information through a RESTful API. The system provides endpoints to create, update, delete, and search candidates based on their names.

### Key Features
- CRUD Operations: Create, read, update, and delete candidate records
- Relevancy-Based Search: Search candidates by name with results sorted by relevancy
- API Documentation: Swagger UI for interactive API exploration and testing

### Technology Stack
- Python 3.11+
- Django & Django REST Framework: Backend web framework
- Poetry: Dependency management
- drf-spectacular: OpenAPI/Swagger documentation
  
### Installation
#### Prerequisites
- Python 3.11 or higher
- Poetry

#### Setup Instructions
1. Clone the repository:
```bash
git clone https://github.com/satyarth12/aviate.git
cd aviate
```
2. Install dependencies using Poetry:
```bash
poetry install
```
3. Activate the Poetry environment:
```bash
poetry shell
```
4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Start the development server:
```bash
python manage.py runserver
```
6. Access the application:
- API: http://127.0.0.1:8000/api/
- Swagger UI: http://127.0.0.1:8000/api/schema/swagger-ui/
- Admin interface: http://127.0.0.1:8000/admin/

## Project Structure

```
django-ats/
├── ats_system/            # Main Django project
│   ├── __init__.py
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── candidates/            # Candidates app
│   ├── __init__.py
│   ├── admin.py           # Admin configuration
│   ├── apps.py
│   ├── models.py          # Candidate model
│   ├── serializers.py     # API serializers
│   ├── tests.py           # Test cases
│   ├── urls.py            # API URL configuration
│   └── views.py           # API views and search 
├── manage.py              # Django management script
├── pyproject.toml         # Poetry configuration
├── poetry.lock            # Poetry dependencies lock 
└── README.md              # This file
```

## API Endpoints

### Candidate Management

| Method | Endpoint                            | Description                      |
| ------ | ----------------------------------- | -------------------------------- |
| GET    | `/api/candidates/`                  | List all candidates              |
| POST   | `/api/candidates/`                  | Create a new candidate           |
| GET    | `/api/candidates/{id}/`             | Retrieve a specific candidate    |
| PUT    | `/api/candidates/{id}/`             | Update a candidate (full update) |
| PATCH  | `/api/candidates/{id}/`             | Partial update a candidate       |
| DELETE | `/api/candidates/{id}/`             | Delete a candidate               |
| GET    | `/api/candidates/search/?q=<query>` | Search candidates by name        |

### Candidate Model

The `Candidate` model includes the following fields:

- `name`: Candidate's full name
- `age`: Candidate's age (positive integer)
- `gender`: One of 'M' (Male), 'F' (Female), or 'O' (Other)
- `email`: Candidate's email address (unique)
- `phone_number`: Candidate's phone number

### Search Functionality

The search feature allows finding candidates based on their names. Results are sorted by relevancy, which is defined by the number of words in the search query that match in the candidate's name.

#### Example:

If the search query is "Ajay Kumar Yadav", the order of results will be:
1. "Ajay Kumar Yadav" (3 matching words)
2. "Ajay Kumar" (2 matching words)
3. "Ajay Yadav" (2 matching words)
4. "Kumar Yadav" (2 matching words)
5. "Ramesh Yadav" (1 matching word)
6. "Ajay Singh" (1 matching word)

#### Search API Usage:

```
GET /api/candidates/search/?q=Ajay Kumar
```

## Request/Response Examples

### Create a Candidate

**Request:**
```http
POST /api/candidates/
Content-Type: application/json

{
  "name": "Ajay Kumar Yadav",
  "age": 30,
  "gender": "M",
  "email": "ajay.kumar@example.com",
  "phone_number": "+91 9876543210"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Ajay Kumar Yadav",
  "age": 30,
  "gender": "M",
  "email": "ajay.kumar@example.com",
  "phone_number": "+91 9876543210"
}
```

### Search Candidates

**Request:**
```http
GET /api/candidates/search/?q=Kumar Yadav
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Ajay Kumar Yadav",
    "age": 30,
    "gender": "M",
    "email": "ajay.kumar@example.com",
    "phone_number": "+91 9876543210"
  },
  {
    "id": 3,
    "name": "Kumar Singh",
    "age": 28,
    "gender": "M",
    "email": "kumar.singh@example.com",
    "phone_number": "+91 9876543212"
  },
  {
    "id": 5,
    "name": "Priya Yadav",
    "age": 27,
    "gender": "F",
    "email": "priya.yadav@example.com",
    "phone_number": "+91 9876543214"
  }
]
```

## Development

### Creating a Superuser

To access the admin interface, create a superuser:

```bash
python manage.py createsuperuser
```