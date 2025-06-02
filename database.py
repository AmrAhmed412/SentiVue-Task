from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean,text, create_engine
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Transcripts(Base):
    __tablename__ = "Transcripts"

    id = Column(UUID(as_uuid=True),primary_key=True,nullable=False)
    fileName = Column(String, nullable=False)
    Transcript = Column(String, nullable=False)