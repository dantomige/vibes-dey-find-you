from src.db.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float


class AudioFeaturesModel(Base):

    __tablename__ = "audio_features"

    song_id = Column(String, ForeignKey("songs.id"), primary_key=True)
    danceability = Column(Float, nullable=True)
    energy = Column(Float, nullable=True)
    key = Column(Integer, nullable=True)
    loudness = Column(Float, nullable=True)
    mode = Column(Integer, nullable=True)
    speechiness = Column(Float, nullable=True)
    acousticness = Column(Float, nullable=True)
    instrumentalness = Column(Float, nullable=True)
    liveness = Column(Float, nullable=True)
    valence = Column(Float, nullable=True)
    tempo = Column(Float, nullable=True)