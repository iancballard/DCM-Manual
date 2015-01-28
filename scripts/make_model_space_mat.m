%%%%this creates the model space .mat file for use with Byaesian model
%%%%comparison. Will work if you use my naming convention, and if your
%%%%subjects star with L. Just a little tinkering with the script should
%%%%make it work in other situations.
clear;

%%%%%%%%USER DEFINED%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
data_path = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/data/'; %results directory where SPM.mat and VOI.mat files live
bad_subs = importdata('/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/scripts/roi_fails.txt');
num_driving = 7;
num_mod = 64;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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


for sub=1:length(subjects) %loop through subjects
    
    model=struct([]); %create a new model structure for every subject
    
    for i=1:num_driving %loop through models
        for j=1:num_mod
            
            %load each model and get the info you need for the
            %model_space.at file
            try temp_model = load([data_path subjects{sub} '/dcm/DCM_c' num2str(i) '_mod' num2str(j) '.mat']); 
            m = struct('fname',[data_path subjects{sub} '/dcm/DCM_c' num2str(i) '_mod' num2str(j) '.mat'],'F',temp_model.F,'Ep',temp_model.Ep,'Cp',temp_model.Cp);
            catch
                disp([data_path subjects{sub} '/dcm/DCM_c' num2str(i) '_mod' num2str(j) '.mat']);   %models which did not run
            end
            
            %add this info to the model structure
            if i==1 && j==1
                model = struct(m);
            else
                model(1,end+1)=struct(m);
            end
                  
        end
    end
    sess = struct('model',model);   %only 1 session, so just put the model in a session structure
    
    %then a new structure for each subject containing the sess structure
    %which contains (nothing but) that subject's model structure
    if sub==1
        subj = struct('sess',sess);
    else
        subj(1,end+1) = struct('sess',sess);
    end
    disp(subjects{sub});
end
save([data_path 'model_space.mat'],'subj');