#!/usr/bin/env bash

DRIVE=/tmp/VHD.img
TABLE=$1

dd if=/dev/zero of=$DRIVE bs=1M count=512
sfdisk $DRIVE < "$TABLE"
LOOP=$(losetup --show -Pf $DRIVE)

mkfs -t ext4 "$LOOP"'p1'
mkfs -t ext2 "$LOOP"'p2'
mkfs.vfat -F 32 "$LOOP"'p3'
mkswap "$LOOP"'p4'
echo "$LOOP" > loop_path.tmp