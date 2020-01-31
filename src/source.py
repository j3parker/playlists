import model
import pathlib
import re
import yaml

class Client:
    """An interface to read playlists from source control."""

    def __init__(self, working_dir):
        self.working_dir = working_dir

    def get_playlists(self):
        yamlFiles = pathlib.Path(self.working_dir).glob('*.yaml')

        playlists = []
        for path in yamlFiles:
            with open(path) as f:
                doc = yaml.load(f, Loader = yaml.SafeLoader)
                playlists.append(parse_playlist(doc))

        return playlists

def parse_playlist(doc):
    playlist_id = doc.get('id')

    return model.Playlist(
        playlist_id,
        doc['title'],
        doc['description'] or "",
        items = [
            model.PlaylistItem(
                None,
                playlist_id,
                parse_video_id_from_url(track),
                idx
            )
            for (idx, track) in enumerate(doc['tracks'])
        ],
    )

# It's nice to put the URLs into the file for human copy & paste.
url_pattern = re.compile('https://www.youtube.com/watch\\?v=([a-zA-Z0-9_-]*)')

def parse_video_id_from_url(url):
    return url_pattern.fullmatch(url.strip()).group(1)
