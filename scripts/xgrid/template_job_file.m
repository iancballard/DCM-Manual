%make sure the paths are added appropriately. This may not be necessary but it doesnt hurt.
p=genpath('/Volumes/adcock_lab/main/resources/programming/matlab/spm8/');
addpath(p)

%ask rita what this does
rehash toolbox
rehash toolboxcache

%fixes spm error. See manual for details
global host_name
host_name = 'this_host';

%spm_jobman is a generic script that runs the majority of spm .mat job files. It must be initialized and then passed a a job
spm_jobman('initcfg') 
spm_jobman('run',['f_path' 'file']) 
