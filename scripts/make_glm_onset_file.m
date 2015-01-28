
%concatenates fsl condition info from 2 runs, for the MID, and outputs a
%.mat file for SPM. This is for the standard GLM used for 1) extraction and
%thresholind of ROIs and 2) group level analysis
clear;
data_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/data/';

%get subject list from the directory. All my subjects start with L, so I
%gather all of the folder names starting with L into a list
temp= dir([data_dir 'L*']);
subjects={};
for i=1:size(temp,1)
	subjects{end+1}=temp(i,1).name;
end

%Specify names of the conditions for the experiment. It is convenient to name them
%the same as the 3 column text files if you are using them
conditions = {'ant_gain5', 'ant_gain0', 'ant_gain1', 'ant_lose5', 'ant_lose0', 'ant_lose1', 'ant_con', 'outcomes'}; 

scans_per_run = 326;
TR=1.5;

for sub=1:length(subjects)
    %create 3 empty cell arrays, one for names, onsets, and durations 
    names=cell(1,length(conditions)); 
    onsets=cell(1,length(conditions));
    durations=cell(1,length(conditions));
    
    for cond=1:length(conditions) %loop through conditions
        
        condition_info_run1=load([data_dir subjects{sub} '/onsets/run1_' conditions{cond} '.txt']) ; %load each condition's 3 column text file. 
        condition_info_run2=load([data_dir subjects{sub} '/onsets/run2_' conditions{cond} '.txt']) ;
        
        %concatenate the 3 column files. But maeke sure to adjust the onsets by adding (scans_per_run * TR) to run2
        condition_info_run2(:,1) = condition_info_run2(:,1) +  scans_per_run * TR; 
        conditions_info_cc = [condition_info_run1 ; condition_info_run2];
        
        %read out the info from the 3 column files into each cell
        names{cond} = conditions{cond};
        onsets{cond} = conditions_info_cc(:,1);
        durations{cond} = conditions_info_cc(:,2);
        
    end
    save([data_dir subjects{sub} '/onsets/onsets_glm'],'names','onsets','durations'); %save the file in the subject's onset directory
end

