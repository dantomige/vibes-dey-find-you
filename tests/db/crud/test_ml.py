from unittest import mock
import pandas as pd
from src.db.crud.core import SongRepository
from src.db.crud.ml import AudioFeaturesRepository
from src.db.tables.core import SongModel, ArtistModel, song_artists_table
from src.db.tables.ml import AudioFeaturesModel
from src.schemas.audio_features import AudioFeatures


def test_add_audio_features(db_session):
    db = db_session
    audio_features_repo = AudioFeaturesRepository(db=db)

    expected_audio_features_model = AudioFeaturesModel(
        song_id="test_song_id",
        danceability=0.5,
        energy=0.5,
        key=5,
        loudness=-5.0,
        mode=1,
        speechiness=0.5,
        acousticness=0.5,
        instrumentalness=0.5,
        liveness=0.5,
        valence=0.5,
        tempo=120.0,
    )

    song_id = "test_song_id"

    features = AudioFeatures(
        danceability=0.5,
        energy=0.5,
        key=5,
        loudness=-5.0,
        mode=1,
        speechiness=0.5,
        acousticness=0.5,
        instrumentalness=0.5,
        liveness=0.5,
        valence=0.5,
        tempo=120.0,
    )

    audio_features_model = audio_features_repo.add_audio_features(
        song_id=song_id, features=features
    )

    assert audio_features_model == expected_audio_features_model
    assert db.query(AudioFeaturesModel).all() == [expected_audio_features_model]


def test_get_audio_features(db_session):
    db = db_session
    audio_features_repo = AudioFeaturesRepository(db=db)

    song_id = "test_song_id"

    features = AudioFeatures(
        danceability=0.5,
        energy=0.5,
        key=5,
        loudness=-5.0,
        mode=1,
        speechiness=0.5,
        acousticness=0.5,
        instrumentalness=0.5,
        liveness=0.5,
        valence=0.5,
        tempo=120.0,
    )

    expected_audio_features_model = AudioFeaturesModel(
        song_id=song_id, **features.model_dump()
    )

    audio_features_repo.add_audio_features(song_id=song_id, features=features)

    result = audio_features_repo.get_audio_features(song_id=song_id)

    assert result == expected_audio_features_model
    assert db.query(AudioFeaturesModel).all() == [expected_audio_features_model]

    assert (
        audio_features_repo.get_audio_features(song_id="non_existent_song_id") is None
    )


def test_update_audio_features(db_session):
    db = db_session
    audio_features_repo = AudioFeaturesRepository(db=db)

    song_id = "test_song_id"

    features = AudioFeatures(
        danceability=0.5,
        energy=0.5,
        key=5,
        loudness=-5.0,
        mode=1,
        speechiness=0.5,
        acousticness=0.5,
        instrumentalness=0.5,
        liveness=0.5,
        valence=0.5,
        tempo=120.0,
    )
    audio_features_repo.add_audio_features(song_id=song_id, features=features)

    updated_features = AudioFeatures(
        danceability=0.7,
        energy=0.7,
        key=7,
        loudness=-3.0,
        mode=0,
        speechiness=0.7,
        acousticness=0.7,
        instrumentalness=0.7,
        liveness=0.7,
        valence=0.7,
        tempo=130.0,
    )

    expected_audio_features_model = AudioFeaturesModel(
        song_id=song_id, **updated_features.model_dump()
    )

    audio_features_repo.update_audio_features(
        song_id=song_id, features=updated_features
    )

    result = audio_features_repo.get_audio_features(song_id=song_id)

    assert result == expected_audio_features_model
    assert db.query(AudioFeaturesModel).all() == [expected_audio_features_model]


def test_remove_audio_features(db_session):
    db = db_session
    audio_features_repo = AudioFeaturesRepository(db=db)

    song_id = "test_song_id"

    features = AudioFeatures(
        danceability=0.5,
        energy=0.5,
        key=5,
        loudness=-5.0,
        mode=1,
        speechiness=0.5,
        acousticness=0.5,
        instrumentalness=0.5,
        liveness=0.5,
        valence=0.5,
        tempo=120.0,
    )
    audio_features_repo.add_audio_features(song_id=song_id, features=features)

    audio_features_repo.remove_audio_features(song_id=song_id)

    assert audio_features_repo.get_audio_features(song_id=song_id) is None


def test_to_dataframe(db_session):
    db = db_session
    audio_features_repo = AudioFeaturesRepository(db=db)

    song_id = "test_song_id"

    features = AudioFeatures(
        danceability=0.5,
        energy=0.5,
        key=5,
        loudness=-5.0,
        mode=1,
        speechiness=0.5,
        acousticness=0.5,
        instrumentalness=0.5,
        liveness=0.5,
        valence=0.5,
        tempo=120.0,
    )

    expected_columns = [
        "song_id",
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
    ]

    audio_features_model = audio_features_repo.add_audio_features(
        song_id=song_id, features=features
    )

    df = audio_features_repo.to_dataframe()

    assert isinstance(df, pd.DataFrame)

    assert len(df) == 1
    assert df.columns.tolist() == expected_columns

    for column in expected_columns:
        assert df[column].iloc[0] == getattr(audio_features_model, column)
