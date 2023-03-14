from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth 
from flask import Flask, url_for, session
import time
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def create_spotify_oauth():
    return SpotifyOAuth(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=url_for('redirectPage', _external=True),
            scope="user-library-read")

def get_token2():
    token_valid = False
    token_info = session.get("token_info", {})

    # Checking if the session already has a token stored
    if not (session.get('token_info', False)):
        token_valid = False
        return token_info, token_valid

    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(session.get('token_info').get('refresh_token'))

    token_valid = True
    return token_info, token_valid

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
    json_result =  json.loads(result.content)
    
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result =  json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist name exists")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def cleaner(json):
    result_str = ""
    for idx, song in enumerate(json):
        result_str += f" {idx + 1}. {song['name']}"
    return result_str

def get_user_data(token):
    url = "https://api.spotify.com/v1/me/top/artists"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    print(result.content)
    # json_result = json.loads(result.content)
    # print(json_result)

    

# result = search_for_artist(token,"bts")
# artist_id = result["id"]
# print(artist_id)
# songs  = get_songs_by_artist(token, artist_id)

# cleaner(songs)