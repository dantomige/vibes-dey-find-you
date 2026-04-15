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

    def __init__(self, client, limit=None):
        self.client = client
        self.limit = limit if limit is not None else self.PAGE_LIMIT

    def _genre_from_json(self, tags_json) -> list[str]:
        raise NotImplementedError

    def _artist_from_json(self, artist_json) -> Artist:
        raise NotImplementedError

    def _song_from_json(self, song_json) -> Song:
        raise NotImplementedError

    def list_genres(self) -> list[str]:
        """Fetch all genres from MusicBrainz."""
        raise NotImplementedError

    def list_artists_in_genres(self, genres) -> list[Artist]:
        """
        Fetch artists in the specified genres from MusicBrainz.
        Args:
            genres (list[str]): List of genres to search for.
            Returns:
                list[Artist]: List of artists in the specified genres.
        """
        raise NotImplementedError
    
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
        raise NotImplementedError


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
