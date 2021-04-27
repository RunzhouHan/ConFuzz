import json

MAX = 1000
fs_size = 50000
blocksize = 1024
journal_dev = "journal_dev"
image = "loop_dev"
mount_dir = './mnt'
legacy_dir = '/tmp/legacy'
os_list = ["linux_1.0", "linux_1.1","linux_1.2","linux_2.0"]
ext_list = ["ext2", "ext3", "ext4"]
usage_list = ["floppy", "small", "default"]
UUID_list = ["2b8fd835-3b1b-4258-9a41-7345c6aa15e1", "13f725e4-a4a4-11eb-bcbc-0242ac130002"]
''' important: satisfying byte-per-inode ratio is essential to guarantee semantic correctness, 
need to specify some rules fo ensure this value is capatible with other arg values. Otherwise,
mke2fs will report 'Cannot create filesystem with requested number of inodes'
Currently have found value of '-E resize' (id:7) conflicts with value of '-g' (id:13)  '''

# Global rule: remove the last sibling operator of each arg branch

# value type      #        format  	  	meaning
# arithmatic_int    1      [a,b,c]    	arithmatic sequence between [int a,int b] with factor int c
# geometric_int     2	   [a,b,c,d]  	
# string            3	   "something"	"something"
# string_array      4      ["a","b"]    select one out of "a" and "b"

mke2fs_command = {
	"-b": {
		"id": 0,
		# "arg": "-b",
		"value_type": 2,
		"value": [2, 0, 2, 1024], # (2^0 to 2^2)*1024
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": True, # set true for -i
		"dependency_id": None,
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-c": {
		"id": 1,
		# "arg": "-c",
		"value_type": None,
		"value": None,
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,
		"weight": None,
		"must_child": False,
		"child_id": [2],
		"c":{
			"id": 2,
			# "arg": "c",
			"value_type": None,
			"value": None,
			"operator_value": None,
			"operator_sibling": None,
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [1],
			"weight": None,
			"must_child": False,
			"child_id": None
			}
		},
	"-E": {
		"id": 3,
		# "arg": "-E",
		"value_type": None,
		"value": None,
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": " ",
		"mutex": None,
		"must_have": True,
		"dependencies_id": None,
		"weight": None,
		"must_child": True,
		"child_id": [4,5,6,7, 8,9,10],
		"stride=": {  # RAID arg, need to test with '='' & '= ' 
			"id": 4,
			# "arg": "stride=", 
			"value_type": 1,
			"value": [0, MAX, 1], 
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,  
			"must_have": False,
			"dependency_id": [3], 
			"weight": None,
			"must_child": False,
			"child_id": None
			},
		"stripe-width=": {  # RAID arg
			"id": 5,
			# "arg": "stride-width=", 
			"value_type": 1,
			"value": [0, MAX, 1], # This is typically stride-size * N
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,  
			"must_have": False,
			"dependency_id": [3], 
			"weight": None,
			"must_child": False,
			"child_id": None
			},
		"resize=": {  
			"id": 6,
			# "arg": "resize=", 
			"value_type": 1,
			# "value": [0, MAX, 1], 
			"value": [0, 1000000, 1], 
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None, 
			"must_have": False,
			"dependency_id": [3], 
			"weight": None,
			"must_child": False,
			"child_id": None
			},
		"lazy_itable_init=": {  
			"id": 7,
			# "arg": "lazy_itable_init=", 
			"value_type": 1,
			"value": [0, 1, 1],
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,  
			"must_have": False,
			"dependency_id": [3], 
			"weight": None,
			"must_child": False,
			"child_id": None
			},
		"test_fs": {  
			"id": 8,
			# "arg": "test_fs", 
			"value_type": None,
			"value": None,
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None, 
			"must_have": False,
			"dependency_id": [3], 
			"weight": None,
			"must_child": False,
			"child_id": None
			},
		"discard": {  
			"id": 9,
			# "arg": "discard",  # SSD-related argument, discarding blocks initially is useful on solid state devices and sparse / thin-provisioned storage
			"value_type": None,
			"value": None,
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None, 
			"must_have": False,
			"dependency_id": [3], 
			"weight": None,
			"must_child": False,
			"child_id": None
			},
		"nodiscard": {  
			"id": 10,
			# "arg": "nodiscard",  # SSD-related argument, discarding blocks initially is useful on solid state devices and sparse / thin-provisioned storage
			"value_type": None,
			"value": None,
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None, 
			"must_have": False,
			"dependency_id": [3], 
			"weight": None,
			"must_child": False,
			"child_id": None
			}
		},
		# {
		# "id": ,
		# "arg": "-f",
		# "value": -1,
		# "operator_sibling": " ",
		# "operator_child": None,
		# "mutex": None,
		# "must_have": False,
		# "dependency_id": None,
		# "child": None
		# },
	"-F ": {
		"id": 11,
		# "arg": "-F",
		"value_type": None,
		"value": None,
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": True,
		# set as true currently to avoid popping questions
		"dependency_id": None,
		"weight": None,
		"must_child": False,
		"child_id": None
		},

########################################
##############checkpoint################
########################################
# checkpoint for modification on value type
	"-g ": {
		"id": 12,
		# "arg": "-g",
		#  if (fs_param.s_blocks_per_group < 256 ||
		#              fs_param.s_blocks_per_group > 8 * (unsigned) blocksize) {
		#              com_err(program_name, 0, "%s",
		#                  _("blocks per group count out of range"));
		#              exit(1);
		"value_type": 1,
		"value": [0, MAX, 8], # -3 is a flag for 'multiply'. Here it means 8 * N, maximum value is limited by disk capacity, may conflict with value (id:7)
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-G": {
		"id": 13,
		# "arg": "-G",
		"value_type": 2, # should be power of 2, 0,-1 means 2^0 to 2^n, min & max need to be checked
		"value": [2, 0, 10, 1],
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": [32], # to be replaced with real id
		"weight": None,
		"must_child": False,
		"child_id": None
		},		
	"-i": {
		"id": 14,
		# "arg": "-i",
		"value_type": 1,
		# "value": [1024, 67108864, 1],
		"value": [1024, 4096, 1],
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},	
	"-I": {
		"id": 15,
		# "arg": "-I",
		"value_type": 2,
		"value": [2, 0, 3, 128],  # value between 128 and 1024
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},
		# Global rule here: For 15 & 16, inode_size * inode_count shouldn't exceed blocksize * total_blocks
	"-j": {
		"id": 16,
		# "arg": "-j",
		"value_type": None,
		"value": None,
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		# May need to be modified later May have to have ext3/4 enabled. In other words, doesn't work with a ext2 file system, 
		# tested with '-t ext2 -j', it will create a ext3 instead, so no dependency/mutex need to be specified here
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-J": {
		"id": 17,
		# "arg": "-J",
		"value_type": None,
		"value": None,
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": " ",
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": True,
		"child_id": [18, 19],
		"size=": {  
			"id": 18,
			# "arg": "size=", 
			"value_type": 1,
			# Global Rule: The size of the journal must be at least 1024 filesystem blocks (i.e., 1MB if using 1k blocks, 4MB if using 4k blocks, etc.) and may be no more than 102,400 filesystem blocks.
			"value": [1024*blocksize/1048576, 102400*blocksize/1048576, 1], 
			# "value": [1024*blocksize, 102400*blocksize, 1], 
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": [19],  
			"must_have": False,
			"dependency_id": [17], 
			"weight": None,
			"must_child": False,
			"child_id": None
			},
		"device=": {  
			"id": 19,
			# "arg": "device=", 
			"value_type": 3,
			"value": journal_dev, 
			# Global rule: The external journal must already have been created using the command
			# mke2fs -O journal_dev external-journal
			# where external-journal must have been created with the same block size as the new filesystem
			# Need more design here ...
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": [18],  
			"must_have": False,
			"dependency_id": [17],  # Need more dependencies related to 'mke2fs -O journal_dev external-journal'
			"weight": None,
			"must_child": False,
			"child_id": None
			}
			
		},	
	"-K": {
		"id": 20,
		# "arg": "-K",
		# An SSD related arg, Keep, do not attempt to discard blocks at mkfs time
		# depreciated, better one is '-E discard'
		"value_type": None,
		"value": None,
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},	
	"-l": {
		"id": 21,
		# "arg": "-l",
		# An SSD related arg, Keep, do not attempt to discard blocks at mkfs time
		# Mostly equvalant to -c
		"value_type": 3,
		"value": image,  # value between 128 and 1024
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},		
	"-L": {
		"id": 22,
		# "arg": "-L",
		# The maximum length of the volume label is 16 bytes. 
		"value_type": 1,
		"value": [0, MAX, 1], 
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},	
	"-m": {
		"id": 23,
		# "arg": "-m",
		"value_type": 1,
		"value": [0,50,1], 
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},	
	"-M": {
		"id": 24,
		# "arg": "-M",
		"value_type": 3,
		"value": mount_dir, 
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-n": {
		"id": 25,
		# "arg": "-n",
		"value_type": None,
		"value": None, 
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-N": {
		"id": 26,
		# "arg": "-N",
		"value_type": 1,
		"value": [0,MAX,1], 
		# Global rule: val_I * val_N <= block_num * block_size, is also related to val_i
		# Need a mature rule to orchestract -N -i -I and other possible inode num/size values
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-o": {
		"id": 27,
		# "arg": "-o",
		"value_type": 4,
		"value": os_list, 
		# Need to provide a OS name list later
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-O": {
		"id": 28,
		# "arg": "-O",
		"value_type": None,
		"value": None, 
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": " ",
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": True,
		"child_id": [29,30,31,32,33,34,35,36,37,38],
		"dir_index": {
			"id": 29,
			# "arg": "dir_index",
			"value_type": None,
			"value": None, 
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [28],  
			"weight": None,
			"must_child": False,
			"child_id": None
			},
		"extent": {
			"id": 30,
			# "arg": "extent",
			"value_type": None,
			"value": None, 
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [28],  
			"weight": None,
			"must_child": False,
			"child_id": None
			},
		"filetype": {
			"id": 31,
			# "arg": "filetype",
			"value_type": None,
			"value": None, 
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [28],  
			"weight": None,
			"must_child": False,
			"child_id": None
			},
		"flex_bg": {
			"id": 32,
			# "arg": "flex_bg",
			"value_type": None,
			"value": None, 
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [28],  
			"weight": None,
			"must_child": False,
			"child_id": None
			},
		"has_journal": {
			"id": 33,
			# "arg": "has_journal",
			"value_type": None,
			"value": None, 
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [28],  
			"weight": None,
			"must_child": False,
			"child_id": None
			},
		"journal_dev": {
			"id": 34,
			# "arg": "journal_dev",
			# Create an external ext3 journal on the given device instead of a regular ext2 filesystem. 
			# Note that external-journal must be created with the same block size as the filesystems that will be using it.
			"value_type": None,
			"value": None, 
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [28],  
			"weight": None,
			"must_child": False,
			"child_id": None
			},
		"large_file": {
			"id": 35,
			# "arg": "large_file",
			# Modern kernels set this feature automatically when a file > 2GB is created.
			"value_type": None,
			"value": None, 
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [28],  
			"weight": None,
			"must_child": False,
			"child_id": None
			},
		"resize_inode": {
			"id": 36,
			# "arg": "resize_inode",
			# related to -E resize
			"value_type": None,
			"value": None, 
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [28],  
			"weight": None,
			"must_child": False,
			"child_id": None
		},
		"sparse_super": {
			"id": 37,
			# "arg": "sparse_super",
			# save space for large fs
			"value_type": None,
			"value": None, 
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [28],  
			"weight": None,
			"must_child": False,
			"child_id": None
		},
		"uninit_bg": {
			"id": 38,
			# "arg": "uninit_bg",
			"value_type": None,
			"value": None, 
			"operator_value": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [28],  
			"weight": None,
			"must_child": False,
			"child_id": None
			}
		},
	"-q": {
		"id": 39,
		# "arg": "-q",
		"value_type": None,
		"value": None, 
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-r": {
		"id": 40,
		# "arg": "-r",
		# not sure how many numbers it takes, so far only setting to 1 works, and 0 is said to support 1.2 kernel
		"value_type": 1,
		"value": [0,1,1], 
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-S": {
		"id": 41,
		# "arg": "-S",
		# The e2fsck program should be run immediately after this option is used
		"value_type": None,
		"value": None, 
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-t": {
		"id": 42,
		# "arg": "-t",
		"value_type": 4,
		"value": ext_list, 
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": True,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-T": {
		"id": 43,
		# "arg": "-T",
		"value_type": 4,
		"value": usage_list, 
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-U": {
		"id": 44,
		# "arg": "-U",
		"value_type": 4,
		"value": UUID_list, 
		"operator_value": " ",
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-v": {
		"id": 45,
		# "arg": "-v",
		"value_type": None,
		"value": None, 
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-V": {
		"id": 46,
		# "arg": "-V",
		"value_type": None,
		"value": None, 
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
		},
	"-d": {
		"id": 47,
		"value_type": 3,
		"value": legacy_dir, 
		"operator_value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"must_child": False,
		"child_id": None
	}
}

with open('mke2fs.json', 'w') as f:
	json.dump(mke2fs_command, f, ensure_ascii=False, indent=4)