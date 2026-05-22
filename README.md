# Job Application Tracker API

A Django REST Framework project built to manage job applications through a clean REST API.

The API supports:

- creating, listing, retrieving, updating, and deleting job applications
- filtering applications by status
- viewing summary counts grouped by status
- generating a professional follow-up email draft using the OpenAI Chat Completions API

## Project Overview

This project was implemented to match the below requirements:

- `JobApplication` model with `company`, `role`, `status`, `applied_date`, and `notes`
- CRUD endpoints for job applications
- optional filtering with `?status=...`
- summary endpoint at `/api/applications/summary/`
- AI endpoint at `/api/applications/<id>/generate-followup/`
- automated tests for create, filter, and summary
- clear setup and endpoint usage instructions

## Tech Stack

- Python
- Django
- Django REST Framework
- OpenAI Python SDK
- SQLite

## Project Structure

```text
job-application-tracker/
├── applications/
├── config/
├── manage.py
├── requirements.txt
├── README.md
└── .env
```

## Data Model

The `JobApplication` model contains:

- `company`: required string
- `role`: required string
- `status`: one of `applied`, `interviewing`, `rejected`, `offered`
- `applied_date`: auto-created `DateTimeField`
- `notes`: optional text field

Default status is `applied`.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/rohithsukka/job-application-tracker-api
cd job-application-tracker
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create the environment file

Create a `.env` file in the project root with:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-5.4-mini
```

If you only want to demonstrate the project structure for review, a placeholder key is acceptable. The AI endpoint will return a clear error unless a valid key is configured.

### 6. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Run the development server on port 8001

```bash
python manage.py runserver 8001
```

Base URL:

```text
http://127.0.0.1:8001/
```

## API Endpoints

### 1. Create a Job Application

**POST** `/api/applications/`

Example request:

```bash
curl -X POST http://127.0.0.1:8001/api/applications/ \
  -H "Content-Type: application/json" \
  -d "{\"company\":\"Google\",\"role\":\"Backend Engineer\",\"status\":\"applied\",\"notes\":\"Applied through careers portal\"}"
```

Example response:

```json
{
  "id": 1,
  "company": "Google",
  "role": "Backend Engineer",
  "status": "applied",
  "applied_date": "2026-05-23T12:00:00Z",
  "notes": "Applied through careers portal"
}
```

### 2. List All Applications

**GET** `/api/applications/`

```bash
curl http://127.0.0.1:8001/api/applications/
```

### 3. Filter Applications by Status

**GET** `/api/applications/?status=applied`

```bash
curl "http://127.0.0.1:8001/api/applications/?status=applied"
```

### 4. Retrieve an Application by ID

**GET** `/api/applications/<id>/`

```bash
curl http://127.0.0.1:8001/api/applications/1/
```

### 5. Update an Application Status

**PATCH** `/api/applications/<id>/`

Example request:

```bash
curl -X PATCH http://127.0.0.1:8001/api/applications/1/ \
  -H "Content-Type: application/json" \
  -d "{\"status\":\"interviewing\"}"
```

### 6. Delete an Application

**DELETE** `/api/applications/<id>/`

```bash
curl -X DELETE http://127.0.0.1:8001/api/applications/1/
```

### 7. Summary Endpoint

**GET** `/api/applications/summary/`

This returns counts grouped by status.

```bash
curl http://127.0.0.1:8001/api/applications/summary/
```

Example response:

```json
{
  "applied": 2,
  "interviewing": 1,
  "rejected": 0,
  "offered": 1
}
```

### 8. Generate Follow-Up Email

**POST** `/api/applications/<id>/generate-followup/`

This endpoint uses the OpenAI Chat Completions API to generate a concise, professional follow-up email draft based on the selected application.

```bash
curl -X POST http://127.0.0.1:8001/api/applications/1/generate-followup/
```

Example response:

```json
{
  "application_id": 1,
  "followup_email": "Dear Hiring Team,\n\nI hope you are doing well. I wanted to follow up on my application for the Backend Engineer role at Google and ask whether there are any updates regarding the hiring process.\n\nThank you for your time and consideration.\n\nBest regards,\n[Your Name]"
}
```

## API Testing Order

For manual testing, use this order so later requests have data to work with:

1. Create an application
2. List applications
3. Filter by status
4. Retrieve by ID
5. Update status
6. Check summary
7. Generate follow-up email
8. Delete an application

## Running Automated Tests

The project includes the minimum required tests from the assignment:

- create an application
- filter applications by status
- verify the summary endpoint response structure

Run all tests with:

```bash
python manage.py test
```

## Error Handling

The API handles common failure scenarios such as:

- invalid application IDs
- invalid status values
- missing OpenAI API key
- OpenAI API failures
- empty AI responses

## Notes

- SQLite is used as the default database for simplicity.
- OpenAI credentials are loaded from environment variables.
- The development server for this project should be started on port `8001`.
