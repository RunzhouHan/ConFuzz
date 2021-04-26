#!/bin/bash


# MAX = 1000000
# FS_SIZE = 100
# blocksize = 1024
# journal_dev = "journal_dev"
# image = "loop_dev"
# mount_dir = './mnt'
# os_list = ["linux_1.0", "linux_1.1","linux_1.2","linux_2.0"]
# ext_list = ["ext2", "ext3", "ext4"]
# usage_list = ["floppy", "small", "default"]
# UUID_list = ["2b8fd835-3b1b-4258-9a41-7345c6aa15e1", "13f725e4-a4a4-11eb-bcbc-0242ac1./30002"]


# DIR=/tmp
PASSES=10
# SZ=32m
# SCRIPT_DIR="$(dirname "$0")"
# BLK_SZ=4096
# INODE_SZ=256
# EXTENDED_OPTS="discard"
# EXTENDED_FSCK_OPTIONS=""
# RUN_FSCK=1
# OVERRIDE_PATH=1
# HAS_FUSE2FS=0
# USE_FUSE2FS=0
# MAX_FSCK=10
# SRCDIR=/etc

# CONFIG_FILE=mke2fs.json

count=0

for i in {1..10}
do
	./arg_fuzz mke2fs.json
	tmp=$(./arg_fuzz mke2fs.json)
	mke2fs $tmp
	echo $?
	ret=$(echo $?)
	if [ $ret -gt 0 ]
	then
		count+=1
	fi
done

echo "${count}/${PASSES} succeeded."