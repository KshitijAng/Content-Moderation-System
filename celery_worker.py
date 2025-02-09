import openai
from celery import Celery
import os
from database import SessionLocal, ModerationResult  
from dotenv import load_dotenv
load_dotenv()

# Load OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

REDIS_URL = os.getenv("REDIS_URL")

celery = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery.task(bind=True, autoretry_for=(openai.error.OpenAIError,), retry_backoff=True, retry_jitter=True, max_retries=5)
def moderate_text_task(self, task_id: str, text: str): 
    response = openai.Moderation.create(
        input=text,
        api_key=OPENAI_API_KEY
    )
    
    moderation_data = response["results"][0]
    
    db = SessionLocal()
    moderation_result = db.query(ModerationResult).filter(ModerationResult.id == task_id).first()
    
    if moderation_result:
        moderation_result.flagged = moderation_data["flagged"]
        moderation_result.categories = moderation_data["categories"]
        moderation_result.category_scores = moderation_data["category_scores"]
        db.commit()
        db.refresh(moderation_result)
    
    db.close()
    return {
        "flagged": moderation_data["flagged"],
        "categories": moderation_data["categories"],
        "category_scores": moderation_data["category_scores"]
    }
