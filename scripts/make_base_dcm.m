%%batch script which loops through subjects and makes a base dcm model for
%%another script to modify with the appropriate a,b, and c matrices. Must
%%have specified, but not estimated, an SPM.mat file
%%Disclaimer: This is largely copied from a script available for the
%%tutorial attntion to visual motion dataset, and I have no knowledge as to
%%what many of these variables are. The best I can do is see if the output
%%matches that of the GUI


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%Must specify these variables%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
data_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/data/'; %results directory where SPM.mat and VOI.mat files live
spm_dir = '/results_dcm/SPM.mat'; %where you have the SPM.mat with the appropriate onset files
TE = .03; %TE in seconds
TR=1.5; 
output_model = '/results_dcm/DCM_base_model.mat';
ROI_1 = '/results_dcm/VOI_VTA_1.mat';
ROI_2 = '/results_dcm/VOI_NACC_1.mat';
ROI_3 = '/results_dcm/VOI_MFGB46_1.mat';
bad_subs = importdata('Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/roi_fails.txt');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%%Also see below for options about centering inputs, nonlinear, et cetera.
%%These are described briefly in the extensions section of the manual.
%%Using them may require a bit of tinkering with the script.

%get subject list from the directory. All my subjects start with L, so I
%gather all of the folder names starting with L into a list
temp= dir([data_path 'L*']);
subjects={};
for i=1:size(temp,1)
    subjects{end+1}=temp(i,1).name;
end
good_subjects=[];
for i=1:length(subjects)
    is_bad_sub=0;
    for j=1:length(bad_subs)
        if strcmp(subjects{i},bad_subs{j})==1
            is_bad_sub=1;
        end
    end
    if is_bad_sub==0
        good_subjects{end+1}=subjects{i};
    end
end
subjects = good_subjects;

for sub=1:length(subjects)
    
    %names of the VOIs, in this case there are 3
    VOI_1 = [subjects{sub} ROI_1];
    VOI_2 = [subjects{sub} ROI_2];
    VOI_3 = [subjects{sub} ROI_3];
    
    load(fullfile(data_dir,subjects{sub},spm_dir)); %load the SPM.mat file
    
    %fill the xY file with the appropriate data
    load(fullfile(data_dir,VOI_1),'xY');
    DCM.xY(1) = xY;
    load(fullfile(data_dir,VOI_2),'xY');
    DCM.xY(2) = xY;
    load(fullfile(data_dir,VOI_3),'xY');
    DCM.xY(3) = xY;
    
    DCM.n = length(DCM.xY);      % number of regions
    DCM.v = length(DCM.xY(1).u); % number of time points
    
    %fill up Y cells. This is largely information extracted from the ROIs
    DCM.Y.dt  = SPM.xY.RT;
    DCM.Y.X0  = DCM.xY(1).X0;
    for i = 1:DCM.n
        DCM.Y.y(:,i)  = DCM.xY(i).u;
        DCM.Y.name{i} = DCM.xY(i).name;
    end
    DCM.Y.Q    = spm_Ce(ones(1,DCM.n)*DCM.v);
    
    %fill up U cells. This will need to be modified depending on which
    %columns you are using as inputs. Often you will only be modelling some of the
    %columns of the design matrix
    DCM.U.dt   =  SPM.Sess.U(1).dt;
    DCM.U.name = [];
    DCM.U.u = [];
    
    for i=1:2 %this dcm only has to types of inputs. In this case the first 2 in the design matrix. This will need to be changed according to your needs
        DCM.U.name = [DCM.U.name SPM.Sess.U(i).name];
        DCM.U.u    = [DCM.U.u SPM.Sess.U(i).u(33:end,1)]; %The 33 is a mystery....
    end
    
    DCM.delays = [TR;TR;TR];  %slice timing delays. 0s for no extra slice timing correction
    DCM.TE = TE;      %scanner TE
    
    DCM.options.nonlinear  = 0;
    DCM.options.two_state  = 0;
    DCM.options.stochastic = 0;
    DCM.options.centre = 0;
    DCM.options.endogenous = 0;
    
    %This will be filled out by the script that constructs the model space
    DCM.a = [];
    DCM.b = [];
    DCM.c = [];
    DCM.d = [];
    
    save(fullfile(data_dir,subjects{sub}, output_model),'DCM');
end