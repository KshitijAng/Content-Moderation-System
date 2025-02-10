from dotenv import load_dotenv
from database import SessionLocal, engine, Base, ModerationResult
from celery_worker import moderate_text_task
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid
import os

load_dotenv()
# Load OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TextModerationRequest(BaseModel):
    text: str

class ModerationResponse(BaseModel):
    id: str
    flagged: bool
    categories: dict
    category_scores: dict

@app.post("/api/v1/moderate/text", response_model=ModerationResponse)
def moderate_text(request: TextModerationRequest, db: Session = Depends(get_db)):
    if not request.text.strip():  # Reject empty strings after stripping spaces
        raise HTTPException(status_code=400, detail="Text input cannot be empty.")
    
    if request.text.isdigit():  # Reject inputs that are only numbers
        raise HTTPException(status_code=400, detail="Text input cannot be only numbers.")

    moderation_id = str(uuid.uuid4())

    moderation_result = ModerationResult(
        id=moderation_id,
        text=request.text, 
        flagged=False, 
        categories={},
        category_scores={}
    )
    db.add(moderation_result)
    db.commit()

    moderate_text_task.apply_async(args=[moderation_id, request.text])
    
    return moderation_result

@app.get("/api/v1/task/{task_id}")
def get_task_result(task_id: str, db: Session = Depends(get_db)):
    moderation_result = db.query(ModerationResult).filter(ModerationResult.id == task_id).first()
    
    if not moderation_result:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if moderation_result.categories: 
        return {
            "status": "Completed",
            "result": {
                "flagged": moderation_result.flagged,
                "categories": moderation_result.categories,
                "category_scores": moderation_result.category_scores
            }
        }
    
    return {"status": "Processing"}


@app.get("/api/v1/stats")
def get_moderation_stats(db: Session = Depends(get_db)):
    total_requests = db.query(ModerationResult).count()
    flagged_count = db.query(ModerationResult).filter(ModerationResult.flagged == True).count()
    return {"total_requests": total_requests, "flagged_count": flagged_count}
