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
        self.placeholder_map = {}

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
        response = self.list_playlists()

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
        response = self.list_playlistitems(id)

        return [
            model.PlaylistItem(
                item['id'],
                item['snippet']['playlistId'],
                item['contentDetails']['videoId'],
                item['snippet']['position'],
            )
            for item in response['items']
        ]

    def apply(self, op):
        if isinstance(op, model.OpNewPlaylist):
            new_id = self.insert_playlist(
                title = op.title,
                description = op.description,
                privacy_status = 'public',
            )

            self.placeholder_map[op.playlist_id.nonce] = new_id
            print(f'Remembering that {op.playlist_id} -> {new_id}')

        elif isinstance(op, model.OpUpdatePlaylistMetadata):
            self.update_playlist(
                playlist_id = op.playlist_id,
                title = op.title,
                description = op.description,
            )

        elif isinstance(op, model.OpDeletePlaylist):
            self.delete_playlist(
                playlist_id = op.playlist_id,
            )

        elif isinstance(op, model.OpAddToPlaylist):
            if isinstance(op.playlist_id, model.PlaceholderId):
                playlist_id = self.placeholder_map[op.playlist_id.nonce]
            else:
                playlist_id = op.playlist_id

            self.insert_playlistitem(
                playlist_id = playlist_id,
                video_id = op.video_id,
                position = op.position,
            )

        elif isinstance(op, model.OpReorderPlaylistItem):
            self.update_playlistitem(
                item_id = op.item_id,
                playlist_id = op.playlist_id,
                video_id = op.video_id,
                position = op.position,
            )

        elif isinstance(op, model.OpRemoveFromPlaylist):
            self.delete_playlistitem(op.playlist_id)

        else:
            raise Exception('unimplemented operation')

    def list_playlists(self):
        return self.client.playlists().list(
            part = 'snippet,status',
            mine = True,
            maxResults = 50,
        ).execute()

    def insert_playlist(self, title, description, privacy_status):
        return self.client.playlists().insert(
            part = 'snippet,status',
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                },
                'status': {
                    'privacyStatus': privacy_status,
                },
            },
        ).execute()['id']

    def update_playlist(self, playlist_id, title, description):
        self.client.playlists().update(
            part = 'id,snippet',
            body = {
            	'id': playlist_id,
                'snippet': {
                    'title': title,
                    'description': description,
                },
            },
        ).execute()

    def delete_playlist(self, playlist_id):
        self.client.playlists().delete(playlist_id).execute()

    def list_playlistitems(self, id):
        return self.client.playlistItems().list(
            part = 'contentDetails,snippet',
            playlistId = id,
            maxResults = 50,
        ).execute()

    def insert_playlistitem(self, playlist_id, video_id, position):
        self.client.playlistItems().insert(
            part = 'snippet',
            body = {
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id,
                    },
                    'position': position,
                },
            },
        ).execute()

    def update_playlistitem(self, item_id, playlist_id, video_id, position):
        self.client.playlistItems().update(
            part = 'snippet',
            body = {
                'id': item_id,
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id,
                    },
                    'position': position,
                },
            },
        ).execute()

    def delete_playlistitem(self, item_id):
        self.client.playlistItems().delete(item_id).execute()
