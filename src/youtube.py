import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import model
import os

class Client:
    """Interface with YouTube for syncing playlists."""

    def __init__(self, client):
        self.client = client

    def from_environment():
        creds =google.oauth2.credentials.Credentials(
            token = None,
            token_uri = 'https://oauth2.googleapis.com/token',
            refresh_token = os.environ['REFRESH_TOKEN'],
            client_id = os.environ['OAUTH_CLIENT_ID'],
            client_secret = os.environ['OAUTH_CLIENT_SECRET'],
        )

        client = googleapiclient.discovery.build(
            'youtube', 'v3',
            credentials = creds,
        )

        return Client(client)

    def get_playlists(self):
        response = self.client.playlists().list(
            part = 'snippet,status',
            mine = True,
            maxResults = 50,
        ).execute()

        return [
            model.Playlist(
                playlist['id'],
                playlist['snippet']['title'],
                playlist['snippet']['description'],
                self.get_playlistitems(playlist['id']),
            )
            for playlist in response['items']
            if playlist['status']['privacyStatus'] == 'public'
        ]

    def get_playlistitems(self, id):
        response = self.client.playlistItems().list(
            part = 'contentDetails',
            playlistId = id,
            maxResults = 50,
        ).execute()

        return [
            model.PlaylistItem(
                id = item['id'],
                video = item['contentDetails']['videoId'],
            )
            for item in response['items']
        ]

    def apply(op):
        # TODO
        return



