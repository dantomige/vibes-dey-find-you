import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.base import Base
from src.db.crud import SongRepository
from src.schemas.song import Song
from src.schemas.artist import Artist
from src.schemas.date import Date

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(engine)

    db = SessionLocal()

    yield db

    db.close()


def test_add_songs(db_session):
    pass

def test_get_all_songs(db_session):
    pass

def test_update_songs(db_session):
    pass

def test_remove_song(db_session):
    pass