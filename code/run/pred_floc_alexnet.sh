#!/bin/bash
#SBATCH --partition=tarrq
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --exclude=mind-1-13
#SBATCH --cpus-per-task=4
#SBATCH --open-mode=append
#SBATCH --output=./sbatch_output/output-%A-%x-%u.out 
#SBATCH --time=8-00:00:00

echo $SLURM_JOBID
echo $SLURM_NODELIST

source ~/myenv/bin/activate

# change this path
ROOT=/user_data/mmhender/modfit/

# put the code directory on your python path
PYTHONPATH=:${ROOT}code/${PYTHONPATH}

cd ${ROOT}code/model_fitting/

# subjects=(2 3 4 5 6 7 8)
subjects=(1 3 4 5 6 7 8)

debug=0
# debug=1

which_prf_grid=5

fitting_type=alexnet

alexnet_layer_name=best_layer
alexnet_padding_mode=reflect
use_pca_alexnet_feats=1

use_precomputed_prfs=1

image_set=floc

for subject in ${subjects[@]}
do
    
    python3 predict_other_ims.py --subject $subject --image_set $image_set --debug $debug --which_prf_grid $which_prf_grid --fitting_type $fitting_type --alexnet_layer_name $alexnet_layer_name  --alexnet_padding_mode $alexnet_padding_mode  --use_pca_alexnet_feats $use_pca_alexnet_feats --use_precomputed_prfs $use_precomputed_prfs
    
done