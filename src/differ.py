import model

def diff_playlists(expected, actual):
    matched_playlists, new_playlists, deleted_playlists = match_playlists(expected, actual)

    for (exp, act) in matched_playlists:
        if exp.title != act.title or exp.description != act.description:
            yield model.OpUpdatePlaylistMetadata(
                playlist_id = act.playlist_id,
                title = exp.title,
                description = exp.description
            )

        for op in diff_tracks(exp.items, act.items):
            yield op

    for playlist in new_playlists:
        id = model.PlaceholderId.next()

        yield model.OpNewPlaylist(
            id,
            playlist.title,
            playlist.description,
        )

        for item in playlist.items:
            yield model.OpAddToPlaylist(
                id,
                item.video_id,
                item.position,
            )

    for playlist in deleted_playlists:
        yield model.OpDeletePlaylist(playlist.playlist_id)

def match_playlists(expected, actual):
    expected_ids = {}
    new_playlists = []
    for (idx, playlist) in enumerate(expected):
        if playlist.playlist_id is None:
            new_playlists.append(playlist)
        else:
            expected_ids[playlist.playlist_id] = idx

    deleted_playlists = []
    matched_playlists = []
    for playlist in actual:
        if playlist.playlist_id in expected_ids:
            idx = expected_ids[playlist.playlist_id]
            matched_playlists.append((expected[idx], playlist))
        else:
            deleted_playlists.append(playlist)

    return matched_playlists, new_playlists, deleted_playlists

def diff_tracks(expected, actual):
    matched_tracks, new_tracks, deleted_tracks = match_tracks(expected, actual)

    for (exp, act) in matched_tracks:
        if exp.position != act.position:
            yield model.OpReorderPlaylistItem(
                act.item_id,
                exp.playlist_id,
                exp.video_id,
                exp.position,
            )

    for track in new_tracks:
        yield model.OpAddToPlaylist(
            track.playlist_id,
            track.video_id,
            track.position,
        )

    for track in deleted_tracks:
        yield model.OpRemoveFromPlaylist(track.item_id)

def match_tracks(expected, actual):
    expected_video_ids = {}
    for (idx, track) in enumerate(expected):
        expected_video_ids[track.video_id] = idx

    matched_tracks = []
    actual_video_ids = {}
    deleted_tracks = []
    for track in actual:
        if track.video_id in actual_video_ids:
            # Just in class, clean up duplicate tracks
            deleted_tracks.append(track)
        elif track.video_id in expected_video_ids:
            idx = expected_video_ids[track.video_id]
            matched_tracks.append((expected[idx], track))
        else:
            deleted_tracks.append(track)

        actual_video_ids[track.video_id] = True

    new_tracks = []
    for track in expected:
        if track.video_id not in actual_video_ids:
            new_tracks.append(track)

    return matched_tracks, new_tracks, deleted_tracks
