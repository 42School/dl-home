#!/bin/sh

TMP="/tmp/img2tgz/$1/"
SRC="/mnt/homes/$1.img"
DST="/tmp/img2tgz/$1.tar.gz"

if [ -f "$DST" ]
then
    exit
fi

mkdir -p "$TMP"
mount -o loop "$SRC" "$TMP"
tar cfz "$DST" --exclude=./Library -C "$TMP" .
umount "$TMP"
rmdir "$TMP"
