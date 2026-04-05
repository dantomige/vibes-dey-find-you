from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Table, Column, ForeignKey, Integer, String

Base = declarative_base()

song_artists_table = Table(
    "song_artists",
    Base.metadata,
    Column("song_id", ForeignKey("songs.id"), primary_key=True),
    Column("artist_id", ForeignKey("artists.id"), primary_key=True),
)


class SongModel(Base):

    __tablename__ = "songs"

    id = Column(String, primary_key=True)
    mbid = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=True)
    isrc = Column(String, nullable=True)

    artists = relationship("ArtistModel", secondary=song_artists_table)


class ArtistModel(Base):

    __tablename__ = "artists"

    id = Column(String, primary_key=True)
    arid = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)

    songs = relationship(
        "SongModel", secondary=song_artists_table, back_populates="artists"
    )
