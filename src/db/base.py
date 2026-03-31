from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Song(Base):

    __tablename__ = "songs"

    pass

class Artist(Base):

    __tablename__ = "artists"