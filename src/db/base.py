from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Table, Column, ForeignKey, Integer, String

Base = declarative_base()

song_artists = Table(
    "song_artists",
    Base.metadata,
    Column("song_id", ForeignKey("songs.id"), primary_key=True),
    Column("song_id", ForeignKey("artists.id"), primary_key=True)
)

class Song(Base):

    __tablename__ = "songs"

    id = Column(String, primary_key=True)
    mbid = Column(String, nullable=False)
    title = Column(String, nullable=False)
    artists = relationship("Artist", secondary=song_artists)
    duration = Column(Integer, nullable=True)
    isrc = Column(String, nullable=True)

class Artist(Base):

    __tablename__ = "artists"

    id = Column(String, primary_key=True)
    arid = Column(String, nullable=False)
    name = Column(String, nullable=False)