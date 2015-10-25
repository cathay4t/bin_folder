#!/bin/bash
ffmpeg -i "$1" -vn -acodec libvorbis -aq 5 "$2"
