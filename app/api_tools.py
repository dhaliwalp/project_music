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

    if genres:
        genres = genres[1:]
    
    return genres

def get_songs_by_genres(token, genres):
    songs = []
    for genre in genres:
        url = f"https://api.spotify.com/v1/search?q=genre:{genre}&type=track&limit=10"
        headers = get_auth_header(token)
        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        genre_songs = json_result.get("tracks", {}).get("items", [])
        for song in genre_songs:
            if song.get("preview_url"): 
                songs.append(song)
                break  
    return songs

def get_songs_by_similar_artists(token, artist_id, limit=4):
    songs = []
    added_artist_ids = set()
    
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    similar_artists = json_result.get("artists", [])
    
    for artist in similar_artists:
        similar_artist_id = artist["id"]
        if similar_artist_id in added_artist_ids:
            continue 
        similar_artist_url = f"https://api.spotify.com/v1/artists/{similar_artist_id}/top-tracks?country=US"
        similar_artist_result = get(similar_artist_url, headers=headers)
        similar_artist_json = json.loads(similar_artist_result.content)
        similar_artist_tracks = similar_artist_json.get("tracks", [])
        
        if similar_artist_tracks:
            track = similar_artist_tracks[0] 
            if track.get("preview_url"):
                songs.append(track)
                added_artist_ids.add(similar_artist_id)
                if len(songs) >= limit:
                    break
    
    return songs[:limit]



# Usage example

# token = get_token()
# result = search_for_artist(token, "Frank Ocean")
# artist_id = result["id"]
# artist_genres = get_artist_genres(token, artist_id)
# genre_songs = get_songs_by_genres(token, artist_genres)

# # print(artist_genres)

# for idx, song in enumerate(genre_songs):
#     print(f"{idx + 1}. {song['name']} - {', '.join(artist['name'] for artist in song['artists'])}")
