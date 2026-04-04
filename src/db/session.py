from sqlalchemy.orm import sessionmaker
from src.db.engine import engine

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()