##This job runs in xgrid. It makes a job specific m file, opens matlab, executes the m file, closes matlab, then deletes the m file
##Created by Ian Ballard and Jeff MacInnes, 2012. Contact: iancballard@gmail.com
import sys
import os
import string
import platform

# arguments passed by the superscript
subject = sys.argv[1] 
jobs_dir = sys.argv[2]  
data_dir = sys.argv[3] 
script_dir = sys.argv[4]

sub = subject.split('_')
b=sub[1];

# make subject specific .m file
matlab_dir = '/Volumes/adcock_lab/main/resources/software/base_programs/MATLAB_R2010a.app/bin/' #where matlab is held on the server
template_file = os.path.join(script_dir,'template_job_file.m') #this is your template .m file
temp_file = (os.path.join(script_dir) + 'template_job_file' + b + '.m') #create a temporary copy to add subject info to

computer_name = platform.node() #this is necessary for some troubleshooting. See manual for details

#opens the template script, writes a temporary copy that replaces flag words with the SUBJ variable
f = open(template_file,'r')
ff = open(temp_file, 'w')
for line in f:
	line = string.replace(line, 'file', subject) #in this case, the flag word is SUBJ (in the .m file), replaced with the variable subject
	line = string.replace(line, 'f_path', jobs_dir) #path to the job file
	line = string.replace(line, 'this_host', computer_name)
	ff.write(line)	
f.close()
ff.close()

#modify permissions on new file
cmd_str = string.join(('chmod','ug+rwx', temp_file), ' ')
os.system(cmd_str)

# open matlab, run file
cmd_str = (matlab_dir +  'matlab -nodisplay -nojvm < ' + temp_file  + ' > ' + script_dir + 'test' + b +'.txt') #matlab -nodisplay opens matlab, the file in brackets is the file it runs. Tand the last part saves a file called test.txt with output on the matlab screen. You could edit this to create job specific outputs for troubleshooting matlab errors
os.system(cmd_str) #runs the job

# delete job specific m file
#os.remove(temp_file)
