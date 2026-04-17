import json
import pytest
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.base import Base

@pytest.fixture
def load_fixture():
    def _load(name):
        path = Path(__file__).parent / "fixtures" / name
        with open(path) as f:
            return json.load(f)
    return _load

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(engine)

    db = SessionLocal()

    yield db

    db.close()