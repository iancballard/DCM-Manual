import os
os.system('cd FUNC_DIR/SUBJECT_NUM/anat/') #cd to the subject's anatomical directory

os.system('/bin/mkdir -p PATH') #add a new /reg directory

os.system('chmod -R ug+rwx PATH') #make sure permissions are set right for the new directory

#############this chunk was copied from the log of a typical fsl job. had to be made outside of the GUI in order to input meanrun1.nii from SPM

#copy in and rename anatomical and functional files
os.system('FSL_DIR/fslmaths FUNC_DIR/SUBJECT_NUM/anat/coplanar PATH/initial_highres') #coplanar

os.system('FSL_DIR/fslmaths FUNC_DIR/SUBJECT_NUM/anat/full_anat PATH/highres') #full anatomical (skull stripped)

os.system('FSL_DIR/fslmaths FUNC_DIR/SUBJECT_NUM/anat/full_anat_head  PATH/highres_head') #full anatomical (non skull stripped)

os.system('FSL_DIR/fslmaths /Volumes/adcock_lab/main/resources/software/base_programs/fsl/data/standard/MNI152_T1_2mm_brain PATH/standard') # template (skull stripped)

os.system('FSL_DIR/fslmaths /Volumes/adcock_lab/main/resources/software/base_programs/fsl/data/standard/MNI152_T1_2mm PATH/standard_head')  #template (non skull stripped)

os.system('FSL_DIR/fslmaths /Volumes/adcock_lab/main/resources/software/base_programs/fsl/data/standard/MNI152_T1_2mm_brain_mask_dil PATH/standard_mask') #mask for template brain

os.system('FSL_DIR/fslmaths FUNC_DIR/SUBJECT_NUM/run1/meanrun1  PATH/example_func') #mean of run 1 

#initial registration step, functional to coplanar
os.system('FSL_DIR/flirt -ref PATH/initial_highres -in PATH/example_func -out PATH/example_func2initial_highres -omat PATH/example_func2initial_highres.mat -cost corratio -dof 7 -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -interp trilinear  ')

#invert the last transformation
os.system('FSL_DIR/convert_xfm -inverse -omat PATH/initial_highres2example_func.mat PATH/example_func2initial_highres.mat')

os.system('FSL_DIR/flirt -ref PATH/highres -in PATH/initial_highres -out PATH/initial_highres2highres -omat PATH/initial_highres2highres.mat -cost corratio -dof 7 -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -interp trilinear  ')

os.system('FSL_DIR/convert_xfm -inverse -omat PATH/highres2initial_highres.mat PATH/initial_highres2highres.mat')

#concatenate transformations
os.system('FSL_DIR/convert_xfm -omat PATH/example_func2highres.mat -concat PATH/initial_highres2highres.mat PATH/example_func2initial_highres.mat')

#func to highres
os.system('FSL_DIR/flirt -ref PATH/highres -in PATH/example_func -out PATH/example_func2highres -applyxfm -init PATH/example_func2highres.mat -interp trilinear')

#invert last transformation
os.system('FSL_DIR/convert_xfm -inverse -omat PATH/highres2example_func.mat PATH/example_func2highres.mat')

#highres to standard
os.system('FSL_DIR/flirt -ref PATH/standard -in PATH/highres -out PATH/highres2standard -omat PATH/highres2standard.mat -cost corratio -dof 12 -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -interp trilinear  ')

#fnirt
os.system('FSL_DIR/fnirt --in=PATH/highres_head --aff=PATH/highres2standard.mat --cout=PATH/highres2standard_warp --iout=PATH/highres2standard --jout=PATH/highres2standard_jac --config=T1_2_MNI152_2mm --ref=PATH/standard_head --refmask=PATH/standard_mask --warpres=10,10,10')

#invert fnirt, standard to high res
os.system('FSL_DIR/convert_xfm -inverse -omat PATH/standard2highres.mat PATH/highres2standard.mat')

#concatenate transforms from fnirt and flirt
os.system('FSL_DIR/convert_xfm -omat PATH/example_func2standard.mat -concat PATH/highres2standard.mat PATH/example_func2highres.mat')

#apply warp to functional data
os.system('FSL_DIR/applywarp --ref=PATH/standard --in=PATH/example_func --out=PATH/example_func2standard --warp=PATH/highres2standard_warp --premat=PATH/example_func2highres.mat')

#invert warp
os.system('FSL_DIR/convert_xfm -inverse -omat PATH/standard2example_func.mat PATH/example_func2standard.mat')

###this ends the part copied from the FSL log files

#this inverts the warp and applies transforms to the functional data
os.system('FSL_DIR/invwarp -w PATH/highres2standard_warp -o PATH/highres2standard_warp_inv -r PATH/highres')

os.system('FSL_DIR/applywarp --ref=PATH/standard --in=FUNC_DIR/SUBJECT_NUM/run1/rrun1  --out=FUNC_DIR/SUBJECT_NUM/run1/wrrun1  --warp=PATH/highres2standard_warp --premat=PATH/example_func2highres.mat')
os.system('FSL_DIR/applywarp --ref=PATH/standard --in=FUNC_DIR/SUBJECT_NUM/run2/rrun2  --out=FUNC_DIR/SUBJECT_NUM/run2/wrrun2 --warp=PATH/highres2standard_warp --premat=PATH/example_func2highres.mat')

#this strips out some of the non-brain voxels to reduce the image size
os.system('FSL_DIR/fslroi FUNC_DIR/SUBJECT_NUM/run1/wrrun1 FUNC_DIR/SUBJECT_NUM/run1/wrrun1_stripped 0 86 0 104 0 86')
os.system('FSL_DIR/fslroi FUNC_DIR/SUBJECT_NUM/run2/wrrun2 FUNC_DIR/SUBJECT_NUM/run2/wrrun2_stripped 0 86 0 104 0 86')

#unzip to make spm happy
os.system('gunzip ' +  '/FUNC_DIR/SUBJECT_NUM/run1/wrrun1_stripped.nii.gz')
os.system('gunzip ' +  '/FUNC_DIR/SUBJECT_NUM/run2/wrrun2_stripped.nii.gz')

