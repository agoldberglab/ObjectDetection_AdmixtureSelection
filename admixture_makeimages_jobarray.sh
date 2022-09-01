#!/bin/bash
#SBATCH -p scavenger
#SBATCH --job-name="png"
#SBATCH -a 1-100
#SBATCH --mem=5G
#SBATCH -o "100_png.out"

module load R/4.0.0

c=$SLURM_ARRAY_TASK_ID

declare -i c100="${c}00"

for i in {0..99};
do

c_array[$i]=$((c100 - i))

done

for i in "${c_array[@]}"
do

filename=$(ls /work/ih49/simulations/empirical/*_seed-${i}_alltracts.txt | head -n 1)
~/home/selectionscan_NN/simplified_scripts/admixture_makeimage_empirical.R $filename 49364325 200 /hpc/home/ih49/home/selectionscan_NN/767_AIM_positions_GB_empirical.RData

#filename=$(ls /work/ih49/simulations/model_misspecification/Fst_0/*_seed-${i}_alltracts.txt | head -n 1)
#~/home/selectionscan_NN/simplified_scripts/admixture_makeimage.R $filename 50000000 200

#filename=$(ls /work/ih49/simulations/model_misspecification/contraction/*_seed-${i}_alltracts.txt | head -n 1)
#~/home/selectionscan_NN/simplified_scripts/admixture_makeimage.R $filename 50000000 200

#filename=$(ls /work/ih49/simulations/model_misspecification/expansion/*_seed-${i}_alltracts.txt | head -n 1)
#~/home/selectionscan_NN/simplified_scripts/admixture_makeimage.R $filename 50000000 200

#filename=$(ls /work/ih49/simulations/model_misspecification/bottleneck/*_seed-${i}_alltracts.txt | head -n 1)
#~/home/selectionscan_NN/simplified_scripts/admixture_makeimage.R $filename 50000000 200

#filename=$(ls /work/ih49/simulations/model_misspecification/bottleneck_intense/*_seed-${i}_alltracts.txt | head -n 1)
#~/home/selectionscan_NN/simplified_scripts/admixture_makeimage.R $filename 50000000 200

#filename1=$(ls /work/ih49/simulations/local_ancestry_prop/*_seed-${i}_alltracts.txt | head -n 1)
#filename2=$(ls /work/ih49/simulations/local_ancestry_prop/*_seed-${i}_ancestryproportions_sample.csv | head -n 1)
#~/home/selectionscan_NN/simplified_scripts/admixture_makeimage_whole-genome.R $filename1 $filename2 50000000 200

done
