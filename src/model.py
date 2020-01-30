import typing

class PlaylistItem(typing.NamedTuple):
    """A playlistItem: https://developers.google.com/youtube/v3/docs/playlistItems#resource-representation """
    item_id: typing.Optional[str]
    playlist_id: str
    video_id: str
    position: int

class Playlist(typing.NamedTuple):
    """A playlist: https://developers.google.com/youtube/v3/docs/playlists#resource """
    playlist_id: str
    title: str
    description: str
    items: typing.List[PlaylistItem]

# YouTube operation objects

nonce = -1
class PlaceholderId(typing.NamedTuple):
    """Used to refer to a not-yet-created playlist inside OpAddToPlaylist."""
    nonce: int

    def next():
        global nonce
        nonce += 1
        return PlaceholderId(nonce)

    def __repr__(self):
        return f'(new playlist {self.nonce})'

class OpNewPlaylist(typing.NamedTuple):
    playlist_id: PlaceholderId
    title: str
    description: str

    def __repr__(self):
        return f'''Create new playlist.
    playlist_id: {self.playlist_id}
    title: {self.title}
    description: {self.description}'''

class OpUpdatePlaylistMetadata(typing.NamedTuple):
    playlist_id: str
    title: str
    description: str

    def __repr__(self):
        return f'''Update playlist metadata.
    playlist_id: {self.playlist_id}
    title: {self.title}
    description: {self.description}'''

class OpDeletePlaylist(typing.NamedTuple):
    playlist_id: str

    def __repr__(self):
        return f'''Delete a playlist.
    item_id: {self.item_id}'''

class OpAddToPlaylist(typing.NamedTuple):
    playlist_id: typing.Union[str, PlaceholderId]
    video_id: str
    position: int

    def __repr__(self):
        return f'''Add a new track to the playlist.
    playlist_id: {self.playlist_id}
    video_id: {self.video_id}
    position: {self.position}'''

class OpReorderPlaylistItem(typing.NamedTuple):
    item_id: str
    playlist_id: str
    video_id: str
    position: int

    def __repr__(self):
        return f'''Re-order an existing track in a playlist.
    item_id: {self.item_id}
    playlist_id: {self.playlist_id}
    video_id: {self.video_id}
    position: {self.position}'''

class OpRemoveFromPlaylist(typing.NamedTuple):
    item_id: str

    def __repr__(self):
        return f'''Remove a track from a playlist.
    item_id: {self.item_id}'''
