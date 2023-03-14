from flask import Flask, render_template, request, redirect, session
from templates.main import get_token, search_for_artist, get_songs_by_artist, cleaner, create_spotify_oauth
from requests import get, post
from spotipy.oauth2 import SpotifyOAuth 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)
@app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template("home.html")

@app.route('/search', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        artist_name = request.form['artist_name']
        token = get_token()
        artist = search_for_artist(token, artist_name)
        
        return render_template('index.html', artist=artist, cleaner=cleaner, get_songs_by_artist=get_songs_by_artist,token=token )
    else:
        string = "Artist not found"
        return render_template('index.html', string=string)

@app.route('/redirect')
def redirectPage():
    # sp_oauth = create_spotify_oauth()
    # session.clear()
    # code = request.args.get("code")
    # token_info = sp_oauth.get_access_token(code)
    # session[TOKEN_INFO] = token_info
    return redirect("/main")
    
if __name__ == "__main__":
    app.run(debug=True)