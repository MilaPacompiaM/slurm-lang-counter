#!/bin/bash
#SBATCH --job-name=getLangRankRe
#SBATCH --partition=sapphire
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --ntasks-per-node=4
#SBATCH --time=00:10:00
#SBATCH --output=slurm-%j.out

# when running it you should run: sbatch getLangRank.slurm name of file so we can test different files
module load OpenMPI/4.1.4
module load mpi4py/3.1.4

mpirun -np 8 python3 getLangRankRe.py "$1"
