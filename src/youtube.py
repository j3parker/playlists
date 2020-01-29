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
                id = item['id'],
                video = item['contentDetails']['videoId'],
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

            self.placeholder_map[op.id.nonce] = new_id
            print(f'Remembering that {op.id} -> {new_id}')

        elif isinstance(op, model.OpUpdatePlaylistMetadata):
            self.update_playlist(
                id = op.id,
                title = op.title,
                description = op.description,
            )

        elif isinstance(op, model.OpDeletePlaylist):
            self.delete_playlist(
                id = op.id,
            )

        elif isinstance(op, model.OpAddToPlaylist):
            if isinstance(op, model.PlaceholderId):
                playlist_id = self.placeholder_map[op.playlist_id.nonce]
            else:
                playlist_id = op.playlist_id

            print(f'adding {video_id} to {playlist_id}')

            self.insert_playlistitem(
                playlist_id = playlist_id,
                video_id = op.video_id,
                position = op.position,
            )

        elif isinstance(op, model.ReorderPlaylistItem):
            self.update_playlistitem(
                playlist_id = op.playlist_id,
                video_id = op.video_id,
                position = op.position,
            )

        elif isinstance(op, model.RemoveFromPlaylist):
            self.delete_playlistitem(
                playlist_id = op.playlist_id,
                video_id = op.video_id,
            )

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

    def update_playlist(self, id, title, description):
        raise Exception('unimplemented')

    def delete_playlist(self, id):
        raise Exception('unimplemented')

    def list_playlistitems(self, id):
        self.client.playlistItems().list(
            part = 'contentDetails',
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

    def update_playlistitem(self, playlist_id, video_id, position):
        raise Exception('unimplemented')

    def delete_playlistitem(self, playlist_id, video_id):
        raise Exception('unimplemented')
