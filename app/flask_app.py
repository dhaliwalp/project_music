from flask import Flask, render_template, request
from api_tools import get_token, search_for_artist, get_songs_by_similar_artists
from dotenv import load_dotenv
import os
from requests import post, get

app = Flask(__name__)

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

@app.route('/', methods=['GET', 'POST'])
def index():
    songs = []
    if request.method == 'POST':
        artist_names = [request.form.get('artist1'), request.form.get('artist2'), request.form.get('artist3')]
        token = get_token()
        for artist_name in artist_names:
            artist_result = search_for_artist(token, artist_name)
            if artist_result:
                artist_id = artist_result['id']
                artist_songs = get_songs_by_similar_artists(token, artist_id)
                for song in artist_songs:
                    artists = ', '.join(artist['name'] for artist in song['artists'])
                    song_info = {'name': song['name'], 'artists': artists, 'preview_url': song.get('preview_url')}
                    songs.append(song_info)
    return render_template('songs.html', songs=songs)


if __name__ == '__main__':
    app.run(debug=True)
