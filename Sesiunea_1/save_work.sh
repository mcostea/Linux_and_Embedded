#!/bin/bash

SOURCE_DIR="/home/mihai/_work/Curs_UT/Curs1"

DEST_DIR="/home/mihai/saves"
DATE=$(date +"%Y-%m-%d")

DEST_PATH="$DEST_DIR/$DATE"

mkdir -p "$DEST_PATH"

cp -r "$SOURCE_DIR/." "$DEST_PATH"

echo "Fisiere copiate la : $DEST_PATH"
