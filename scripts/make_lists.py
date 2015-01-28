#outputs to the terminal window a list of paths to an SPM t-stat image for use in the second levels

import os
import numpy as np
import string

# USER SETTINGS ############################################################
data_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/data' #relevant directories
script_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/scripts' #relevant directories
subject_list = os.path.join(script_dir,'subject_list.txt')
image_of_interest = 'results_swr/spmT_0001.img,1'
############################################################################



# get list of subjects to loop through 
subjects = []
subj_file = open(subject_list, 'r')
for subj in subj_file.readlines():
	subj = subj.strip('\n')
	subjects.append(subj)
subj_file.close()

for subj in subjects:
	subject, date = subj.split('/')
	sub_path = os.path.join(data_dir,subject,image_of_interest)
	print sub_path
	