import os
import time
import requests
from typing import Optional
from dotenv import load_dotenv
from collections import Counter
from src.schemas import Song, Artist, Date


class MusicBrainzService:

    BASE_URL = "https://musicbrainz.org/ws/2/"
    PAGE_LIMIT = 100

    def __init__(self, header, limit=None):
        self.header = header
        self.limit = limit if limit is not None else self.PAGE_LIMIT

    def _genre_from_json(self, tags_json) -> list[str]:
        return [tag["name"] for tag in tags_json]

    def _artist_from_json(self, artist_json) -> Artist:
        return Artist(arid=artist_json["id"], name=artist_json["name"])

    def _song_from_json(self, song_json) -> Song:
        return Song(
            rid=song_json.get("rid"),
            isrc=song_json.get("isrc"),
            title=song_json["title"],
            artists=[
                self._artist_from_json(artist_json["artist"])
                for artist_json in song_json["artist-credit"]
            ],
            release_date=Date.from_string(song_json.get("first-release-date")),
            genre=self._genre_from_json(song_json.get("tags")),
            duration=song_json.get("length"),
        )

    def list_genres(self) -> list[str]:
        """Fetch all genres from MusicBrainz."""

        endpoint = f"{self.BASE_URL}genre/all?limit={self.limit}&fmt=txt"

        response = requests.get(endpoint, headers=self.header)
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            return []

        genres = response.text.splitlines()
        return genres

    def list_artists_in_genres(self, genres) -> list[Artist]:
        """
        Fetch artists in the specified genres from MusicBrainz.
        Args:
            genres (list[str]): List of genres to search for.
            Returns:
                list[Artist]: List of artists in the specified genres.
        """

        all_artists = []
        seen_artist_arids = set()

        for genre in genres:

            offset = 0
            count = None

            while count != 0:
                endpoints = f"{self.BASE_URL}artist?query=tag:{genre}&limit={self.limit}&offset={offset}&fmt=json"
                response = requests.get(endpoints, headers=self.header)

                if response.status_code != 200:
                    print(f"Error fetching data: {response.status_code}")

                response_json = response.json()

                artists_jsons = response_json["artists"]
                artists = [self._artist_from_json(artist) for artist in artists_jsons]
                new_artists = [
                    artist for artist in artists if artist.arid not in seen_artist_arids
                ]

                all_artists.extend(new_artists)
                seen_artist_arids.update(
                    [new_artist.arid for new_artist in new_artists]
                )

                count = len(artists)
                offset += count

                time.sleep(1)

        return all_artists
    
    def list_songs_in_genres(self, genres, date_from=None, date_to=None) -> list[Song]:
        """
        Fetch songs in the specified genres from MusicBrainz. Filters by first-release-date (inclusive) if given
        Args:
            genres (list[str]): List of genres to search for.
            date_from (str, optional): Start date for filtering songs (YYYY-MM-DD). Filter by first-release-date. Defaults to None.
            date_to (str, optional): End date for filtering songs (YYYY-MM-DD). Filter by first-release-date. Defaults to None.
        Returns:
            list[Song]: List of songs in the specified genres.
        """
        all_songs = []
        seen_song_mbids = set()

        for genre in genres:

            offset = 0
            count = None

            while count != 0:
                endpoint = f"{self.BASE_URL}recording?query=tag:{genre}&limit={self.limit}&offset={offset}&fmt=json"

                response = requests.get(endpoint, headers=self.header)

                if response.status_code != 200:
                    print(f"Error fetching data: {response.status_code}")

                response_json = response.json()

                print(response_json["count"], response_json["offset"])

                songs_jsons = response_json["recordings"]
                songs = [self._song_from_json(song_json) for song_json in songs_jsons]
                new_songs = [song for song in songs if song.mbid not in seen_song_mbids]

                all_songs.extend(new_songs)
                seen_song_mbids.update([new_song.mbid for new_song in new_songs])

                count = len(songs)
                offset += count

                time.sleep(1)

        return all_songs


if __name__ == "__main__":

    load_dotenv()

    headers = {
        "User-Agent": f"VibesDeyFindYou/1.0 (contact: {os.getenv("HEADER_CONTACT")})"
    }

    service = MusicBrainzService(headers)

    afro_genres = [
        "afrobeats",
        "afrobeat",
        "afropiano",
        "afroswing",
        "amapiano",
        "alté",
        "highlife",
    ]

    afrobeats_artists = service.list_artists_in_genres(afro_genres)
    afrobeats_artists_names = [
        afrobeats_artist.name for afrobeats_artist in afrobeats_artists
    ]
    artist_names_freq = Counter(afrobeats_artists_names)

    for name, freq in artist_names_freq.items():
        if freq > 1:
            print("Repeated name: ", name)

            for artist in afrobeats_artists:
                if artist.name == name:
                    print("Repeated names ids: ", {artist.arid})

    print(afrobeats_artists_names)
    print(len(afrobeats_artists_names))
    print(len(set(afrobeats_artists_names)) == len(afrobeats_artists_names))
    print(len(set(a.arid for a in afrobeats_artists)) == len(afrobeats_artists))

    popular_artists = ["Wizkid", "Burna Boy", "Davido", "Ruger"]

    for artist in popular_artists:
        print(
            f"Checking {artist} in found afrobeats artists: ",
            artist in afrobeats_artists_names,
        )

    afro_songs = service.list_songs_in_genres(genres=afro_genres)
    afro_songs_titles = [song.title for song in afro_songs]

    print(afro_songs_titles)
    print((len(afro_songs_titles)))

    popular_songs = ["Woman", "Lonely at the Top", "UNAVAILABLE"]

    for song in popular_songs:
        print(
            f"Checking {song} in found afrobeats songs: ",
            song in afro_songs_titles,
        )
