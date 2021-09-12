#!/bin/bash
#SBATCH --partition=tarrq
#SBATCH --nodelist=mind-1-23
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4
#SBATCH --open-mode=append
#SBATCH --output=./sbatch_output/output-%A-%x-%u.out 
#SBATCH --time=8-00:00:00

source ~/myenv/bin/activate

CWD=$(pwd)
cd ../../
ROOT=$(pwd)

subj=1
volume_space=0

# fitting_type=bdcn
fitting_type=gabor_solo
n_prf_sd_out=2
mult_patch_by_prf=1
do_nms=0
downsample_factor=1
do_pca=1
min_pct_var=95
max_pc_to_retain=400
map_ind=-1

n_ori=4
n_sf=4
group_all_hl_feats=1

ridge=1

shuffle_images=0
random_images=0
random_voxel_data=0

sample_batch_size=100
voxel_batch_size=100
zscore_features=1

up_to_sess=10
debug=0
shuff_rnd_seed=0

do_fitting=1
do_val=1
do_varpart=1

date_str=0

cd $ROOT/code/model_fitting

python3 fit_model2.py --subject $subj --volume_space $volume_space --up_to_sess $up_to_sess --sample_batch_size $sample_batch_size --voxel_batch_size $voxel_batch_size --zscore_features $zscore_features --ridge $ridge --do_pca $do_pca --min_pct_var $min_pct_var --max_pc_to_retain $max_pc_to_retain --map_ind $map_ind --debug $debug --fitting_type $fitting_type --shuffle_images $shuffle_images --random_images $random_images --random_voxel_data $random_voxel_data --do_fitting $do_fitting --do_val $do_val --date_str $date_str --shuff_rnd_seed $shuff_rnd_seed --n_prf_sd_out $n_prf_sd_out --mult_patch_by_prf $mult_patch_by_prf --do_nms $do_nms --downsample_factor $downsample_factor --group_all_hl_feats $group_all_hl_feats --n_ori $n_ori --n_sf $n_sf