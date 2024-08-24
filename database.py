from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
  __tablename__ = "users"
  user_id = Column(Integer, primary_key=True, index=True)
  survey_id = Column(Integer)

class Survey(Base):
  __tablename__ = "surveys"
  id = Column(Integer, primary_key=True, index=True)
  survey_id = Column(Integer, index=True)
  question_id = Column(Integer, index=True)
  question = Column(String)

class Response(Base):
  __tablename__ = "responses"
  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, index=True)
  survey_id = Column(Integer, index=True)
  question_id = Column(Integer, index=True)
  response = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
  db = SessionLocal()
  try:
      yield db
  finally:
      db.close()

def create_user(db: Session, user_id: int, survey_id: int):
  db_user = User(user_id=user_id, survey_id=survey_id)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

def create_survey(db: Session, survey_id: int, question_id: int, question: str):
  db_survey = Survey(survey_id=survey_id, question_id=question_id, question=question)
  db.add(db_survey)
  db.commit()
  db.refresh(db_survey)
  return db_survey

def create_response(db: Session, user_id: int, survey_id: int, question_id: int, response: str):
  db_response = Response(user_id=user_id, survey_id=survey_id, question_id=question_id, response=response)
  db.add(db_response)
  db.commit()
  db.refresh(db_response)
  return db_response

def get_users(db: Session, skip: int = 0, limit: int = 100):
  return db.query(User).offset(skip).limit(limit).all()

def get_surveys(db: Session, skip: int = 0, limit: int = 100):
  return db.query(Survey).offset(skip).limit(limit).all()

def get_responses(db: Session, skip: int = 0, limit: int = 100):
  return db.query(Response).offset(skip).limit(limit).all()

def get_survey_by_id(db: Session, survey_id: int):
  return db.query(Survey).filter(Survey.survey_id == survey_id).all()

def get_responses_by_survey_id(db: Session, survey_id: int):
  return db.query(Response).filter(Response.survey_id == survey_id).all()

def get_response_count_by_survey_id(db: Session, survey_id: int):
  return db.query(Response).filter(Response.survey_id == survey_id).count()