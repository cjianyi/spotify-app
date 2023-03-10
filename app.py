from flask import Flask, render_template, request
from templates.main import get_token, search_for_artist, get_songs_by_artist, cleaner
from requests import get, post
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')
@app.route('/search', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        artist_name = request.form['artist_name']
        token = get_token()
        artist = search_for_artist(token, artist_name)
        
        return render_template('index.html', artist=artist, cleaner=cleaner, get_songs_by_artist=get_songs_by_artist,token=token )
    else:
        return render_template('index.html')
    
if __name__ == "__main__":
    app.run(debug=True)