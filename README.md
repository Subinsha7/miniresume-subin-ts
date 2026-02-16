# Mini Resume Management API

## Python Version
Python 3.13.3

## Installation Steps

1. Clone the repository
   git clone https://github.com/Subinsha7/miniresume-subin-ts.git
   cd miniresume-subin-ts

2. Create virtual environment
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

## Run the Application

uvicorn main:app --reload

Application runs at:
http://127.0.0.1:8000

Swagger Docs:
http://127.0.0.1:8000/docs

## Health Check

GET /health

Response:
{
  "status": "healthy"
}

## Create Candidate

POST /candidates

Form Data:
- full_name
- dob (YYYY-MM-DD)
- contact_number
- contact_address
- education_qualification
- graduation_year
- years_of_experience
- skill_set (comma separated)
- resume (PDF/DOC/DOCX)
