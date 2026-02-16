from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
import uuid

app = FastAPI()

# In-memory database
candidates_db = {}

# Allowed resume file types
ALLOWED_EXTENSIONS = ["pdf", "doc", "docx"]


class Candidate(BaseModel):
    id: str
    full_name: str = Field(..., min_length=2)
    dob: date
    contact_number: str = Field(..., min_length=10, max_length=15)
    contact_address: str
    education_qualification: str
    graduation_year: int = Field(..., ge=1950)
    years_of_experience: float = Field(..., ge=0)
    skill_set: List[str]



@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "healthy"}


@app.post("/candidates", status_code=status.HTTP_201_CREATED)
async def create_candidate(
    full_name: str = Form(...),
    dob: date = Form(...),
    contact_number: str = Form(...),
    contact_address: str = Form(...),
    education_qualification: str = Form(...),
    graduation_year: int = Form(...),
    years_of_experience: float = Form(...),
    skill_set: str = Form(...),  # comma separated
    resume: UploadFile = File(...)
):
    # Validate file type
    file_extension = resume.filename.split(".")[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    candidate_id = str(uuid.uuid4())

    candidate = Candidate(
        id=candidate_id,
        full_name=full_name,
        dob=dob,
        contact_number=contact_number,
        contact_address=contact_address,
        education_qualification=education_qualification,
        graduation_year=graduation_year,
        years_of_experience=years_of_experience,
        skill_set=[skill.strip() for skill in skill_set.split(",")]
    )

    candidates_db[candidate_id] = candidate

    return {
        "message": "Candidate created successfully",
        "id": candidate_id
    }
@app.get("/candidates")
def list_candidates(
    skill: Optional[str] = None,
    experience: Optional[float] = None,
    graduation_year: Optional[int] = None
):
    results = []

    for candidate in candidates_db.values():
        if skill and skill.lower() not in [s.lower() for s in candidate.skill_set]:
            continue

        if experience is not None and candidate.years_of_experience != experience:
            continue

        if graduation_year is not None and candidate.graduation_year != graduation_year:
            continue

        results.append(candidate)

    return results
@app.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: str):
    if candidate_id not in candidates_db:
        raise HTTPException(status_code=404, detail="Candidate not found")

    return candidates_db[candidate_id]
@app.delete("/candidates/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidate(candidate_id: str):
    if candidate_id not in candidates_db:
        raise HTTPException(status_code=404, detail="Candidate not found")

    del candidates_db[candidate_id]
    return
