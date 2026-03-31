from sqlalchemy.orm import sessionmaker
from src.db.engine import engine

SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()