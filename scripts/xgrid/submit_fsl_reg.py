#submits FSL registration jobs
import sys
import os
import string


# USER SETTINGS ############################################################
data_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/data' #relevant directories
script_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/scripts' #relevant directories
subject_list = os.path.join(script_dir,'subject_list.txt')

#############################################################



#############################################################
# check for valid kerberos ticket 
exit_status = os.system('klist -s')
if not exit_status == 0:			# 0 = sucesss
	print 'Your Kerberos ticket has expired'
	os.system('kinit')
#############################################################

template_file = os.path.join(script_dir,'xgrid/fsl_reg.py') 
FSL_DIRECTORY = '/Volumes/adcock_lab/main/resources/software/base_programs/fsl/bin'

# get list of subjects to loop through 
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
		line = string.replace(line,'PATH',path_dir)
		line = string.replace(line,'FSL_DIR',FSL_DIRECTORY)
		line = string.replace(line,'FUNC_DIR',data_dir)
		ff.write(line)		
	f.close()		
	ff.close()
	cmd_str = string.join(('xgrid_sub', 'python', temp_file), ' ')
	os.system(cmd_str)