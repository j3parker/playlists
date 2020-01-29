# Playlists

A collection of YouTube playlists. To make a new playlist, make a new file.

* `*.yaml`: descriptions of playlists
* `.github/`: syncs the playlists to YouTube on every commit (to `master`).
* `src/sync.py`: the tool which do-eth the syncs
* `src/dev.sh`: run a container that has all the goods necessary to run `src/sync.py`
