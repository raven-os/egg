#!/usr/bin/env bash

DRIVE=/tmp/VHD.img
LOOP=$(cat loop_path.tmp)

losetup -d "$LOOP"
rm loop_path.tmp
rm $DRIVE