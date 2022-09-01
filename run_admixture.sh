#!/bin/bash
#SBATCH -p scavenger
#SBATCH --job-name="SLiMulation"
#SBATCH -a 1-10

c=$SLURM_ARRAY_TASK_ID

declare -i c100="${c}00"

for i in {0..99};
do

c_array[$i]=$((c100 - i))

done

for i in "${c_array[@]}"
do

/hpc/home/ih49/home/SLiM_build/slim -d L=50000000 -d N=10000 \
-d mig=0.5 -d t_end=50 \
-d out='"/work/ih49/simulations/model_misspecification/Fst_0/L-50_N-10000_single-pulse_Fst-0_m-0.5"' \
-d seed=\'"seed-$i"\' ~/home/selectionscan_NN/simplified_scripts/admixture_Fst.slim

/hpc/home/ih49/home/SLiM_build/slim -d L=50000000 -d N=10000 \
-d mig=0.75 -d t_end=50 \
-d out='"/work/ih49/simulations/model_misspecification/admix_prop_75/L-50_N-10000_single-pulse_m-0.75"' \
-d seed=\'"seed-$i"\' ~/home/selectionscan_NN/simplified_scripts/admixture.slim

done

