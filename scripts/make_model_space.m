%%batch script which loops through subjects, copies the base dcm model and
%%constructs a dcm for each model in the full model space. This will have
%%to be adapted for the specific A,B,and C matrices you are testing. This
%%specific version will vary all combinations of B and C possibilities,
%%while mantaining the full intrinsic connectivity matrix, A. Further, this
%%example has specific columns of the design matrix acting exclusively as
%%driving or modulatory inputs, never both.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%Must specify these variables%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
data_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/data/';
num_vois = 3;  %number of regions in your model
num_conditions = 2; %total number of conditions (design matrix columns) which act on the DCMs
base_model = '/results_dcm/DCM_base_model.mat';
bad_subs = importdata('Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/roi_fails.txt');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%get subject list from the directory. All my subjects start with L, so I
%gather all of the folder names starting with L into a listtemp= dir([data_dir 'L*']);
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


%%Construct matrices
a_matrix = [1 1 1; 1 1 1; 1 1 1]; %all of these models have full intrinsic connectivity
%c_all= [1 1 1 0 0 0 1; 1 1 0 1 1 0 0 ; 1 0 0 1 0 1 1]; %this 3x7 matrix has all 7 possible combinations of driving inputs (1s and 0s) for 3 regions
c_all = [[1,1,1;1,1,0;1,0,0;]];

%%makes all of the possible b matrices
%This chunk fills a list with all unique permutations of ones and
%zeros, which are then filled into the appropriate entries of the b matrix
num_permutations = 2; %number of different entries of the b matrix to be permuted. Must be <=num_vois^2 - num_vois = 6
elements = [ 0 0 0 0 0 0 0 0 0 0 1 1]; %num_permutations random entries will be taken from elements and checked for uniquness. 7 is the max number of replacements
permutation_list = zeros(1,num_permutations); %list to be filled

while size(permutation_list,1) < 2^num_permutations
    vector =  randsample(elements,num_permutations);
    permutation_list(end+1,:)= vector;
    permutation_list = unique(permutation_list, 'rows');
end

all_models = []; %store all_models for reference when writing DCM.mat files
for i = 1:size(permutation_list,1)
    matrix = [0 1 permutation_list(i,2); 1 0 0; 1 permutation_list(i,1)  0]; %fill in the b matrix with the correct entries from list at the entries want to vary
%    dlmwrite([data_dir 'matrices.txt'], matrix, 'delimiter', '\t', '-append', 'precision', 0, 'roffset', 3);     %print models for reference
    all_models(:,:,i) = matrix;
end

%Create the DCM.mat files
for sub=1:length(subjects)
    for i=1:length(c_all)       %for all the driving inputs
        for j=1:size(permutation_list,1)     %for all the modulatory inputs

            %create a copy of the template named DCM_c{driving input
            %number}_mod{modulatory input number}
            copyfile([data_dir subjects{sub} base_model], [data_dir subjects{sub} '/results_dcm/DCM_c' num2str(i) '_mod' num2str(j) '.mat']);
            load([data_dir subjects{sub} '/results_dcm/DCM_c' num2str(i) '_mod' num2str(j) '.mat']);
            
            driving = zeros(num_vois,num_conditions);
            driving(:,2)  = c_all(:,i);		%%in this case the second condition is the driving input, so the first column stays zero
               
            %B matrices are 3 dimensional, since there is a seperate 2D B
            %for each modulatory input (for a driving input, the
            %correspodnding B matrix is all 0s).  So B(:,:,1) corresponds
            %to the modulatory connections of the first regressor. 
            mod = zeros(num_vois,num_vois,num_conditions);		%%in this case the first condition is the modulatory input, so mod(:,:,2) stays zero
            mod(:,:,1) = all_models(:,:,j);

            %save the matrices in the appropriate fields of the data
            %structure
            DCM.c = driving;
            DCM.b = mod;
            DCM.a = a_matrix;
d = double([]);
d = reshape(d,3,3,0);			
DCM.d = d
            save([data_dir subjects{sub} '/results_dcm/DCM_c' num2str(i) '_mod' num2str(j) '.mat'],'DCM');     %save the new file
        end

    end
end

