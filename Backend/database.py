from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean,text, create_engine
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost:5432/sentivue-task'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# class Post(Base):
#     __tablename__ = "posts"

#     id = Column(Integer,primary_key=True,nullable=False)
#     title = Column(String,nullable=False)
#     content = Column(String,nullable=False)
#     published = Column(Boolean, server_default='TRUE')
#     created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

class Transcripts(Base):
    __tablename__ = "Transcripts"

    id = Column(UUID(as_uuid=True),primary_key=True,nullable=False)
    fileName = Column(String, nullable=False)
    Transcript = Column(String, nullable=False)