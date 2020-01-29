import model

def diff(expected, actual):
    matched_playlists, new_playlists, old_playlists = match_playlists(expected, actual)

    for (exp, act) in matched_playlists:
        if exp.title != act.title or exp.description != act.description:
            yield model.UpdatePlaylistMetadata(
                id = act.id,
                title = exp.title,
                description = exp.description
            )

            # TODO: deal with the tracks

    for playlist in new_playlists:
        id = model.PlaceholderId.next()

        yield model.OpNewPlaylist(
            id,
            playlist.title,
            playlist.description,
        )

        for (idx, item) in enumerate(playlist.items):
            yield model.OpAddToPlaylist(
                id,
                item.video,
                idx,
            )

    for playlist in old_playlists:
        yield model.OpDeletePlaylist(playlist.id)

def match_playlists(expected, actual):
    """Pair up playlists from expected and actual and separate from new/deleted playlists."""
    # TODO
    return [], expected, []
