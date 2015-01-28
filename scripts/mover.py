"""
mover.py

Will move files into appropriate directories for SPM analysis

"""

import sys
import os
import shutil
import numpy as np
import glob
from nifti import *


MID_DIR = '/Volumes/singapore/MID'

subject_list = 'clean_controls.txt'
#'redo_subjs.txt'
subjects = np.genfromtxt(os.path.join(MID_DIR, 'Scripts/analysis_scripts/subject_lists/DCM', subject_list), dtype='string')
this_string=[];

for subj in subjects:
	subject, date = subj.split('/')
	if subject!='L0012C00':


	# if os.path.exists(os.path.join(MID_DIR, 'Analysis/SPM',subject,'onsets'))==True:
	# 	onset_dir=os.path.join(MID_DIR, 'Data/Behavioral',subj)
	# 	new_onset_dir=os.path.join(MID_DIR, 'Analysis/SPM',subject,'onsets')
	# #	os.mkdir(new_onset_dir)
	# 	onsetfiles=glob.glob(os.path.join(onset_dir,'run*'))
	# 
	# 	for onsets in onsetfiles:
	# 		name = onsets.split('/')
	# 		new_onset=os.path.join(MID_DIR, 'Analysis/SPM',subject,'onsets',name[8])
	#  		shutil.copy(onsets,new_onset)	 	

		# new_run1_dir=os.path.join(MID_DIR, 'Analysis/SPM',subject,'run1')
		# 	new_run2_dir=os.path.join(MID_DIR, 'Analysis/SPM',subject,'run2')
		# 	new_anat_dir=os.path.join(MID_DIR, 'Analysis/SPM',subject,'anat')
		# 	os.mkdir(new_run1_dir)
		# 	os.mkdir(new_run2_dir)
		# 	os.mkdir(new_anat_dir)
		# 
		# 	func_dir = os.path.join(MID_DIR, 'Analysis/SPM',subj,'run2.feat','filtered_func_data.nii.gz')
		# 	new_func_dir=os.path.join(MID_DIR, 'Analysis/SPM',subject,'run2','run2.nii')
		# 	cmd_str = 'gunzip -c ' + func_dir + ' > ' + new_func_dir
		# 	os.system(cmd_str)
		# 	
		# 
		# 	func_dir = os.path.join(MID_DIR, 'Analysis/SPM',subj,'run1.feat','filtered_func_data.nii.gz')
		# 	new_func_dir=os.path.join(MID_DIR, 'Analysis/SPM',subject,'run1','run1.nii')
		# 	cmd_str = 'gunzip -c ' + func_dir + ' > ' + new_func_dir
		# 	os.system(cmd_str)
		# 
		# 	anat_dir = os.path.join(MID_DIR, 'Data/Anat',subj,'COPLANAR_S1_brain.nii.gz')
		# 	new_anat_dir=os.path.join(MID_DIR, 'Analysis/SPM',subject,'anat','coplanar.nii')
		# 	cmd_str = 'gunzip -c ' + anat_dir + ' > ' + new_anat_dir
		# 	os.system(cmd_str)
		# 
		# anat_dir = os.path.join(MID_DIR, 'Data/Anat',subj,'FULL_ANAT_brain.nii.gz')
		# new_anat_dir=os.path.join(MID_DIR, 'Analysis/SPM',subject,'anat','full_anat.nii')
		# cmd_str = 'gunzip -c ' + anat_dir + ' > ' + new_anat_dir
		# os.system(cmd_str)
		# 
	#	getting un-skullstripped data from data files, sometimes there are 2 dates and it is in only one of them
		jobs_dir =  os.path.join(MID_DIR, MID_DIR, 'Data/Anat',subject)
		subjects = []
		for item in os.listdir(jobs_dir):
			subjects.append(item)	
		for sub in subjects:
			if os.path.exists(os.path.join(MID_DIR, 'Data/Anat',subject,sub,'FULL_ANAT.hdr')):
				anat_dir = os.path.join(MID_DIR, 'Data/Anat',subject,sub,'FULL_ANAT.hdr')
		anat_dir = anat_dir[:-4] 
		new_anat_dir=os.path.join(MID_DIR, 'Analysis/SPM',subject,'anat','full_anat_head.nii')
		os.system('fslchfiletype NIFTI ' + anat_dir + ' ' + new_anat_dir)
			

		# try:
		# 	anat_dir = os.path.join(MID_DIR, 'Data/Anat',subj,'FIELD_MAP_S1.hdr')
		# 	new_anat_dir=os.path.join(MID_DIR, 'Analysis/SPM',subject,'anat','FIELD_MAP_S1.hdr')
		# 	shutil.copyfile(anat_dir,new_anat_dir)
		# 
		# 	anat_dir = os.path.join(MID_DIR, 'Data/Anat',subj,'FIELD_MAP_S1.img')
		# 	new_anat_dir=os.path.join(MID_DIR, 'Analysis/SPM',subject,'anat','FIELD_MAP_S1.img')
		# 	shutil.copyfile(anat_dir,new_anat_dir)
		# except:
		# 	print 'no fieldmap for ' + subject

		print subject