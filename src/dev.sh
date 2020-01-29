#!/bin/sh
docker build -t playlists .
docker run -v $(pwd)/..:/git -it playlists /bin/bash
