#!/bin/bash

SZ=32m
JD_SZ=16m
RUN_FSCK=1
OVERRIDE_PATH=1
MAX_FSCK=2
CMD=
FEATURES=
TEST_RESIZE2FS=0
TEST_E2FSCK=0
MAX_FUZZ_TIME=10


DIR=/tmp
TESTMNT="${DIR}/mnt/"
BASE_IMG="${DIR}/image"
JOURNAL_DEV="${DIR}/journal_dev"

SCRIPT_DIR="$(dirname "$0")"
ARG_FUZZ_DIR="${SCRIPT_DIR}/"
MKE2FS_CONFIG="${SCRIPT_DIR}/json/mke2fs.json"
RESIZE2FS_CONFIG="${SCRIPT_DIR}/json/resize2fs.json"
E2FSCK_CONFIG="${SCRIPT_DIR}/json/e2fsck.json"


help() {
	echo "Usage: $0 OPTIONS"
	echo "-d:	Create test files in this directory. (${DIR})"
	echo "-n:	Run the fuzzing loop for this many times. (${MAX_FUZZ_TIME})"
	echo "-s:	Create FS images of this size. (${SZ})"
	echo "-S:	Copy files from this dir. (${SRCDIR})"
	echo "-x:	Run e2fsck at most this many times. (${MAX_FSCK})"
	echo "-m:	Read mke2fs config file from this path and run mke2fs"
	echo "-r:	Read resize2fs config file from this path and run resize2fs"
	echo "-k: 	Read e2fsck config files from this path and run e2fsck"
	echo "-h: 	Print help"
	exit 0
}

GETOPT="d:n:s::S:m:r:kfpx:h:"
test "${HAS_FUSE2FS}" && GETOPT="${GETOPT}u"

while getopts "${GETOPT}" opt; do
	case "${opt}" in
	"d")
		DIR="${OPTARG}"
		;;
	"n")
		MAX_FUZZ_TIME="${OPTARG}"
		;;
	"s")
		SZ="${OPTARG}"
		;;
	"p")
		OVERRIDE_PATH=0
		;;
	"x")
		MAX_FSCK="${OPTARG}"
		;;
	"S")
		SRCDIR="${OPTARG}"
		;;
	"m")
		MKFS_CONFIG="${OPTARG}"
		;;
	"r")
		TEST_RESIZE2FS=1
		# RESIZE2FS_CONFIG="${OPTARG}"
		;;
	"k")
		TEST_E2FSCK=1
		e2fsck_CONFIG="${OPTARG}"
		;;
	"h")
		help
		;;
	*)
		help
		;;
	esac
done

if [ "${OVERRIDE_PATH}" -gt 0 ]; then
	PATH="${SCRIPT_DIR}:${SCRIPT_DIR}/bin/:${PATH}"
	export PATH
fi

#########################
# step 1: set up images #
#########################
echo "+ create fs images"
umount "${TESTMNT}"
rm -rf "${TESTMNT}"
mkdir -p "${TESTMNT}"
rm -rf "${BASE_IMG}"
rm -rf "${JOURNAL_DEV}"

truncate -s "${SZ}" "${BASE_IMG}"
echo "++ created ${BASE_IMG}, size ${SZ}"
truncate -s "${JD_SZ}" "${JOURNAL_DEV}"
echo "++ created ${JOURNAL_DEV}, size ${JD_SZ}"
echo "+ create fs images: done"
echo ""

# Fuzz mke2fs configuration 
echo "+ fuzz mke2fs configuration"
CMD=$(arg_fuzz ${MKE2FS_CONFIG})

############# Modify here ##############
FEATURES= # features need to trigger the bug, 
#example: FEATURES="has_journal,extent,huge_file,flex_bg,uninit_bg,dir_nlink"
# mke2fs -F -O ${FEATURES} ${BASE_IMG}
########################################

mke2fs ${BASE_IMG}
# echo $CMD 
# ${CMD}
# mke2fs ${CMD} ${BASE_IMG}
if [ $? -ne 0 ]; then
	echo "++ mke2fs failed with configuration: ${CMD}"
	exit $?
fi
echo "+ fuzz mke2fs configuration: done"
echo ""

############################
# step 2: age the FS image #
############################
echo "+ age the file system"
# modprobe loop
mount "${BASE_IMG}" "${TESTMNT}"
# mount "${BASE_IMG}" "${TESTMNT}" -o loop
if [ $? -ne 0 ]; then
	echo "++ mount failed"
	exit $?
fi

############# Modify here ##############
cd "${TESTMNT}"
# run workload here
echo "++ Workload finished"
cd ..
# cd "${SCRIPT_DIR}"
########################################

umount "${TESTMNT}"

# if [ "${TEST_E2FSCK}" -ne 0 ]; then
# 	echo "++ target utilty is e2fsck, apply corruption workload"
# 	######## corruption here ########
# 	# example: e2fuzz
# 	#################################
# 	if [ $? -ne 0 ]; then
# 		echo "++ corruption failed"
# 		exit $?
# 	fi
# 	echo "++ apply corruption workload: done"	
# fi
# echo "+ age the file system: done"


# ##################################
# # step 3: execute target utility #
# ##################################
# echo "+ execute target utility"
# if [ "${TEST_RESIZE2FS}" -ne 0 ]; then
# 	echo "++ target utilty is resize2fs"
# 	CMD=$(arg_fuzz ${MKE2FS_CONFIG})
# 	# echo $CMD 
# 	# ${CMD}
# 	# resize2fs ${CMD} ${BASE_IMG}
# 	resize2fs ${BASE_IMG}
# 	if [ $? -ne 0 ]; then
# 		echo "resize2fs failed with configuration: ${CMD}"
# 		exit $?
# 	fi
# 	echo "++ resize2fs finished succesfully"	
# fi
# if [ "${TEST_E2FSCK}" -ne 0 ]; then
# 	echo "++ target utilty is e2fsck"
# 	CMD=$(arg_fuzz ${E2FSCK_CONFIG})
# 	# echo $CMD 
# 	# ${CMD}
# 	# resize2fs ${CMD} ${BASE_IMG}
# 	e2fsck -yf ${BASE_IMG}
# 	if [ $? -ne 0 ]; then
# 		echo "e2fsck failed with configuration: ${CMD}"
# 		exit $?
# 	fi
# 	echo "++ e2fsck finished succesfully"	
# fi
# echo "+ execute target utility: done"

# ##################################
# # step 4: run verifier 
# ##################################
# echo "+ post-utility verification"
# ############# Modify here ##############
# # run verification here and give report 
# ########################################
# echo "+ post-utility verification: done"

#################################
step 5: clean up 
#################################
echo "+ clean up"
rm -rf "${TESTMNT}"
rm -rf "${BASE_IMG}"
rm -rf "${JOURNAL_DEV}"
echo "+ clean up: done"

