import asyncio
from async_spotify import SpotifyApiClient
from async_spotify.authentification import SpotifyAuthorisationToken
from async_spotify.authentification.authorization_flows import AuthorizationCodeFlow
from pprint import pprint
from box import Box

scopes = [
  "user-library-read",
  "user-top-read",
  "user-read-private",
  "user-read-email",
  "user-read-currently-playing",
  "user-read-playback-state",
  "user-read-recently-played",
  "user-modify-playback-state",
  "playlist-read-private",
  "playlist-modify-private",
  "streaming",
]

client_id = '462a9ac24c9e447da38717e74876ebd3'
client_secret = '6bb0a6d2f0484fd0ae1b96ec9a221126'
redirect_uri = 'http://127.0.0.1:5000/login_redirect'

async def main():
    # Create a auth_code_flow object and load the auth_code_flow from env variables
    auth_flow = AuthorizationCodeFlow(client_id, client_secret, scopes, redirect_uri)
    #auth_flow.load_from_env()

    # Create a new Api client and pass the auth_code_flow
    api_client = SpotifyApiClient(auth_flow, hold_authentication=True)

    try:
      # Get the auth token with your code
      #code: str = "Your Spotify Code"
      #auth_token: SpotifyAuthorisationToken = await api_client.get_auth_token_with_code(code)
      auth_token = await api_client.get_or_load_auth_token(auth_flow.redirect_url)

      # Create a new client
      await api_client.create_new_client(request_limit=1500)

      # Start making queries with the internally saved token
      album_tracks: dict = await api_client.albums.get_tracks('03dlqdFWY9gwJxGl3AREVy')
      pprint(album_tracks)

      # If you pass a valid auth_token this auth_token will be used for making the requests
      album_tracks: dict = await api_client.albums.get_tracks('03dlqdFWY9gwJxGl3AREVy', auth_token)
      pprint(album_tracks)

      user_playlists = await api_client.playlists.current_get_all()
      pprint(user_playlists)
      print(len(user_playlists['items']))

    finally:
      await api_client.close_client()

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
