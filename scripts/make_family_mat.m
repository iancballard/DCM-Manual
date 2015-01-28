%%%%this makes the family division .mat file

%%%%%%%%USER DEFINED%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
data_path = '/Volumes/adcock_lab/main/resources/help_and_tutorials/dcm_practice/data/'; %results directory where SPM.mat and VOI.mat files live
num_families = 7;
models_per_family = 64;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

names=cell(1,length(num_families));
partition = [];
for i=1:num_families
    names{i}=['F' num2str(i)];
    partition = [partition zeros(1,models_per_family)+i];
end

family=struct('names',{names},'partition',partition);

save([data_path 'family.mat'],'family');