from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from database import db, create_document
from schemas import ContactSubmission
import os

app = FastAPI(title="Go Go Sparkles API", version="1.0.0")

# CORS
frontend_url = os.getenv("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContactResponse(BaseModel):
    success: bool
    message: str


@app.get("/")
def root():
    return {"status": "ok", "service": "Go Go Sparkles API"}


@app.post("/contact", response_model=ContactResponse)
def submit_contact(payload: ContactSubmission):
    try:
        doc_id = create_document("contactsubmission", payload)
        return ContactResponse(success=True, message="Thanks! Our team will get back to you shortly.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_db():
    if db is None:
        return {"database": "unavailable"}
    try:
        # Ping by listing collections
        cols = db.list_collection_names()
        return {"database": "ok", "collections": cols}
    except Exception as e:
        return {"database": "error", "detail": str(e)}
