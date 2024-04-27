from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"  #can put artist,track

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("NO artists with this name exist..")
        return None

    return json_result[0]

def get_songs_by_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_artist_genres(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    genres = json_result.get("genres", [])
    return genres

def get_songs_by_genres(token, genres):
    songs = []
    for genre in genres:
        url = f"https://api.spotify.com/v1/search?q=genre:{genre}&type=track&limit=1"
        headers = get_auth_header(token)
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        genre_songs = json_result.get("tracks", {}).get("items", [])
        if genre_songs:
            songs.append(genre_songs[0])
    return songs







# Usage example

# token = get_token()
# result = search_for_artist(token, "Playboi")
# artist_id = result["id"]
# artist_genres = get_artist_genres(token, artist_id)
# genre_songs = get_songs_by_genres(token, artist_genres)

# for idx, song in enumerate(genre_songs):
#     print(f"{idx + 1}. {song['name']} - {', '.join(artist['name'] for artist in song['artists'])}")



    # for idx, song in enumerate(songs):
#     print(f"{idx + 1}.{song['name']}")