from sqlalchemy import create_engine, Column, String, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from dotenv import load_dotenv
import os

load_dotenv()

# Load OpenAI API Key
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session for interacting with DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define base class for models
Base = declarative_base()

database = Database(DATABASE_URL)

class ModerationResult(Base):
    __tablename__ = "moderation_results"

    id = Column(String, primary_key=True, index=True)
    text = Column(String, nullable=False)
    flagged = Column(Boolean, nullable=False)
    categories = Column(JSON, nullable=False)
    category_scores = Column(JSON, nullable=False)
