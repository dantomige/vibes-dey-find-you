from unittest.mock import Mock, call
from src.schemas.song import Song
from src.schemas.artist import Artist
from src.schemas.audio_features import AudioFeatures
from src.services.recco_beats_service import ReccoBeatService


def test_service_initialization():
    mock_client = Mock()
    service = ReccoBeatService(client=mock_client)
    assert service.client == mock_client
    assert service.limit == ReccoBeatService.MAX_LIMIT

    custom_limit = 25
    service_with_custom_limit = ReccoBeatService(client=mock_client, limit=custom_limit)
    assert service_with_custom_limit.limit == custom_limit


def test_get_artist_id(load_fixture):
    mock_client = Mock()

    mock_response = Mock()
    mock_response.json.return_value = load_fixture("recco_beats_artists.json")
    mock_client.get.return_value = mock_response

    service = ReccoBeatService(client=mock_client)

    artist_name = "Kendrick Lamar"
    artist_recco_beats_id = service.get_recco_beats_artist_id(artist_name=artist_name)

    expected_artist_recco_beats_id = "caa924b3-075d-462a-bc84-b8da4ebb9f38"
    assert mock_client.get.called_with(
        "https://api.reccobeats.com/v1/artist/search",
        params={"query": artist_name, "size": service.limit, "page": 0},
    )
    assert artist_recco_beats_id == expected_artist_recco_beats_id

    # also check case where query yields nothing (check what return would look like)

    mock_client.get.return_value.json.return_value = {
        "content": [],
        "page": 0,
        "size": 50,
        "totalElements": 0,
        "totalPages": 0,
    }
    artist_name = "fdakflda"

    artist_recco_beats_id = service.get_recco_beats_artist_id(artist_name=artist_name)

    assert mock_client.get.called_with(
        "https://api.reccobeats.com/v1/artist/search",
        params={"query": artist_name, "size": service.limit, "page": 0},
    )
    assert artist_recco_beats_id is None


def test_fetch_artist_page_url(load_fixture):
    mock_client = Mock()

    mock_response = Mock()
    mock_response.json.return_value = load_fixture("recco_beats_artists.json")
    mock_client.get.return_value = mock_response

    service = ReccoBeatService(client=mock_client)

    artist_name = "Kendrick Lamar"
    page_url = service.fetch_artist_page_url(artist_name=artist_name)

    expected_page_url = "https://open.spotify.com/artist/2YZyLoL8N0Wb9xBt1NhZWg"
    assert mock_client.get.called_with(
        "https://api.reccobeats.com/v1/artist/search",
        params={"query": artist_name, "size": service.limit, "page": 0},
    )
    assert page_url == expected_page_url

    # also check case where query yields nothing (check what return would look like)
    mock_client.get.return_value.json.return_value = {
        "content": [],
        "page": 0,
        "size": 50,
        "totalElements": 0,
        "totalPages": 0,
    }
    artist_name = "fdakflda"
    page_url = service.fetch_artist_page_url(artist_name=artist_name)
    assert mock_client.get.called_with(
        "https://api.reccobeats.com/v1/artist/search",
        params={"query": artist_name, "size": service.limit, "page": 0},
    )
    assert page_url is None


def test_get_artist_songs(load_fixture):
    mock_client = Mock()

    all_response_json = load_fixture("recco_beats_songs.json")

    mock_response_first_page = Mock()
    mock_response_first_page.json.return_value = all_response_json["pages"][0]

    mock_response_second_page = Mock()
    mock_response_second_page.json.return_value = all_response_json["pages"][1]

    mock_client.get.side_effect = [mock_response_first_page, mock_response_second_page]

    service = ReccoBeatService(client=mock_client, limit=2)

    recco_beats_artist_id = "caa924b3-075d-462a-bc84-b8da4ebb9f38"
    songs = service.get_artist_songs(recco_beats_artist_id=recco_beats_artist_id)

    expected_songs = [
        Song(
            title="Wanna Be Heard",
            artists=[Artist(name="Kendrick Lamar")],
            recco_beats_id="track1",
        ),
        Song(
            title="LA",
            artists=[
                Artist(name="Kendrick Lamar"),
                Artist(name="Ty Dolla $ign"),
                Artist(name="Brandy"),
                Artist(name="James Fauntleroy"),
            ],
            recco_beats_id="track2",
        ),
        Song(
            title="Look Over Your Shoulder (feat. Kendrick Lamar)",
            artists=[Artist(name="Kendrick Lamar"), Artist(name="Busta Rhymes")],
            recco_beats_id="a0f93935-6b63-4ed6-9359-40eb5a12c22f",
        ),
        Song(
            title="Buy The World",
            artists=[
                Artist(name="Kendrick Lamar"),
                Artist(name="Mike WiLL Made-It"),
                Artist(name="Lil Wayne"),
                Artist(name="Future"),
            ],
            recco_beats_id="c0e21963-2e17-4df4-a0f9-6142812f3e7c",
        ),
    ]

    calls = mock_client.get.call_args_list
    api_call_params = [call.kwargs["params"] for call in calls]

    assert [p["page"] for p in api_call_params] == [0, 1]
    assert [p["size"] for p in api_call_params] == [2, 2]
    assert sorted(s.title for s in songs) == sorted(s.title for s in expected_songs)


def test_fetch_audio_features(load_fixture):
    mock_client = Mock()
    service = ReccoBeatService(client=mock_client)

    mock_response = Mock()

    mock_response.json.return_value = load_fixture("audio_features_response.json")

    mock_client.get.return_value = mock_response

    recco_beats_track_ids = [
        "2740e843-bd29-47d9-afcb-9b97f3e14ef3",
        "db29b2b4-69b9-4965-99ce-fbd35b992dce",
    ]
    expected_url = "https://api.reccobeats.com/v1/audio-features"
    expected_params = {
        "ids": recco_beats_track_ids,
    }

    audio_features = service.fetch_audio_features(
        recco_beats_track_ids=recco_beats_track_ids
    )

    expected_audio_features = [
        AudioFeatures(
            id="2740e843-bd29-47d9-afcb-9b97f3e14ef3",
            href="https://open.spotify.com/track/00ibm2mniJevaKFk9rllrX",
            isrc="FR5R00901562",
            acousticness=0.111,
            danceability=0.538,
            energy=0.949,
            instrumentalness=0.0,
            key=1,
            liveness=0.171,
            loudness=-3.143,
            mode=0,
            speechiness=0.361,
            tempo=83.274,
            valence=0.792,
        ),
        AudioFeatures(
            id="db29b2b4-69b9-4965-99ce-fbd35b992dce",
            href="https://open.spotify.com/track/00iiwyPq0Nt3TvyUYNSSK5",
            isrc="USAT21503251",
            acousticness=0.291,
            danceability=0.454,
            energy=0.482,
            instrumentalness=0.0,
            key=6,
            liveness=0.704,
            loudness=-7.257,
            mode=1,
            speechiness=0.0792,
            tempo=112.651,
            valence=0.362,
        ),
    ]

    assert audio_features == expected_audio_features
    mock_client.get.assert_called_with(expected_url, params=expected_params)

    # also check case where features is None (check what params would look like)
    expected_params_invalid_id = {"ids": recco_beats_track_ids + ["fake_id"]}
    audio_features_invalid_id = service.fetch_audio_features(
        recco_beats_track_ids=recco_beats_track_ids + ["fake_id"]
    )
    assert audio_features_invalid_id == expected_audio_features + [None]
    mock_client.get.assert_called_with(expected_url, params=expected_params_invalid_id)
