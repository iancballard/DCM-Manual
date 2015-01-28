#apply the inverse nonlinear warps to the ROIs

import os
os.system('cd DATA_DIR/SUBJECT_NUM/anat/')

ROI_files='ROI_FILES'
ROI_names = 'ROI_NAMES'
ROI_files = ROI_files.split(' ')
ROI_names = ROI_names.split(' ')
for index, roi in enumerate(ROI_files):
	os.system('FSL_DIR/applywarp --ref=PATH/highres --in=' + roi +' --out=PATH/' + ROI_names[index] + '_anat --warp=PATH/highres2standard_warp_inv')
	os.system('FSL_DIR/applywarp --ref=PATH/example_func --in=' + roi +' --out=PATH/' + ROI_names[index] + '_func --warp=PATH/highres2standard_warp_inv --postmat=PATH/highres2example_func.mat')

