import json

# template for an argument:
# "-b": {
# 	"value": , #required, can be 
# 	"value_combination": 1
# 	"child": None,
# 	"operator_sibling": " ",
# 	"operator_child": None,
# 	"operator_value": " ", 
# 	"mutex": None,
# 	"must_have": True
# 	# "special_ops": None
# }

MAX = 1000000
fs_size = 50000
flex_bg_id = 100
blocksize = 1024
journal_dev = ''
image = ''
mount_dir = ''
os_list = []
ext_list = ["ext2", "ext3", "ext4"]
usage_list = ["floppy", "small", "default"]
UUID_list = []
''' important: satisfying byte-per-inode ratio is essential to guarantee semantic correctness, 
need to specify some rules fo ensure this value is capatible with other arg values. Otherwise,
mke2fs will report 'Cannot create filesystem with requested number of inodes'
Currently have found value of '-E resize' (id:7) conflicts with value of '-g' (id:13)  '''

# Global rule: remove the last sibling operator of each arg branch

value_type = {"arithmatic_int": 1, "geometric_int": 2, "string": 3, "string_array": 4}


mke2fs_command = {
	"-b": {
		"id": 1,
		# "arg": "-b",
		"value_type": 2,
		"value": [2, 0, 2, 1024], # (2^0 to 2^2)*1024
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": True, # set true for -i
		"dependency_id": None,
		"weight": None
		},
	"-c": {
		"id": 2,
		# "arg": "-c",
		"value_type": None,
		"value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,
		"weight": None,
		"c":{
			"id": 3,
			# "arg": "c",
			"value_type": None,
			"value": None,
			"operator_sibling": None,
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [2],
			"weight": None
			}
		},
	"-E": {
		"id": 4,
		# "arg": "-E",
		"value_type": None,
		"value": None,
		"operator_sibling": " ",
		"operator_child": " ",
		"mutex": None,
		"must_have": True,
		"dependencies_id": None,
		"weight": None,
		"stride=": {  # RAID arg, need to test with '='' & '= ' 
			"id": 5,
			# "arg": "stride=", 
			"value_type": 1,
			"value": [0, MAX, 1], 
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,  
			"must_have": False,
			"dependency_id": [4], 
			"weight": None
			},
		"stride-width=": {  # RAID arg
			"id": 6,
			# "arg": "stride-width=", 
			"value_type": 1,
			"value": [0, MAX, 1], # This is typically stride-size * N
			"child": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,  
			"must_have": False,
			"dependency_id": [4], 
			"weight": None
			},
		"resize=": {  
			"id": 7,
			# "arg": "resize=", 
			"value_type": 1,
			"value": [0, MAX, 1], 
			"child": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None, 
			"must_have": False,
			"dependency_id": [4], 
			"weight": None
			},
		"lazy_itable_init=": {  
			"id": 8,
			# "arg": "lazy_itable_init=", 
			"value_type": 1,
			"value": [0, 1, 1],
			"child": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,  
			"must_have": False,
			"dependency_id": [4], 
			"weight": None
			},
		"test_fs": {  
			"id": 9,
			# "arg": "test_fs", 
			"value_type": None,
			"value": None,
			"child": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None, 
			"must_have": False,
			"dependency_id": [4], 
			"weight": None
			},
		"discard": {  
			"id": 10,
			# "arg": "discard",  # SSD-related argument, discarding blocks initially is useful on solid state devices and sparse / thin-provisioned storage
			"value_type": None,
			"value": None,
			"child": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None, 
			"must_have": False,
			"dependency_id": [4], 
			"weight": None
			},
		"nodiscard": {  
			"id": 11,
			# "arg": "nodiscard",  # SSD-related argument, discarding blocks initially is useful on solid state devices and sparse / thin-provisioned storage
			"value_type": None,
			"value": None,
			"child": None,
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None, 
			"must_have": False,
			"dependency_id": [4], 
			"weight": None
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
	"-F": {
		"id": 12,
		# "arg": "-F",
		"value_type": None,
		"value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": True,
		# set as true currently to avoid popping questions
		"dependency_id": None,
		"weight": None
		},

########################################
##############checkpoint################
########################################
# checkpoint for modification on value type
	"-g": {
		"id": 13,
		# "arg": "-g",
		#  if (fs_param.s_blocks_per_group < 256 ||
		#              fs_param.s_blocks_per_group > 8 * (unsigned) blocksize) {
		#              com_err(program_name, 0, "%s",
		#                  _("blocks per group count out of range"));
		#              exit(1);
		"value_type": 1,
		"value": [0, MAX, 8], # -3 is a flag for 'multiply'. Here it means 8 * N, maximum value is limited by disk capacity, may conflict with value (id:7)
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,
		"weight": None
		},
	"-G": {
		"id": 14,
		# "arg": "-G",
		"value_type": 2, # should be power of 2, 0,-1 means 2^0 to 2^n, min & max need to be checked
		"value": [2, 0, MAX, 1],
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": [33], # to be replaced with real id
		"weight": None
		},		
	"-i": {
		"id": 15,
		# "arg": "-i",
		"value_type": 1,
		"value": [1024, 67108864, 1],
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},	
	"-I": {
		"id": 16,
		# "arg": "-I",
		"value_type": 1,
		"value": [128, 1024, 2],  # value between 128 and 1024
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},
		# Global rule here: For 15 & 16, inode_size * inode_count shouldn't exceed blocksize * total_blocks
	"-j": {
		"id": 17,
		# "arg": "-j",
		"value_type": None,
		"value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		# May need to be modified later May have to have ext3/4 enabled. In other words, doesn't work with a ext2 file system, 
		# tested with '-t ext2 -j', it will create a ext3 instead, so no dependency/mutex need to be specified here
		"weight": None
		},
	"-J": {
		"id": 18,
		# "arg": "-J",
		"value_type": None,
		"value": None,
		"operator_sibling": " ",
		"operator_child": " ",
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"size=": {  
			"id": 19,
			# "arg": "size=", 
			"value_type": 1,
			# Global Rule: The size of the journal must be at least 1024 filesystem blocks (i.e., 1MB if using 1k blocks, 4MB if using 4k blocks, etc.) and may be no more than 102,400 filesystem blocks.
			"value": [1024*blocksize/1048576, 102400*blocksize/1048576, 1], 
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": [30],  
			"must_have": False,
			"dependency_id": [18], 
			"weight": None
			},
		"device=": {  
			"id": 20,
			# "arg": "device=", 
			"value_type": 3,
			"value": journal_dev, 
			# Global rule: The external journal must already have been created using the command
			# mke2fs -O journal_dev external-journal
			# where external-journal must have been created with the same block size as the new filesystem
			# Need more design here ...
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": [29],  
			"must_have": False,
			"dependency_id": [18],  # Need more dependencies related to 'mke2fs -O journal_dev external-journal'
			"weight": None
			}
			
		},	
	"-K": {
		"id": 21,
		# "arg": "-K",
		# An SSD related arg, Keep, do not attempt to discard blocks at mkfs time
		# depreciated, better one is '-E discard'
		"value_type": None,
		"value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},	
	"-l": {
		"id": 22,
		# "arg": "-l",
		# An SSD related arg, Keep, do not attempt to discard blocks at mkfs time
		# Mostly equvalant to -c
		"value_type": 3,
		"value": image,  # value between 128 and 1024
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},		
	"-L": {
		"id": 23,
		# "arg": "-L",
		# The maximum length of the volume label is 16 bytes. 
		"value_type": 1,
		"value": [0, MAX, 1], 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},	
	"-m": {
		"id": 24,
		# "arg": "-m",
		"value_type": 1,
		"value": [0,50,1], 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},	
	"-M": {
		"id": 25,
		# "arg": "-M",
		"value_type": 3,
		"value": mount_dir, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},
	"-n": {
		"id": 26,
		# "arg": "-n",
		"value_type": None,
		"value": None, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},
	"-N": {
		"id": 27,
		# "arg": "-N",
		"value_type": None,
		"value": [0,MAX,1], 
		# Global rule: val_I * val_N <= block_num * block_size, is also related to val_i
		# Need a mature rule to orchestract -N -i -I and other possible inode num/size values
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},
	"-o": {
		"id": 28,
		# "arg": "-o",
		"value_type": 4,
		"value": os_list, 
		# Need to provide a OS name list later
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},
	"-O": {
		"id": 29,
		# "arg": "-O",
		"value_type": None,
		"value": None, 
		"operator_sibling": " ",
		"operator_child": " ",
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None,
		"dir_index": {
			"id": 30,
			# "arg": "dir_index",
			"value_type": None,
			"value": None, 
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [29],  
			"weight": None
			},
		"extent": {
			"id": 31,
			# "arg": "extent",
			"value_type": None,
			"value": None, 
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [29],  
			"weight": None
			},
		"filetype": {
			"id": 32,
			# "arg": "filetype",
			"value_type": None,
			"value": None, 
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [29],  
			"weight": None
			},
		"flex_bg": {
			"id": 33,
			# "arg": "flex_bg",
			"value_type": None,
			"value": None, 
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [29],  
			"weight": None
			},
		"has_journal": {
			"id": 34,
			# "arg": "has_journal",
			"value_type": None,
			"value": None, 
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [29],  
			"weight": None
			},
		"journal_dev": {
			"id": 35,
			# "arg": "journal_dev",
			# Create an external ext3 journal on the given device instead of a regular ext2 filesystem. 
			# Note that external-journal must be created with the same block size as the filesystems that will be using it.
			"value_type": None,
			"value": None, 
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [29],  
			"weight": None
			},
		"large_file": {
			"id": 36,
			# "arg": "large_file",
			# Modern kernels set this feature automatically when a file > 2GB is created.
			"value_type": None,
			"value": None, 
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [29],  
			"weight": None
			},
		"resize_inode": {
			"id": 37,
			# "arg": "resize_inode",
			# related to -E resize
			"value_type": None,
			"value": None, 
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [29],  
			"weight": None
		},
		"sparse_super": {
			"id": 38,
			# "arg": "sparse_super",
			# save space for large fs
			"value_type": None,
			"value": None, 
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [29],  
			"weight": None
		},
		"uninit_bg": {
			"id": 39,
			# "arg": "uninit_bg",
			"value_type": None,
			"value": None, 
			"operator_sibling": ",",
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [29],  
			"weight": None
			}
		},
	"-q": {
		"id": 40,
		# "arg": "-q",
		"value_type": None,
		"value": None, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},
	"-r": {
		"id": 41,
		# "arg": "-r",
		# not sure how many numbers it takes, so far only setting to 1 works, and 0 is said to support 1.2 kernel
		"value_type": 1,
		"value": [0,1,1], 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},
	"-S": {
		"id": 42,
		# "arg": "-S",
		# The e2fsck program should be run immediately after this option is used
		"value_type": None,
		"value": None, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},
	"-t": {
		"id": 43,
		# "arg": "-t",
		"value_type": 4,
		"value": ext_list, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": True,
		"dependency_id": None,  
		"weight": None
		},
	"-T": {
		"id": 44,
		# "arg": "-T",
		"value_type": 4,
		"value": usage_list, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},
	"-U": {
		"id": 45,
		# "arg": "-U",
		"value_type": 4,
		"value": UUID_list, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},
	"-v": {
		"id": 46,
		# "arg": "-v",
		"value_type": None,
		"value": None, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		},
	"-V": {
		"id": 47,
		# "arg": "-V",
		"value_type": None,
		"value": None, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"weight": None
		}
}

with open('mke2fs.json', 'w') as f:
	json.dump(mke2fs_command, f, ensure_ascii=False, indent=4)
# print(json_object)