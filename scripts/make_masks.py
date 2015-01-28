###makes a mask out of the peak cluster within an ROI. 

import os
import string


#######USER DEFINED#################################################################
data_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/data' #relevant directories
thresh = str(1.28) #threshold for t-stat images 1.65=.05 1.28=.1
voxel_extent = 3
this_roi = 'vta' 
subject_list = os.path.join(script_dir,'subject_list.txt')
roi_fails = os.path.join(script_dir,'roi_fails.txt')
################################################################################################

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


for subj in subjects:
	sub = subj.split('/')
	sub = sub[0]
	new_dir = os.path.join(MID_DIR,'Analysis/SPM',sub,'roi') #new directory for roi stats

	#this is the stats image masked by a binarized ROI. This should exist from get_cluster.py
	masked_stats = os.path.join(new_dir,'spmT_masked_' + this_roi)

	#make a copy of the cluster image where the clusters are ranked by size
	cluster_size = os.path.join(new_dir,this_roi + '_cluster_size')
	cmd_str = string.join(('cluster', ('--in=' + masked_stats), ('--thresh=' + thresh),'--osize=' + cluster_size),' ')
	os.system(cmd_str)

	#threshold cluster size image by minimum cluster size, then binarize
	cmd_str = string.join(('fslmaths', cluster_size, '-thr',voxel_extent , cluster_size),' ')
	os.system(cmd_str)
	cmd_str = string.join(('fslmaths', cluster_size, '-bin' , cluster_size),' ')
	os.system(cmd_str)

	#make a copy of the cluster image where the clusters are ranked by peak activation	
	cluster_max  = os.path.join(new_dir,this_roi + '_cluster_max')
	os.system('rm ' + cluster_max + '.nii') #delete old versions
	cmd_str = string.join(('cluster', ('--in=' + masked_stats), ('--thresh=' + thresh),'--omax=' + cluster_max),' ')
	os.system(cmd_str)

	#multiply the cluster max image by the thresholded, binarized cluster_size image to remove clusters that are below the cluster extent threshold
	cmd_str = string.join(('fslmaths', cluster_max, '-mul',cluster_size, cluster_max),' ')
	os.system(cmd_str)

	#get max of the image, and use this value to threshold it to get the peak cluster
	cmd_str = string.join(('fslstats', cluster_max, '-R'),' ') #get range
	max_of_mask = os.popen(cmd_str).read() #get max value in range
	max_of_mask =  max_of_mask.split(' ')[1]
	max_of_mask =  str(float(max_of_mask) - .1)
	cmd_str = string.join(('fslmaths', cluster_max, '-thr',max_of_mask , cluster_max),' ')
	os.system(cmd_str)

	#unzip mask
	cmd_str =  string.join(('gunzip', cluster_max + '.nii'),' ') 
	os.system(cmd_str)
	os.system('rm ' + cluster_max + '.nii.gz') #delete old versions

