from unittest.mock import Mock, call
from src.schemas.song import Song
from src.schemas.artist import Artist
from src.services.music_brainz_service import MusicBrainzService


def test_list_genres():
    mock_client = Mock()

    mock_response = Mock()
    mock_response.text = "amapiano\nafrobeats\nafroswing"
    mock_client.get.return_value = mock_response

    service = MusicBrainzService(client=mock_client)
    expected_genres = ["amapiano", "afrobeats", "afroswing"]
    genres = service.list_genres()

    assert sorted(genres) == sorted(expected_genres)


def test_artists_in_genres(load_fixture):
    mock_client = Mock()

    all_response_json = load_fixture("multiple_recordings.json")

    mock_response_first_page = Mock()
    mock_response_first_page.json.return_value = all_response_json["pages"][0]

    mock_response_second_page = Mock()
    mock_response_second_page.json.return_value = all_response_json["pages"][1]

    mock_response_third_page = Mock()
    mock_response_third_page.json.return_value = all_response_json["pages"][2]

    mock_response_fourth_page = Mock()
    mock_response_fourth_page.json.return_value = all_response_json["pages"][3]

    mock_client.get.side_effect = [
        mock_response_first_page,
        mock_response_second_page,
        mock_response_third_page,
        mock_response_fourth_page,
    ]

    service = MusicBrainzService(client=mock_client, limit=2)

    asake = Artist(arid="1001", name="Asake")
    ruger = Artist(arid="1002", name="Ruger")
    davido = Artist(arid="1003", name="Davido")
    burna_boy = Artist(arid="1004", name="Burna Boy")
    shallipopi = Artist(arid="1005", name="Shallipopi")

    expected_artists = [asake, ruger, davido, burna_boy, shallipopi]

    artists = service.list_artists_in_genres(["afrobeat"])

    calls = mock_client.get.call_args_list
    api_call_params = [call.kwargs["params"] for call in calls]

    assert [p["offset"] for p in api_call_params] == [0, 2, 4, 5]
    assert [p["limit"] for p in api_call_params] == [2, 2, 2, 2]
    assert sorted(a.arid for a in artists) == sorted(a.arid for a in expected_artists)


def test_songs_in_genres(load_fixture):

    mock_client = Mock()

    all_response_json = load_fixture("multiple_recordings.json")

    mock_response_first_page = Mock()
    mock_response_first_page.json.return_value = all_response_json["pages"][0]

    mock_response_second_page = Mock()
    mock_response_second_page.json.return_value = all_response_json["pages"][1]

    mock_response_third_page = Mock()
    mock_response_third_page.json.return_value = all_response_json["pages"][2]

    mock_response_fourth_page = Mock()
    mock_response_fourth_page.json.return_value = all_response_json["pages"][3]

    mock_client.get.side_effect = [
        mock_response_first_page,
        mock_response_second_page,
        mock_response_third_page,
        mock_response_fourth_page,
    ]

    service = MusicBrainzService(client=mock_client, limit=1)

    ruger = Artist(arid="art1001", name="Ruger")
    wizkid = Artist(arid="art1002", name="Wizkid")
    asake = Artist(arid="art1003", name="Asake")
    travis_scott = Artist(arid="art1004", name="Travis Scott")

    expected_songs = [
        Song(rid="1001", title="Asiwaju", artists=[ruger]),
        Song(rid="1002", title="Ojuelegba", artists=[wizkid]),
        Song(rid="1003", title="Active", artists=[asake, travis_scott]),
    ]

    songs = service.list_songs_in_genres(genres=["afrobeats"], date_from="2024-01-01")
    calls = mock_client.get.call_args_list
    api_call_params = [call.kwargs["params"] for call in calls]

    assert [p["offset"] for p in api_call_params] == [0, 1, 2, 3]
    for p in api_call_params:
        assert p["limit"] == 1
        assert "tag:afrobeats" in p["query"]
        assert "first-release-date:[2024-01-01 TO *]" in p["query"]
        assert "AND" in p["query"]

    assert sorted(s.rid for s in songs) == sorted(s.rid for s in expected_songs)
