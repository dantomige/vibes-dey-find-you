import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.base import Base, SongModel, ArtistModel, song_artists_table
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

def normalize_artist(artist):
    return (artist.arid, artist.name)

def normalize_song(song):
    return (song.title, tuple(sorted(normalize_artist(artist) for artist in song.artists)))

def test_add_songs(db_session):
    db = db_session
    song_repo = SongRepository(db=db)

    j_hus = Artist(arid="n3n", name="J Hus")
    wizkid = Artist(arid="fda2", name="Wizkid")
    asake = Artist(arid="lw23", name="Asake")

    artists = [j_hus, wizkid, asake]

    songs = [
        Song(title="Alien Girl", artists=[j_hus]),
        Song(title="Turbulence", artists=[wizkid, asake]),
    ]

    # adding simple
    song_repo.add_songs(songs=songs)

    artists_in_db = db.query(ArtistModel).all()
    songs_in_db = db.query(SongModel).all()

    expected_artists_normalized = set(map(normalize_song, artists))
    expected_songs_normalized = set(map(normalize_song, songs))

    artists_normalized = set(map(normalize_song, artists_in_db))
    songs_normalized = set(map(normalize_song, songs_in_db))

    assert len(artists_in_db) == len(expected_artists_normalized)
    assert artists_normalized == expected_artists_normalized
    assert len(songs_in_db) == len(expected_songs_normalized)
    assert songs_normalized == expected_songs_normalized

    # adding repeat songs
    song_repo.add_songs(songs=songs)

    artists_in_db = db.query(ArtistModel).all()
    songs_in_db = db.query(SongModel).all()

    artists_normalized = set(map(normalize_song, artists_in_db))
    songs_normalized = set(map(normalize_song, songs_in_db))

    assert len(artists_in_db) == len(expected_artists_normalized)
    assert artists_normalized == expected_artists_normalized
    assert len(songs_in_db) == len(expected_songs_normalized)
    assert songs_normalized == expected_songs_normalized

    # adding repeat artists
    jogodo = Song(title="Jogodo", artists=[wizkid, asake])
    song_repo.add_songs(song=[jogodo])
    
    artists_in_db = db.query(ArtistModel).all()
    songs_in_db = db.query(SongModel).all()

    expected_artists_normalized = set(map(normalize_song, artists))
    expected_songs_normalized = set(map(normalize_song, songs + [jogodo]))

    artists_normalized = set(map(normalize_song, artists_in_db))
    songs_normalized = set(map(normalize_song, songs_in_db))

    assert len(artists_in_db) == len(expected_artists_normalized)
    assert artists_normalized == expected_artists_normalized
    assert len(songs_in_db) == len(expected_songs_normalized)
    assert songs_normalized == expected_songs_normalized

    # mix
    shallipopi = Artist(arid="g43f", name="Shallipopi")
    alaye = Song(title="Alaye", artists=[wizkid, asake])
    laho = Song(title="Laho", artists=[shallipopi])
    new_songs = [alaye, jogodo, laho]

    song_repo.add_songs(song=new_songs)
    
    artists_in_db = db.query(ArtistModel).all()
    songs_in_db = db.query(SongModel).all()

    expected_artists_normalized = set(map(normalize_song, artists + [shallipopi]))
    expected_songs_normalized = set(map(normalize_song, songs + new_songs))

    artists_normalized = set(map(normalize_song, artists_in_db))
    songs_normalized = set(map(normalize_song, songs_in_db))

    assert len(artists_in_db) == len(expected_artists_normalized)
    assert artists_normalized == expected_artists_normalized
    assert len(songs_in_db) == len(expected_songs_normalized)
    assert songs_normalized == expected_songs_normalized

def test_get_song(db_session):
    db = db_session
    song_repo = SongRepository(db=db)

    j_hus = Artist(arid="n3n", name="J Hus")
    wizkid = Artist(arid="fda2", name="Wizkid")
    asake = Artist(arid="lw23", name="Asake")

    alien_girl = Song(title="Alien Girl", artists=[j_hus])
    turbulence = Song(title="Turbulence", artists=[wizkid, asake])
    songs = [
        alien_girl,
        turbulence
    ]

    expected_alien_girl_normalized = normalize_song(alien_girl)
    expected_turbulence_normalized = normalize_song(turbulence)

    song_repo.add_songs(songs)
    result_alien_girl = song_repo.get_song(mbid=alien_girl.mbid)
    result_turbulence = song_repo.get_song(mbid=turbulence.mbid)

    assert normalize_song(result_alien_girl) == expected_alien_girl_normalized
    assert normalize_song(result_turbulence) == expected_turbulence_normalized

    # throws errors on id that doesn't exist
    with pytest.raises(Exception):
        _ = song_repo.get_song(mbid="random_id_not_in_repo")

def test_get_all_songs(db_session):
    db = db_session
    song_repo = SongRepository(db=db)

    j_hus = Artist(arid="n3n", name="J Hus")
    wizkid = Artist(arid="fda2", name="Wizkid")
    asake = Artist(arid="lw23", name="Asake")

    songs = [
        Song(title="Alien Girl", artists=[j_hus]),
        Song(title="Turbulence", artists=[wizkid, asake]),
    ]

    expected_songs_normalized = set(map(normalize_song, songs))
    
    all_songs = song_repo.get_all_songs()
    all_songs_normalized = set(map(normalize_song, all_songs))

    assert len(all_songs) == len(expected_songs_normalized)
    assert all_songs_normalized == expected_songs_normalized


def test_update_songs(db_session):
    db = db_session
    song_repo = SongRepository(db=db)

    j_hus = Artist(arid="n3n", name="J Hus")
    wizkid = Artist(arid="fda2", name="Wizkid")
    asake = Artist(arid="lw23", name="Asake")

    alien_girl = Song(title="Alien Girl", artists=[j_hus])
    turbulence = Song(title="Turbulence", artists=[wizkid, asake])

    songs = [
        alien_girl,
        turbulence
    ]

    song_repo.add_songs(songs)
    result = song_repo.get_song(mbid=alien_girl.mbid)
    assert normalize_song(result) == normalize_song(alien_girl)

    new_alien_girl = Song(title="Alien Girl", artists=[j_hus], duration=10000)
    song_repo.update_song(mbid=alien_girl.mbid, song=new_alien_girl)
    result = song_repo.get_song(mbid=alien_girl.mbid)

    assert song_repo.get_all_songs() == 2
    assert result.duration == 10000
    assert normalize_song(result) == normalize_song(new_alien_girl)
    

def test_remove_song(db_session):
    db = db_session
    song_repo = SongRepository(db=db)

    j_hus = Artist(arid="n3n", name="J Hus")
    wizkid = Artist(arid="fda2", name="Wizkid")
    asake = Artist(arid="lw23", name="Asake")

    alien_girl = Song(title="Alien Girl", artists=[j_hus])
    turbulence = Song(title="Turbulence", artists=[wizkid, asake])

    songs = [
        alien_girl,
        turbulence
    ]

    song_repo.add_songs(songs)
    song_repo.remove_song(mbid=alien_girl.mbid)

    with pytest.raises(Exception):
        _ = song_repo.get_song(song_repo.mbid)

    assert len(song_repo.get_all_songs()) == 1