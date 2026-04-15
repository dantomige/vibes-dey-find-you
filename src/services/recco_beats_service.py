import requests
import pandas as pd
from src.schemas.song import Song
from src.schemas.audio_features import AudioFeatures
from src.client.http_client import HTTPClient


class ReccoBeatService:

    MAX_LIMIT = 50

    def __init__(self, client, limit=None):
        self.client = client
        self.limit = limit if limit is not None else self.MAX_LIMIT

    def list_features(self) -> list[str]:
        raise NotImplementedError

    def get_recco_beats_artist_id(self, artist_name: str) -> str | None:
        """
        Fetches the Recco Beats artist ID for the given artist name.
        Args:
            artist_name (str): The name of the artist for which to fetch the Recco Beats artist ID.
            Returns:
            str | None: The Recco Beats artist ID corresponding to the given artist name, or None if not found.
        """
        raise NotImplementedError

    def fetch_artist_page_url(self, artist_name: str) -> str | None:
        """
        Fetches the page URL for the given artist name.
        Args:
            artist_name (str): The name of the artist for which to fetch the page URL.
        Returns:
            str | None: The page URL corresponding to the given artist name, or None if not found.
        """
        raise NotImplementedError

    def get_artist_songs(self, recco_beats_artist_id: str) -> list[Song]:
        """
        Fetches the songs for the given Recco Beats artist ID.
        Args:
            recco_beats_artist_id (str): The Recco Beats artist ID for which to
            fetch the songs.
        Returns:
            list[Song]: A list of songs corresponding to the given Recco Beats artist ID. Populates song
            with the following fields: title, artist_name, recco_beats_track_id. The other fields can be left as None or empty.
            Artists are also populated with the name and recco_beats_id fields, and the other fields can be left as None or empty.
        """

        raise NotImplementedError

    def fetch_audio_features(
        self, recco_beats_track_ids: list[str]) -> list[AudioFeatures | None]:
        """
        Fetches the specified audio features for the given recording IDs (RIDs) from the Recco Beats API.
        Args:
            recco_beats_track_ids (list[str]): A list of recording IDs for which to fetch audio features.
        Returns:
            list[AudioFeatures | None]: A list of audio features where each item corresponds to the features on recco_beats_track_ids in
            the same order. If a track ID is invalid or features cannot be fetched, the corresponding item will be None.
        """
        raise NotImplementedError


if __name__ == "__main__":

    artist_name = "Asake"

    url = "https://api.reccobeats.com/v1/artist/search"

    params = {"searchText": artist_name}

    res = requests.get(url, params=params)

    print("Status:", res.status_code)
    data = res.json()

    found_artist = None

    print(len(data["content"]))
    print(data)

    for artist in data["content"]:
        print(artist)
        if artist["name"] == artist_name:
            found_artist = artist

    found_track = None
    limit = 25
    page = 0

    while True:
        url = f"https://api.reccobeats.com/v1/artist/{found_artist['id']}/track"
        params = {"page": page, "size": limit}
        res = requests.get(url, params=params)

        print("Status:", res.status_code)  ### need to do something if it fails here
        data = res.json()

        # print(data)

        print(
            len(data["content"]),
            data["page"],
            data["size"],
            data["totalElements"],
            data["totalPages"],
        )

        for track in data["content"]:
            if track["trackTitle"] == "Jogodo":  ### need better comparison here
                # print(track)
                found_track = track
                break

        if data["page"] == data["totalPages"] - 1:
            break

        page += 1

    print(found_track)

    track_id = found_track["id"]
    track_ids = [track["id"] for track in data["content"][:2]]
    track_ids = ["2740e843-bd29-47d9-afcb-9b97f3e14ef3", "db29b2b4-69b9-4965-99ce-fbd35b992dce", "dasda"]

    print(len(track_ids))
    print(track_ids)

    url = "https://api.reccobeats.com/v1/audio-features"

    params = {"ids": track_ids}

    res = requests.get(url, params=params)

    print("Status:", res.status_code)
    data = res.json()

    print(len(data["content"]))
    print(data)
    
