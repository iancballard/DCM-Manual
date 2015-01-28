###gets the cluster size for VOIS at a given t value

import os
import string

#######USER DEFINED#################################################################
data_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/data' #relevant directories
script_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/scripts' #relevant directories
results_dir = 'results_sr' #name of the directory where you keep your results
stats_filename = 'spmT_0001.hdr' #will depend on which contrast you are using 
thresh = str(1.28) #threshold for t-stat images 1.65=.05 1.28=.1
roi_thresh = str(.25) #level to threshold probabilstic mask
voxel_extent = 3
this_roi = 'vta' 
subject_list = os.path.join(script_dir,'subject_list.txt')
################################################################################################

# generate list of subjects to loop through
subjects = []
subj_file = open(subject_list, 'r')
for subj in subj_file.readlines():
	subj = subj.strip('\n')
	subjects.append(subj)
subj_file.close()


for subj in subjects:
	sub = subj.split('/')
	sub = sub[0]
	
	new_dir = os.path.join(data_dir,sub,'roi') #new directory for roi stats
	if os.path.exists(new_dir)==False:
		cmd_str = string.join(('mkdir',new_dir),' ')
		os.system(cmd_str)
	
	
	#copy stats image and make nifti 
	stats_image = os.path.join(data_dir,sub,results_dir,stats_filename) 
	new_stats_image =os.path.join(new_dir,'spmT')
	cmd_str = string.join(('fslchfiletype', 'NIFTI', stats_image,  new_stats_image),' ')
	os.system(cmd_str)


	#threshold mask at threshold, binarize, and copy
	old_mask = os.path.join(data_dir,sub,'anat/reg/fsl_' + this_roi + '_func.nii.gz')
	new_mask = os.path.join(new_dir,this_roi + '.nii')
	os.system('rm ' + new_mask + '*') #delete old versions
	cmd_str = string.join(('fslmaths',old_mask, '-thr',roi_thresh,new_mask),' ') #threshold
	os.system(cmd_str)
		
	cmd_str = string.join(('fslmaths', new_mask, '-bin',new_mask),' ') #binarise
	os.system(cmd_str)
	
	#multiply the stats image by the mask
	masked_stats = os.path.join(new_dir,'spmT_masked_' + this_roi)
	cmd_str = string.join(('fslmaths', new_stats_image, '-mul',new_mask , masked_stats),' ')
	os.system(cmd_str)
	
	#get cluster info using fsl's cluster command
	cmd_str = string.join(('cluster', ('--in=' + masked_stats), ('--thresh=' + thresh) ),' ')
	cluster_data =  os.popen(cmd_str).read()
	cluster_data2 = cluster_data.split(' ')
	cluster_data2= cluster_data2[13].split('	')
	if len(cluster_data2)<2 or int(cluster_data2[1])<voxel_extent: #if there are no clusters, or if the biggest cluster is less than voxel_extent in size
		print sub
	#	print cluster_data
		
	os.system('gunzip ' + new_mask) #unzip the roi mask
