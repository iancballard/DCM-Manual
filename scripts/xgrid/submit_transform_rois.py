#submits FSL ROI warp jobs
import sys
import os
import string

#############################################################
# check for valid kerberos ticket 
exit_status = os.system('klist -s')
if not exit_status == 0:			# 0 = sucesss
	print 'Your Kerberos ticket has expired'
	os.system('kinit')
#############################################################

# USER SETTINGS ############################################################
#define directories where your scripts are help and load the script to be submitted to xgrid
data_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/data/' #relevant directories
script_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/scripts' #relevant directories
lab_prob_atlas_dir='/Volumes/adcock_lab/main/resources/atlases'
ROI_files = string.join((lab_prob_atlas_dir + '/Midbrain_Atlases/mean_VTA', lab_prob_atlas_dir + '/harvard_subcort_prob/accumbens', data_dir + '/misc/DLPFC'),' ') #path to ROI masks
ROI_names = string.join(('fsl_vta', 'fsl_nacc','fsl_dlpfc'),' ') #the names for the warped versions, will go in the reg directory. Make sure that the index of the path and the name lines up

############################################################



template_file = os.path.join(script_dir,'xgrid/transform_rois.py') 
FSL_DIRECTORY = '/Volumes/adcock_lab/main/resources/software/base_programs/fsl/bin'


# get list of subjects to loop through 
subject_list = os.path.join(script_dir,'subject_list.txt')
subjects = []
subj_file = open(subject_list, 'r')
for subj in subj_file.readlines():
	subj = subj.strip('\n')
	subjects.append(subj)
subj_file.close()


#opens the template script, writes a temporary copy that replaces flag words with the SUBJ variable
for sub in subjects:
	sub=sub.split('/')
	sub = sub[0]
#	if sub!='L0012C00':
	temp_file = os.path.join(script_dir,'xgrid/fsl_reg_' + sub + '.py') #temporary file to be created
	path_dir = os.path.join(data_dir,sub,'anat/reg') #subject specific path
	f = open(template_file,'r')
	ff = open(temp_file, 'w')
	for line in f: #replace info in the file
		line = string.replace(line, 'SUBJECT_NUM',sub)
		line = string.replace(line, 'DATA_DIR',data_dir)
		line = string.replace(line,'PATH',path_dir)
		line = string.replace(line,'FSL_DIR',FSL_DIRECTORY)
		line = string.replace(line,'ROI_FILES',ROI_files)
		line = string.replace(line,'ROI_NAMES',ROI_names)
		ff.write(line)		
	f.close()		
	ff.close()
	cmd_str = string.join(('xgrid_sub', 'python', temp_file), ' ')
	os.system(cmd_str)