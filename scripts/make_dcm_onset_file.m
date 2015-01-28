
%concatenates fsl condition info from 2 runs, for the MID, and outputs a
%.mat file for SPM. This is for the DCM, which has an ant_gain_all driving
%input vector for the gain 5 and gain 0 conditions.

clear;
%get subject list from the directory
data_dir = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/data/';
temp= dir([data_dir 'L*']);
subjects={};
for i=1:size(temp,1)
    subjects{end+1}=temp(i,1).name;
end

conditions = {'ant_gain5', 'ant_gain_all'};
scans_per_run = 326;
TR=1.5;
for sub=1:length(subjects)
    
    onsets_glm=load([data_dir subjects{sub} '/onsets/onsets_glm']);
    
    
    names=cell(1,length(conditions));
    onsets=cell(1,length(conditions));
    durations=cell(1,length(conditions));
    
    for cond=1:length(conditions)
        if cond==2 %the driving input condition
            names{2} = 'ant_gain_all';
            onsets{2} = sort([onsets_glm.onsets{1} ; onsets_glm.onsets{2}; onsets_glm.onsets{3}]);
            durations{2} = ones(60,1);
        else %modulatory inputs. These are typically single conditions, and so this part is identical as for the glm onset files
            condition_info_run1=load([data_dir subjects{sub} '/onsets/run1_' conditions{cond} '.txt']) ;
            condition_info_run2=load([data_dir subjects{sub} '/onsets/run2_' conditions{cond} '.txt']) ;
            
            %concatenate the 3 column files. But maeke sure to adjust the onsets by adding (scans_per_run * TR) to run2
            condition_info_run2(:,1) = condition_info_run2(:,1) +  scans_per_run * TR;
            conditions_info_cc = [condition_info_run1 ; condition_info_run2];
            
            %read out the info from the 3 column files into each cell
            names{cond} = conditions{cond};
            onsets{cond} = conditions_info_cc(:,1);
            durations{cond} = conditions_info_cc(:,2);
        end
    end
    
    save([data_dir subjects{sub} '/onsets/onsets_dcm'],'names','onsets','durations');
end



