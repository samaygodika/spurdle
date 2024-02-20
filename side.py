import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

# Replace with your credentials
client_id = "3d817d22c6fa48a0a0f0c3ded9dee186"
client_secret = "779b1a0338c64f2b82d336130de07d38"
redirect_uri = "http://localhost:8888/callback"

# Scope permissions (adjust as needed)
scope = "user-library-read"

# Create SpotifyOAuth object
sp_oauth = SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope)

def get_liked_songs():
    """
    Retrieves liked songs for a given username using user authorization.

    Args:
        username: Spotify username of the user.

    Returns:
        A list of dictionaries containing track information for liked songs.
    """

    # Obtain access token through user authorization flow
    sp = spotipy.Spotify(auth_manager=sp_oauth)

    # Get current user's saved tracks (liked songs)
    results = sp.current_user_saved_tracks()
    liked_songs = []

    # for item in results['items']:
    #     track = item['track']
    #     liked_songs.append({"title": track['name'], "artist": track['artists'][0]['name']})

    while results:
        for idx, item in enumerate(results['items']):
            track = item['track']
            liked_songs.append({"title": track['name'], "artist": track['artists'][0]['name']})
        if results['next']:
            results = sp.next(results)
        else:
            results = None

    return liked_songs

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
    selected_song = {
        "title": track['name'],
        "artist": track['artists'][0]['name'],
        "preview_url": track['preview_url'],  # URL to a 30s preview of the song, if available
        "spotify_url": track['external_urls']['spotify']  # Link to the song on Spotify
    }

    return selected_song

def play_snippet(song, attempt):
    # Placeholder for playing a song snippet
    # The actual implementation will depend on the Spotify playback capabilities you integrate
    print(f"Playing {attempt + 1} second(s) of the song...")  # Simulate playing a snippet
    print(f"Hint: The song is by {song['artist']}")  # Provide a hint

def start_game():
    target_song = get_random_liked_song()
    print("Guess the song! You'll hear more of it with each wrong guess.")

    max_attempts = 5
    for attempt in range(max_attempts):
        play_snippet(target_song, attempt)
        guess = input("Enter your guess: ")
        if guess.lower() == target_song['title'].lower():
            print("Congratulations! You've guessed the song!")
            break
        else:
            print("Wrong guess. Try again!")
            if attempt < max_attempts - 1:
                print("Let's reveal a bit more of the song...\n")
            else:
                print(f"Sorry, you've run out of attempts. The song was '{target_song['title']}' by {target_song['artist']}.")

if __name__ == "__main__":
    start_game()

# Example usage
# username = input("Enter Spotify username: ")
# username = "samaygodika"
# liked_songs = get_liked_songs()


# if liked_songs:
#     for song in liked_songs:
#         print(f"{song['title']} - {song['artist']}")

# Example usage
# random_song = get_random_liked_song()
# print(random_song)

# print(f"Random Liked Song: {random_song['title']} - {random_song['artist']}")
# print(f"Preview URL: {random_song['preview_url']}")
# print(f"Spotify URL: {random_song['spotify_url']}")