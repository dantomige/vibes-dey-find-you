import requests
import pandas as pd
from src.client.http_client import HTTPClient
from dotenv import load_dotenv

class ReccoBeatService:

    def __init__(self, client):
        self.client = client

    def list_features(self) -> list[str]:
        raise NotImplementedError

    def get_artist_id(self, artist_query: str):
        raise NotImplementedError

    def fetch_artist_spotify_url(self, artist_query: str):
        raise NotImplementedError
    
    def get_artist_songs(self, artist_id: str):
        raise NotImplementedError

    def fetch_audio_features(
        self, recco_ids: list[str], features: list[str]
    ) -> pd.DataFrame:
        """Fetches the specified audio features for the given recording IDs (RIDs) from the AcousticBrainz API.
        Args:
            rids (list[str]): A list of recording IDs for which to fetch audio features.
            features (list[str]): A list of audio features to fetch for each recording ID.
        Returns:
            pd.DataFrame: A DataFrame containing the requested audio features for each recording ID.
        """
        raise NotImplementedError

if __name__ == "__main__":

    url = "https://api.reccobeats.com/v1/artist/search"

    params = {
        "searchText": "Asake"
    }

    res = requests.get(url, params=params)

    print("Status:", res.status_code)
    data = res.json()

    found_artist = None

    for artist in data["content"]:
        if artist["name"] == "Asake":
            print(artist)
            found_artist = artist


    found_track = None
    page = 0

    while True:
        url = f"https://api.reccobeats.com/v1/artist/{found_artist['id']}/track"
        params = {"page": page}
        res = requests.get(url, params=params)

        print("Status:", res.status_code) ### need to do something if it fails here
        data = res.json()

        print(len(data["content"]), data["page"], data["size"], data["totalElements"], data["totalPages"])

        for track in data["content"]:
            if track["trackTitle"] == "Jogodo": ### need better comparison here 
                # print(track)
                found_track = track
                break
        
        if data["page"] == data["totalPages"] - 1:
            break

        page += 1

    print(found_track)

    track_id = found_track["id"]

    url = "https://api.reccobeats.com/v1/audio-features"

    params = {
        "ids": track_id
    }

    res = requests.get(url, params=params)

    print("Status:", res.status_code)
    data = res.json()

    print(data)

