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

fs_size = 50000
flex_bg_id = 100
blocksize = 1024
MAX = 1000000
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

value_type = {"descrete_int": 0, "concrete_int": 1, "string": 2, "string_array": 3}


mke2fs_command = {
	"-b": {
		"id": 1,
		# "arg": "-b",
		"value": [1024, 2048, 4096], # -10 is the flag means select one from the following
		"value_type": 0,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": True, # set true for -i
		"dependency_id": None,
		# "weight": 0;
		"child": None
		},
	"-c": {
		"id": 2,
		# "arg": "-c",
		"value": None,
		"value_type": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,
		"child": {
			"c":{
			"id": 3,
			# "arg": "c",
			"value": None,
			"value_type": None,
			"operator_sibling": None,
			"operator_child": None,
			"mutex": None,
			"must_have": False,
			"dependency_id": [2],
			"child": None
			}
		}
		},
	"-E": {
		"id": 4,
		# "arg": "-E",
		"value": None,
		"value_type": None,
		"operator_sibling": " ",
		"operator_child": " ",
		"mutex": None,
		"must_have": True,
		"dependencies_id": None,
		"child": {
			"stride=": {  # RAID arg, need to test with '='' & '= ' 
				"id": 5,
				# "arg": "stride=", 
				"value": [0, MAX], 
				"value_type": 1,
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None,  
				"must_have": False,
				"dependency_id": [4], 
				"child": None,
				},
			"stride-width=": {  # RAID arg
				"id": 6,
				# "arg": "stride-width=", 
				"value": [0, MAX], # This is typically stride-size * N
				"value_type": 1,
				"child": None,
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None,  
				"must_have": False,
				"dependency_id": [4], 
				"child": None
				},
			"resize=": {  
				"id": 7,
				# "arg": "resize=", 
				"value": [0, MAX], 
				"value_type": 1,
				"child": None,
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None, 
				"must_have": False,
				"dependency_id": [4], 
				"child": None
				},
			"lazy_itable_init=": {  
				"id": 8,
				# "arg": "lazy_itable_init=", 
				"value": [0, 1],
				"value_type": 0,
				"child": None,
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None,  
				"must_have": False,
				"dependency_id": [4], 
				"child": None
				},
			"test_fs": {  
				"id": 9,
				# "arg": "test_fs", 
				"value": None,
				"value_type": None,
				"child": None,
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None, 
				"must_have": False,
				"dependency_id": [4], 
				"child": None
				},
			"discard": {  
				"id": 10,
				# "arg": "discard",  # SSD-related argument, discarding blocks initially is useful on solid state devices and sparse / thin-provisioned storage
				"value": None,
				"value_type": None,
				"child": None,
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None, 
				"must_have": False,
				"dependency_id": [4], 
				"child": None
				},
			"nodiscard": {  
				"id": 11,
				# "arg": "nodiscard",  # SSD-related argument, discarding blocks initially is useful on solid state devices and sparse / thin-provisioned storage
				"value": None,
				"value_type": None,
				"child": None,
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None, 
				"must_have": False,
				"dependency_id": [4], 
				"child": None
				}
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
		"value": None,
		"value_type": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": True,
		# set as true currently to avoid popping questions
		"dependency_id": None,
		"child": None
		},

########################################
##############checkpoint################
########################################
# checkpoint for modification on value type


	"-g": {
		"id": 13,
		# "arg": "-g",
		"value": {"multiple": 8}, # -3 is a flag for 'multiply'. Here it means 8 * N, maximum value is limited by disk capacity, may conflict with value (id:7)
		#  if (fs_param.s_blocks_per_group < 256 ||
		#              fs_param.s_blocks_per_group > 8 * (unsigned) blocksize) {
		#              com_err(program_name, 0, "%s",
		#                  _("blocks per group count out of range"));
		#              exit(1);
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,
		"child": None
		},
	"-G": {
		"id": 14,
		# "arg": "-G",
		"value": {"power": [2,0,-1]}, # should be power of 2, 0,-1 means 2^0 to 2^n, min & max need to be checked
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": [33], # to be replaced with real id
		"child": None
		},		
	"-i": {
		"id": 15,
		# "arg": "-i",
		"value": {"between": [1024, 67108864]},
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},	
	"-I": {
		"id": 16,
		# "arg": "-I",
		"value": {"power": [2, 7, 10]},  # value between 128 and 1024
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},
		# Global rule here: For 15 & 16, inode_size * inode_count shouldn't exceed blocksize * total_blocks
	"-j": {
		"id": 17,
		# "arg": "-j",
		"value": None,
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		# May need to be modified later May have to have ext3/4 enabled. In other words, doesn't work with a ext2 file system, 
		# tested with '-t ext2 -j', it will create a ext3 instead, so no dependency/mutex need to be specified here
		"child": None
		},
	"-J": {
		"id": 18,
		# "arg": "-J",
		"value": None,
		"operator_sibling": " ",
		"operator_child": " ",
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": {
			"size=": {  
				"id": 19,
				# "arg": "size=", 
				"value": {"between": [1024*blocksize/1048576, 102400*blocksize/1048576]}, 
				# Global Rule: The size of the journal must be at least 1024 filesystem blocks (i.e., 1MB if using 1k blocks, 4MB if using 4k blocks, etc.) and may be no more than 102,400 filesystem blocks.
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": [30],  
				"must_have": False,
				"dependency_id": [18], 
				"child": None,
				},
			"device=": {  
				"id": 20,
				# "arg": "device=", 
				"value": {"string": journal_dev}, 
				# Global rule: The external journal must already have been created using the command
				# mke2fs -O journal_dev external-journal
				# where external-journal must have been created with the same block size as the new filesystem
				# Need more design here ...
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": [29],  
				"must_have": False,
				"dependency_id": [18],  # Need more dependencies related to 'mke2fs -O journal_dev external-journal'
				"child": None,
				}
			}
		},	
	"-K": {
		"id": 21,
		# "arg": "-K",
		# An SSD related arg, Keep, do not attempt to discard blocks at mkfs time
		# depreciated, better one is '-E discard'
		"value": None,  # value between 128 and 1024
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},	
	"-l": {
		"id": 22,
		# "arg": "-l",
		# An SSD related arg, Keep, do not attempt to discard blocks at mkfs time
		# Mostly equvalant to -c
		"value": {"string": image},  # value between 128 and 1024
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},		
	"-L": {
		"id": 23,
		# "arg": "-L",
		"value": {"greater": 0}, 
		# The maximum length of the volume label is 16 bytes. 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},	
	"-m": {
		"id": 24,
		# "arg": "-m",
		"value": {"between": [0,50]}, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},	
	"-M": {
		"id": 25,
		# "arg": "-M",
		"value": {"string": mount_dir}, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},
	"-n": {
		"id": 26,
		# "arg": "-n",
		"value": None, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},
	"-N": {
		"id": 27,
		# "arg": "-N",
		"value": {"greater": 0}, 
		# Global rule: val_I * val_N <= block_num * block_size, is also related to val_i
		# Need a mature rule to orchestract -N -i -I and other possible inode num/size values
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},
	"-o": {
		"id": 28,
		# "arg": "-o",
		"value": {"select": os_list}, 
		# Need to provide a OS name list later
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},
	"-O": {
		"id": 29,
		# "arg": "-O",
		"value": None, 
		"operator_sibling": " ",
		"operator_child": " ",
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": {
			"dir_index": {
				"id": 30,
				# "arg": "dir_index",
				"value": None, 
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None,
				"must_have": False,
				"dependency_id": [29],  
				"child": None
				},
			"extent": {
				"id": 31,
				# "arg": "extent",
				"value": None, 
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None,
				"must_have": False,
				"dependency_id": [29],  
				"child": None
				},
			"filetype": {
				"id": 32,
				# "arg": "filetype",
				"value": None, 
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None,
				"must_have": False,
				"dependency_id": [29],  
				"child": None
				},
			"flex_bg": {
				"id": 33,
				# "arg": "flex_bg",
				"value": None, 
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None,
				"must_have": False,
				"dependency_id": [29],  
				"child": None
				},
			"has_journal": {
				"id": 34,
				# "arg": "has_journal",
				"value": None, 
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None,
				"must_have": False,
				"dependency_id": [29],  
				"child": None
				},
			"journal_dev": {
				"id": 35,
				# "arg": "journal_dev",
				# Create an external ext3 journal on the given device instead of a regular ext2 filesystem. 
				# Note that external-journal must be created with the same block size as the filesystems that will be using it.
				"value": None, 
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None,
				"must_have": False,
				"dependency_id": [29],  
				"child": None
				},
			"large_file": {
				"id": 36,
				# "arg": "large_file",
				# Modern kernels set this feature automatically when a file > 2GB is created.
				"value": None, 
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None,
				"must_have": False,
				"dependency_id": [29],  
				"child": None
				},
			"resize_inode": {
				"id": 37,
				# "arg": "resize_inode",
				# related to -E resize
				"value": None, 
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None,
				"must_have": False,
				"dependency_id": [29],  
				"child": None
			},
			"sparse_super": {
				"id": 38,
				# "arg": "sparse_super",
				# save space for large fs
				"value": None, 
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None,
				"must_have": False,
				"dependency_id": [29],  
				"child": None
			},
			"uninit_bg": {
				"id": 39,
				# "arg": "uninit_bg",
				"value": None, 
				"operator_sibling": ",",
				"operator_child": None,
				"mutex": None,
				"must_have": False,
				"dependency_id": [29],  
				"child": None
				}
			}
		},
	"-q": {
		"id": 40,
		# "arg": "-q",
		"value": None, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},
	"-r": {
		"id": 41,
		# "arg": "-r",
		"value": {"select": [0,1]}, 
		# not sure how many numbers it takes, so far only setting to 1 works, and 0 is said to support 1.2 kernel
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},
	"-S": {
		"id": 42,
		# "arg": "-S",
		# The e2fsck program should be run immediately after this option is used
		"value": None, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},
	"-t": {
		"id": 43,
		# "arg": "-t",
		"value": {"select": ext_list}, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": True,
		"dependency_id": None,  
		"child": None
		},
	"-T": {
		"id": 44,
		# "arg": "-T",
		"value": {"select": usage_list}, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},
	"-U": {
		"id": 45,
		# "arg": "-U",
		"value": {"select": UUID_list}, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},
	"-v": {
		"id": 46,
		# "arg": "-v",
		"value": None, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None
		},
	"-V": {
		"id": 47,
		# "arg": "-V",
		"value": None, 
		"operator_sibling": " ",
		"operator_child": None,
		"mutex": None,
		"must_have": False,
		"dependency_id": None,  
		"child": None,
		"weight": 0
		},
}

with open('mke2fs.json', 'w') as f:
	json.dump(mke2fs_command, f, ensure_ascii=False, indent=4)
# print(json_object)