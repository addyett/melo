import json
import os
from dataclasses import dataclass, field
from typing import List, Optional

import appdirs
import pyyoutube
import spotipy
from youtube_dl import YoutubeDL
from ytmusicapi import YTMusic

APP_DIR = os.path.join(appdirs.user_data_dir(), '.melo')
CACHE_PATH = os.path.join(appdirs.user_data_dir(), '.melo', 'spotify_cache')

YT = pyyoutube.Api(api_key='AIzaSyCq47Zxsu4pN1MMWBNa04380TGDxT7hrQM')

YTDL = YoutubeDL({
    # 'outtmpl': self.title + self.ext,
    'format': 'bestaudio',
    'extractaudio': True,
    'retries': 5,
    'continuedl': True,
    'nopart': True,
    'hls_prefer_native': True,
    'quiet': True
})

SCOPES = '''
            user-read-playback-state
            user-follow-read
            user-follow-modify
            playlist-read-private
            playlist-read-collaborative
            playlist-modify-private
            playlist-modify-public
            user-read-recently-played
            user-library-read
            user-library-modify
            user-top-read
            user-read-private
        '''  # pylint: disable=invalid-name

if os.path.exists(CACHE_PATH):
    SPOTIFY = spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            scope=SCOPES,
            client_id="22e27810dff0451bb93a71beb5e4b70d",
            client_secret="6254b7703d8540a48b4795d82eae9300",
            redirect_uri="http://localhost:8080/",
            cache_handler=spotipy.CacheFileHandler(
                cache_path=CACHE_PATH
            )
        )
    )
else:
    SPOTIFY = spotipy.Spotify(
        auth_manager=spotipy.SpotifyClientCredentials(
            client_id='22e27810dff0451bb93a71beb5e4b70d',
            client_secret='6254b7703d8540a48b4795d82eae9300'
        )
    )

_ytmusic_cookies = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "SAPISIDHASH 1643090086_74cc0985095757af3f1af65902686e81b6637950",
    "content-encoding": "gzip",
    "content-type": "application/json",
    "cookie": "VISITOR_INFO1_LIVE=uyP5rRxNQhk; PREF=tz=Asia.Calcutta&f6=40000000; YSC=Q9aJ39XjaxI; SID=GQiVhB2tjMF5Z0BE6-SY--IlCwcC_z3cS4W8BGpxVd7stlEzvK9hxJn9F7fJub0alxpgdA.; __Secure-1PSID=GQiVhB2tjMF5Z0BE6-SY--IlCwcC_z3cS4W8BGpxVd7stlEzHz9XaSut4DXx5clU4qpx1A.; __Secure-3PSID=GQiVhB2tjMF5Z0BE6-SY--IlCwcC_z3cS4W8BGpxVd7stlEzYr0_Hswrcd9rmYm2Xxia_Q.; HSID=AXeZ83FjzhA8x1gY2; SSID=A0Z7pkk9iPB6BX-3f; APISID=04432aWLTO54P4Gp/A-Oni_5vP1OAfIYeT; SAPISID=Orxl6q7KyzDWyxMB/Ag-yFYBZUXWy4E778; __Secure-1PAPISID=Orxl6q7KyzDWyxMB/Ag-yFYBZUXWy4E778; __Secure-3PAPISID=Orxl6q7KyzDWyxMB/Ag-yFYBZUXWy4E778; LOGIN_INFO=AFmmF2swRAIgHSN980c9f8lkxpke8TdftmbblS4jZ7yTp1YTiR4DLvsCICKFB1SIMxehNygfMgnGc1YN6vED-kFyi8MzTWG0SyfM:QUQ3MjNmejk0emRXVURCMmsyLXNxaGN2LUN3N2FfOVkyNHlDR3lDb0poVmhMV0xDMnVRQUdiaHlueWVkSTVNZHFNejY5SWdiVFJ6NTBNbGNuU2o3UXNjazRRMmVDYmlTZ3Zrc1pMZWF0ZE5oV0xzeWpFQXJKWHlHcXRESFIxQnAzX3VMT1FJOElUOHNFSHN5ZXZNaUNBMzk2TXB2U1YtLXNR; SIDCC=AJi4QfGNmCEAfa_dQq_4mIiapY6nuREkM-CXP4G7dphqBk6k8wJgqW538_oPf3A8yMrd7zkGCA; __Secure-3PSIDCC=AJi4QfEs1oqCsKgL0dbAqFDExHQDcWnX49JGwoqdKv0eo_1NxlzcNAYsNQ_Rv4Vd3l32kda0Vw",
    "dnt": "1",
    "origin": "https://music.youtube.com",
    "referer": "https://music.youtube.com/",
    "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"97\", \"Chromium\";v=\"97\"",
    "sec-ch-ua-arch": "\"x86\"",
    "sec-ch-ua-bitness": "\"64\"",
    "sec-ch-ua-full-version": "\"97.0.4692.71\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-platform-version": "\"14.0.0\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "same-origin",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "x-client-data": "CIq2yQEIo7bJAQjBtskBCKmdygEI7enKAQjq8ssBCJ75ywEI1/zLAQjmhMwBCIOVzAEI9pXMAQ==",
    "x-goog-authuser": "0",
    "x-goog-visitor-id": "Cgt1eVA1clJ4TlFoayikob6PBg%3D%3D",
    "x-origin": "https://music.youtube.com",
    "x-youtube-client-name": "67",
    "x-youtube-client-version": "1.20220119.00.00"
}

YTMUSIC = YTMusic(auth=json.dumps(_ytmusic_cookies))


class Image:
    """
    An object representing a Spotify image resource.

    Attributes
    ----------
    height : :class:`str`
        The height of the image.
    width : :class:`str`
        The width of the image.
    url : :class:`str`
        The URL of the image.
    """

    __slots__ = ("height", "width", "url")

    def __init__(self, *, height: str, width: str, url: str):
        self.height = height
        self.width = width
        self.url = url

    def __repr__(self):
        return f"<melo.Image: {self.url!r} (width: {self.width!r}, height: {self.height!r})>"

    def __eq__(self, other):
        return type(self) is type(other) and self.url == other.url


@dataclass
class SearchResults:
    """A dataclass   of search results.

    Attributes
    ----------
    artists : List[:class:`Artist`]
        The artists of the search.
    playlists : List[:class:`Playlist`]
        The playlists of the search.
    albums : List[:class:`Album`]
        The albums of the search.
    tracks : List[:class:`Track`]
        The tracks of the search.
    """

    def __add__(self, other: "SearchResults"):
        self_items = self.__dict__.items()
        for attr, val in other.__dict__.items():
            if attr not in self_items:
                self.__setattr__(attr, val)
            else:
                self.__setattr__(attr, self.__getattribute__(attr).extend(val))
        return self

    def __bool__(self):
        return any(self.__dict__.values())

    def __repr__(self) -> str:
        return f"<melo.SearchResults: {id(self)}>"

    artists: Optional[List] = field(default_factory=list)
    albums: Optional[List] = field(default_factory=list)
    tracks: Optional[List] = field(default_factory=list)
    playlists: Optional[List] = field(default_factory=list)


class URIBase:
    '''A base class to define basic dunder methods for all URI baed methods. It's purpose is to reduce boiler plate for models

    All melo models must inherit from this class to have basic dunder methods
    '''

    uri = repr(None)
    id = repr(None)

    def __hash__(self):
        return hash(self.uri)

    def __eq__(self, __o: object) -> bool:
        return (
            type(self) is type(__o) and self.uri == __o.uri
        )

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def __bool__(self):
        return not not self.id

    def __str__(self) -> str:
        return self.uri
