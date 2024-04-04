from flask import Flask, jsonify, redirect, request, session, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import uuid
from flask_caching import Cache

import random
# app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))

app = Flask(__name__)
app.secret_key = 'SOME_SECRET_KEY'  # Used to add security for session data
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
app.config['SESSION_COOKIE_NAME'] = 'spotify_auth_session'
app.config['SESSION_PERMANENT'] = False
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds

cache = Cache(app)

# Replace these with your Spotify app credentials
client_id = "3d817d22c6fa48a0a0f0c3ded9dee186"
client_secret = "779b1a0338c64f2b82d336130de07d38"
redirect_uri = "https://spurdle-4ce9b96bb79b.herokuapp.com/callback"
# redirect_uri = "http://localhost:8888/callback"

scope = "streaming user-read-email user-read-private user-modify-playback-state user-library-read"

# Spotify OAuth object
sp_oauth = SpotifyOAuth(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        scope=scope,
                        cache_path=".cache-" + str(uuid.uuid4()))

@app.route('/')
def login():
    if not session.get('token_info'):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return render_template('index.html')  # Your HTML file with the Web Playback SDK

@app.route('/callback')
def callback():
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect('/')

@app.route('/get-liked-songs')
@cache.cached(timeout=300, key_prefix='liked_songs')  # Cache this view for 5 minutes
def get_liked_songs():
    # Your logic to fetch liked songs
    sp = spotipy.Spotify(auth_manager=sp_oauth)

    results = sp.current_user_saved_tracks()
    songs = results['items']

    while results['next']:
        results = sp.next(results)  
        songs.extend(results['items'])
    
    # Assuming you want to return a simplified list of song names
    song_list = [song['track']['name'] for song in songs]
    print('got all songs')
    return jsonify(song_list)

@app.route('/get-random-song')
def get_random_liked_song():
    """
    Retrieves a random liked song for the current authorized user.

    Returns:
        A dictionary containing track information for the randomly selected liked song.
    """

    sp = spotipy.Spotify(auth_manager=sp_oauth)

    # Get the total number of tracks to determine the range for random selection
    results = sp.current_user_saved_tracks(limit=1)
    total_tracks = results['total']

    # Choose a random offset within the total number of saved tracks
    random_offset = random.randint(0, total_tracks - 1)

    # Fetch a single track at the random offset
    result = sp.current_user_saved_tracks(limit=1, offset=random_offset)
    track = result['items'][0]['track']

    # Prepare the selected track's information
    # selected_song = {
    #     "title": track['name'],
    #     "artist": track['artists'][0]['name'],
    #     "preview_url": track['preview_url'],  # URL to a 30s preview of the song, if available
    #     "spotify_url": track['external_urls']['spotify']  # Link to the song on Spotify
    # }
    print(track['name'])

    return jsonify({"previewUrl": track['preview_url'], "title": track['name']})

@app.route('/submit-guess', methods=['POST'])
def submit_guess():
    data = request.get_json()
    guess = data.get('guess', 'none')

    print(guess)
    return jsonify({'message': 'Guess received', 'guess': guess})

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=8888)
