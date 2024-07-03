#!/bin/bash
#SBATCH -p hgx2q
#SBATCH --job-name="start_carla"
#SBATCH -n 1
#SBATCH --gres=gpu:1
#SBATCH --time 00-6:00:00    # time (D-HH:MM:SS)
module purge
module use /cm/shared/ex3-modules/latest/modulefiles
module load slurm/slurm/21.08.8
#module load cuda11.1/toolkit/11.1.1
#module load cuda11.8
module load cuda11.8/toolkit/11.8.0
source /home/chengjielu/anaconda3/bin/activate interfuser
export PYTHONPATH=root_path:$PYTHONPATH

cd /home/chengjielu/D1/projects/epiga-carla/epiga-project/carla/ && DISPLAY= ./CarlaUE4.sh --world-port=2000 -opengl