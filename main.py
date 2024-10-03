import requests
from bs4 import BeautifulSoup

import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://example.com"


date = input("When are we going? (Type in a date in the format YYYY-MM-DD)\n")
print(date)

URL = f"https://www.billboard.com/charts/hot-100/{date}/"
#URL = f"https://www.billboard.com/charts/hot-100/2022-04-30/"

response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, 'html.parser')

#print(soup.prettify())

all_songs_titles = soup.find_all(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")

all_artists = soup.find_all(name="span", class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only")

first_song = soup.find_all(name="a", class_="c-title__link lrv-a-unstyle-link")[0].getText(strip=True)
first_artist = soup.find_all(name="p", class_="c-tagline a-font-primary-l a-font-primary-m@mobile-max lrv-u-color-black u-color-white@mobile-max lrv-u-margin-tb-00 lrv-u-padding-t-025 lrv-u-margin-r-150")[0].getText(strip=True)

song_titles = [(title.getText(strip=True)) for title in all_songs_titles]
song_artists = [(title.getText(strip=True)) for title in all_artists]

song_titles.insert(0, first_song)
song_artists.insert(0, first_artist)
print(song_titles)
print(song_artists)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

me = sp.current_user()['id']

playlist = sp.user_playlist_create(user=me, name=f"{date} Billboard 100", public=False)
id_playlist = playlist['id']

"""
searched_song = sp.search(q="track%3AYellow%2520artist%3AColdplay", type="track", limit=1)
print(searched_song)
song_name = searched_song["tracks"]["items"][0]["name"]
song_uri = searched_song["tracks"]["items"][0]["uri"]
print(song_name)
print(song_uri)
"""

all_uri_list = []

for i in range(0,100):
    searched_song = sp.search(q=f"track%3A{song_titles[i]}%2520artist%3A{song_artists[i]}", type="track", limit=1)
    song_name = searched_song["tracks"]["items"][0]["name"]
    song_uri = searched_song["tracks"]["items"][0]["uri"]
    all_uri_list.append(song_uri)
    #print(f"{song_name} - {song_uri}")

print(all_uri_list)

sp.playlist_add_items(playlist_id=id_playlist, items=all_uri_list)
print("Todo listo! Checa Spotify")

"""
Links

Spotipy Documentation: https://spotipy.readthedocs.io/en/2.22.1/
Spotify for Developers Documentation: https://developer.spotify.com/documentation/web-api
"""
