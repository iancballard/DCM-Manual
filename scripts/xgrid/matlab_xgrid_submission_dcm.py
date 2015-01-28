##Superscript which loops through jobs or subjects and submits a seperate script to python with the job-specific variables
##Created by Ian Ballard and Jeff MacInnes, 2012. Contact: iancballard@gmail.com
import sys
import os
import string

# USER SETTINGS ############################################################
#define directories where your scripts are help and load the script to be submitted to xgrid
data_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/data' #relevant directories
script_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/scripts/' #relevant directories
subject_list = os.path.join(script_dir,'subject_list.txt')
bad_roi_list = os.path.join(script_dir,'roi_fails.txt')
############################################################


#############################################################
# check for valid kerberos ticket 
exit_status = os.system('klist -s')
if not exit_status == 0:			# 0 = sucesss
	print 'Your Kerberos ticket has expired'
	os.system('kinit')
#############################################################


## BEGIN SUBMISSION LOOP:
xgrid_script = os.path.join(script_dir, 'xgrid/matlab_xgrid_dcm.py') #script to be submitted to xgrid


jobs_dir =  os.path.join(MID_DIR, 'Analysis/SPM/spmbatch_jobs_extract_vois_gain/')
subjects = []
for item in os.listdir(jobs_dir):
	if item[-4:] == '.mat':
		subjects.append(item)

# generate list of subjects to loop through, removing subjects who have failed the roi test
subjects = []
subj_file = open(subject_list, 'r')
for subj in subj_file.readlines():
	subj = subj.strip('\n')
	split_sub = subj.split('/')[0]
	
	flag=True
	subj_fails = open(roi_fails,'r') #loop through bad subjects
	for subj2 in subj_fails.readlines():
		subj2 = subj2.strip('\n')
		if subj2==split_sub: #if this subject matches any of the bad subjects, change the flag to false
			flag=False

	if flag==True: #if the flag is true, then the subject isnt on the bad subject list, so add it to our list
		subjects.append(subj)
	subj_fails.close()
subj_file.close()


#pass the info you want to transfer to the xgrid script as an extra argument
for subj in subjects:
	subj = subj.split('/')
	sub = subj[0]
	jobs_dir =  os.path.join(data_dir, sub, 'results_dcm/')
	jobs = []
	for item in os.listdir(jobs_dir):
		if item[0:5] == 'DCM_c':  ##make sure the .mat files are DCM jobs you want (not the base model)
			jobs.append(item)
	for job in jobs:
		cmd_str = string.join(('xgrid_sub_select', 'python ', xgrid_script, sub, jobs_dir, job, data_dir, script_dir), ' ') #xgrid command string
		os.system(cmd_str)

