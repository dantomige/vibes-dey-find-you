import pytest

from unittest.mock import Mock

from src.db.base import Base
from src.db.tables.core import SongModel, ArtistModel, song_artists_table
from src.db.crud.core import SongRepository
from src.schemas.song import Song
from src.schemas.artist import Artist
from src.schemas.date import Date

### CHECK SONG ARTIST TABLE


def normalize_artist(artist):
    return (artist.name)


def normalize_song(song):
    return (
        song.title,
        tuple(sorted(normalize_artist(artist) for artist in song.artists)),
    )


def TestGetSongIdsByExternalId():

    def test_query_by_musicbrainz_only():
        db = Mock()
        query = db.query.return_value
        query.filter.return_value.first.return_value = SongModel(song_id="MB_ID")

        repo = SongRepository(db)

        result = repo.get_song_ids_by_external_id(
            music_brainz_id="MB456"
        )

        assert result == "MB_ID"
        assert query.filter.call_count == 1
        assert query.filter.call_args[0][0].compare(
            SongModel.music_brainz_id == "MB456"
        )

    def test_query_by_recco_beats_only():
        db = Mock()
        query = db.query.return_value
        query.filter.return_value.first.return_value = SongModel(song_id="RB_ID")

        repo = SongRepository(db)

        result = repo.get_song_ids_by_external_id(
            recco_beats_id="RB456"
        )

        assert result == "RB_ID"
        assert query.filter.call_count == 1
        assert query.filter.call_args[0][0].compare(
            SongModel.recco_beats_id == "RB456"
        )

    def test_query_by_isrc_only():
        db = Mock()
        query = db.query.return_value
        query.filter.return_value.first.return_value = SongModel(song_id="ISRC_ID")

        repo = SongRepository(db)

        result = repo.get_song_ids_by_external_id(
            isrc="ISRC456"
        )

        assert result == "ISRC_ID"
        assert query.filter.call_count == 1
        assert query.filter.call_args[0][0].compare(
            SongModel.isrc == "ISRC456"
        )

    def test_query_priority_order():
        db = Mock()
        query = db.query.return_value

        first_mock = Mock()
        first_mock.first.side_effect = [
            None,                          # musicbrainz fails
            SongModel(song_id="RB_ID")     # recco succeeds
        ]

        query.filter.return_value = first_mock

        repo = SongRepository(db)

        result = repo.get_song_ids_by_external_id(
            music_brainz_id="MB456",
            recco_beats_id="RB456"
        )

        assert result == "RB_ID"
        assert query.filter.call_count == 2

    def test_query_with_no_ids():
        db = Mock()
        repo = SongRepository(db)

        result = repo.get_song_ids_by_external_id()

        assert result is None
        assert db.query.call_count == 0


def test_add_songs(db_session):
    db = db_session
    song_repo = SongRepository(db=db)

    j_hus = Artist(name="J Hus")
    wizkid = Artist(name="Wizkid")
    asake = Artist(name="Asake")

    artists = [j_hus, wizkid, asake]

    songs = [
        Song(title="Alien Girl", artists=[j_hus]),
        Song(title="Turbulence", artists=[wizkid, asake]),
    ]

    # adding simple
    song_ids = song_repo.add_songs(songs=songs)

    artists_in_db = db.query(ArtistModel).all()
    songs_in_db = db.query(SongModel).all()

    expected_artists_normalized = set(map(normalize_song, artists))
    expected_songs_normalized = set(map(normalize_song, songs))
    expected_ids = set(song.id for song in songs_in_db)

    artists_normalized = set(map(normalize_song, artists_in_db))
    songs_normalized = set(map(normalize_song, songs_in_db))

    assert len(song_ids) == 2
    assert set(song_ids) == expected_ids
    assert len(artists_in_db) == len(expected_artists_normalized)
    assert artists_normalized == expected_artists_normalized
    assert len(songs_in_db) == len(expected_songs_normalized)
    assert songs_normalized == expected_songs_normalized

    # adding repeat songs
    song_ids = song_repo.add_songs(songs=songs)

    artists_in_db = db.query(ArtistModel).all()
    songs_in_db = db.query(SongModel).all()

    artists_normalized = set(map(normalize_song, artists_in_db))
    songs_normalized = set(map(normalize_song, songs_in_db))

    assert len(song_ids) == 2
    assert set(song_ids) == expected_ids
    assert len(artists_in_db) == len(expected_artists_normalized)
    assert artists_normalized == expected_artists_normalized
    assert len(songs_in_db) == len(expected_songs_normalized)
    assert songs_normalized == expected_songs_normalized

    # adding repeat artists
    jogodo = Song(title="Jogodo", artists=[wizkid, asake])
    song_ids = song_repo.add_songs(song=[jogodo])

    artists_in_db = db.query(ArtistModel).all()
    songs_in_db = db.query(SongModel).all()

    expected_artists_normalized = set(map(normalize_song, artists))
    expected_songs_normalized = set(map(normalize_song, songs + [jogodo]))
    expected_ids = set(song.id for song in songs_in_db)

    artists_normalized = set(map(normalize_song, artists_in_db))
    songs_normalized = set(map(normalize_song, songs_in_db))

    assert len(song_ids) == 2
    assert set(song_ids) == expected_ids
    assert len(artists_in_db) == len(expected_artists_normalized)
    assert artists_normalized == expected_artists_normalized
    assert len(songs_in_db) == len(expected_songs_normalized)
    assert songs_normalized == expected_songs_normalized

    # mix
    shallipopi = Artist("g43f", name="Shallipopi")
    alaye = Song(title="Alaye", artists=[wizkid, asake])
    laho = Song(title="Laho", artists=[shallipopi])
    new_songs = [alaye, jogodo, laho]

    song_ids = song_repo.add_songs(song=new_songs)

    artists_in_db = db.query(ArtistModel).all()
    songs_in_db = db.query(SongModel).all()

    expected_artists_normalized = set(map(normalize_song, artists + [shallipopi]))
    expected_songs_normalized = set(map(normalize_song, songs + new_songs))
    expected_ids = set(song.id for song in songs_in_db)

    artists_normalized = set(map(normalize_song, artists_in_db))
    songs_normalized = set(map(normalize_song, songs_in_db))

    assert len(song_ids) == 2
    assert set(song_ids) == expected_ids
    assert len(artists_in_db) == len(expected_artists_normalized)
    assert artists_normalized == expected_artists_normalized
    assert len(songs_in_db) == len(expected_songs_normalized)
    assert songs_normalized == expected_songs_normalized


def test_get_song(db_session):
    db = db_session
    song_repo = SongRepository(db=db)

    j_hus = Artist(name="J Hus")
    wizkid = Artist(name="Wizkid")
    asake = Artist(name="Asake")

    alien_girl = Song(title="Alien Girl", artists=[j_hus])
    turbulence = Song(title="Turbulence", artists=[wizkid, asake])
    songs = [alien_girl, turbulence]

    expected_alien_girl_normalized = normalize_song(alien_girl)
    expected_turbulence_normalized = normalize_song(turbulence)

    song_ids = song_repo.add_songs(songs)
    result_alien_girl = song_repo.get_song(song_id=song_ids[0])
    result_turbulence = song_repo.get_song(song_id=song_ids[1])

    assert normalize_song(result_alien_girl) == expected_alien_girl_normalized
    assert normalize_song(result_turbulence) == expected_turbulence_normalized

    result_invalid = song_repo.get_song(song_id="random_id_not_in_repo")

    assert result_invalid is None


def test_get_all_songs(db_session):
    db = db_session
    song_repo = SongRepository(db=db)

    j_hus = Artist(name="J Hus")
    wizkid = Artist(name="Wizkid")
    asake = Artist(name="Asake")

    songs = [
        Song(title="Alien Girl", artists=[j_hus]),
        Song(title="Turbulence", artists=[wizkid, asake]),
    ]

    expected_songs_normalized = set(map(normalize_song, songs))

    song_repo.add_songs(songs)
    all_songs = song_repo.get_all_songs()
    all_songs_normalized = set(map(normalize_song, all_songs))

    assert len(all_songs) == len(expected_songs_normalized)
    assert all_songs_normalized == expected_songs_normalized


def test_update_songs(db_session):
    db = db_session
    song_repo = SongRepository(db=db)

    j_hus = Artist(name="J Hus")
    wizkid = Artist(name="Wizkid")
    asake = Artist(name="Asake")

    alien_girl = Song(title="Alien Girl", artists=[j_hus])
    turbulence = Song(title="Turbulence", artists=[wizkid, asake])

    songs = [alien_girl, turbulence]

    song_ids = song_repo.add_songs(songs)
    alien_girl_id = song_ids[0]
    result = song_repo.get_song(song_id=alien_girl_id)
    assert normalize_song(result) == normalize_song(alien_girl)

    new_alien_girl = Song(title="Alien Girl", artists=[j_hus], duration=10000)
    song_repo.update_song(song_id=alien_girl_id, song=new_alien_girl)
    result = song_repo.get_song(song_id=alien_girl_id)

    assert len(song_repo.get_all_songs()) == 2
    assert result.duration == 10000
    assert normalize_song(result) == normalize_song(new_alien_girl)


def test_remove_song(db_session):
    db = db_session
    song_repo = SongRepository(db=db)

    j_hus = Artist(name="J Hus")
    wizkid = Artist(name="Wizkid")
    asake = Artist(name="Asake")

    alien_girl = Song(title="Alien Girl", artists=[j_hus])
    turbulence = Song(title="Turbulence", artists=[wizkid, asake])

    songs = [alien_girl, turbulence]

    song_ids = song_repo.add_songs(songs)
    song_repo.remove_song(song_id=song_ids[0])

    result = song_repo.get_song(song_id=song_ids[0])

    assert result is None
    assert len(song_repo.get_all_songs()) == 1


def test_to_dataframe(db_session):
    db = db_session
    song_repo = SongRepository(db=db)

    j_hus = Artist(name="J Hus")
    wizkid = Artist(name="Wizkid")
    asake = Artist(name="Asake")

    alien_girl = Song(title="Alien Girl", artists=[j_hus])
    turbulence = Song(title="Turbulence", artists=[wizkid, asake])

    songs = [alien_girl, turbulence]

    song_ids = song_repo.add_songs(songs)
    df = song_repo.to_dataframe()

    assert len(df) == 2
    assert set(df.columns) == {"song_id", "title", "artists", "duration"}
    assert set(df["song_id"]) == set(song_ids)
    assert set(df["title"]) == {"Alien Girl", "Turbulence"}
    assert set(df["duration"]) == {0, 10000}

    assert df[df["title"] == "Alien Girl"]["artists"].iloc[0] == ["J Hus", "Wizkid"]
    assert df[df["title"] == "Turbulence"]["artists"].iloc[0] == ["Asake"]