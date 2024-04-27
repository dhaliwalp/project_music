from flask import Flask, render_template, request
from api_tools import get_token, search_for_artist, get_artist_genres, get_songs_by_genres
import os
from dotenv import load_dotenv

app = Flask(__name__, template_folder='/src/templates', static_folder='/src/static', static_url_path='')

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
                artist_genres = get_artist_genres(token, artist_id)
                artist_songs = get_songs_by_genres(token, artist_genres)
                songs.append({'artist': artist_name, 'songs': artist_songs})
    return render_template('songs.html', songs=songs)

@app.route('/hello')
def hello():
    return render_template('hello.html')

if __name__ == '__main__':
    app.run(debug=True)