# db.py
import os
from sqlalchemy import create_engine, Column, String, Text, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True, index=True)
    status = Column(String, index=True)
    input = Column(JSON)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class Song(Base):
    __tablename__ = "songs"
    id = Column(String, primary_key=True, index=True)
    job_id = Column(String)
    title = Column(String)
    poem_title = Column(String)
    poem_text = Column(Text)
    lyrics = Column(Text)
    audio_url = Column(String, nullable=True)
    midi_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

def init_db():
    Base.metadata.create_all(bind=engine)