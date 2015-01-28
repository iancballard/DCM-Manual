##Superscript which loops through jobs or subjects and submits a seperate script to python with the job-specific variables
##Created by Ian Ballard and Jeff MacInnes, 2012. Contact: iancballard@gmail.com
import sys
import os
import string

# USER SETTINGS ############################################################
#define directories where your scripts are help and load the script to be submitted to xgrid
data_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/data/' #relevant directories
script_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/scripts/xgrid' #relevant directories
jobs_dir =  os.path.join(data_dir, 'templates/spmbatch_jobs_s/') # if you want to loop through jobs
loop_variable = 1 #1 to loop through jobs, 2 to exclude subjects for bad ROIs, and 3 to loop through subjects

if loop_variable==2:
	roi_fails = os.path.join(script_dir,'roi_fails.txt') #if you are at the point to remove subjects for failing ROI activation
if loop_variable==3:
	subject_list = os.path.join(script_dir,'clean_controls.txt') # if you want to loop through subjects

############################################################


#############################################################
# check for valid kerberos ticket 
exit_status = os.system('klist -s')
if not exit_status == 0:			# 0 = sucesss
	print 'Your Kerberos ticket has expired'
	os.system('kinit')
#############################################################


## BEGIN SUBMISSION LOOP:
xgrid_script = os.path.join(script_dir, 'matlab_xgrid.py') #script to be submitted to xgrid



if loop_variable==1: #loop through a list of jobs in a directory. This will create a list of all the files in a dirctory ending in .mat
	subjects = []
	for item in os.listdir(jobs_dir):
		if item[-4:] == '.mat':
			subjects.append(item)
			
elif loop_variable==2: #If at this point, you have subjects to remove for not having ROIs, generate list of subjects to loop through, removing subjects who have failed the roi test
	subjects_good = []
	for subj in subjects:
		split_sub = subj.split('/')[0]
		is_bad_sub=True
		subj_fails = open(roi_fails,'r') #loop through bad subjects
		for subj2 in subj_fails.readlines():
			subj2 = subj2.strip('\n')
			if subj2==split_sub: #if this subject matches any of the bad subjects, change the flag to false
				is_bad_sub=False
		if is_bad_sub==True: #if the flag is true, then the subject isnt on the bad subject list, so add it to our list
			subjects_good.append(subj)
		subj_fails.close()
	subjects = subjects_good
	
elif loop_variable==3: # loop through subjects
	subjects = []
	subj_file = open(subject_list, 'r')
	for subj in subj_file.readlines():
		subj = subj.strip('\n')
		subjects.append(subj)
	subj_file.close()
		
#pass the info you want to transfer to the xgrid script as an extra argument
for subj in subjects:
	sub = subj.split('_')
#if you only want to do 1 particular subject. normally comment this out
#	b = sub[1]
#	if b == 'L0012C00': 
	cmd_str = string.join(('xgrid_sub_select', 'python ', xgrid_script, subj, jobs_dir, data_dir, script_dir), ' ') #xgrid command string
	os.system(cmd_str)

